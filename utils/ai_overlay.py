import cv2
import mediapipe as mp
import numpy as np
import os
from PIL import Image
import io

from rembg import remove as rembg_remove
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'pose_landmarker.task')

# Landmark indices
NOSE = 0
LEFT_EYE = 2; RIGHT_EYE = 5
LEFT_SHOULDER = 11; RIGHT_SHOULDER = 12
LEFT_ELBOW = 13; RIGHT_ELBOW = 14
LEFT_WRIST = 15; RIGHT_WRIST = 16
LEFT_HIP = 23; RIGHT_HIP = 24

def _get_landmarker():
    base_options = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
    options = mp_vision.PoseLandmarkerOptions(
        base_options=base_options,
        running_mode=mp_vision.RunningMode.IMAGE
    )
    return mp_vision.PoseLandmarker.create_from_options(options)

def _detect_landmarks(img_bgr):
    rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    lm_er = _get_landmarker()
    result = lm_er.detect(mp_img)
    lm_er.close()
    if result.pose_landmarks and len(result.pose_landmarks) > 0:
        return result.pose_landmarks[0]
    return None

def _px(lm_pt, w, h):
    return (int(lm_pt.x * w), int(lm_pt.y * h))

def _skin_mask(bgr):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    ycrcb = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb)
    # Define skin color ranges
    mask1 = cv2.inRange(hsv, np.array([0, 20, 70]), np.array([25, 255, 255]))
    mask2 = cv2.inRange(ycrcb, np.array([0, 133, 77]), np.array([255, 173, 127]))
    return cv2.bitwise_and(mask1, mask2)

def _extract_fabric(bgra, lm):
    if lm is None: return bgra
    h, w = bgra.shape[:2]
    alpha = bgra[:, :, 3].copy()
    
    # 1. Anatomical Erasure (Head)
    nose = _px(lm[NOSE], w, h)
    ls = _px(lm[LEFT_SHOULDER], w, h)
    rs = _px(lm[RIGHT_SHOULDER], w, h)
    # Erase circle around face
    head_radius = int(abs(ls[0]-rs[0]) * 0.4)
    cv2.circle(alpha, nose, head_radius, 0, -1)
    # Erase everything above shoulder level
    shoulder_y = min(ls[1], rs[1])
    alpha[:shoulder_y - 10, :] = 0

    # 2. Skin Segmentation
    skin = _skin_mask(bgra[:,:,:3])
    alpha[skin > 0] = 0
    
    # 3. Hand Erasure
    for wrist in [LEFT_WRIST, RIGHT_WRIST]:
        pt = _px(lm[wrist], w, h)
        cv2.circle(alpha, pt, int(w*0.1), 0, -1)

    res = bgra.copy()
    res[:, :, 3] = alpha
    return res

def overlay_clothing(user_image_path, clothing_image_path, output_path):
    user_img = cv2.imread(user_image_path)
    if user_img is None: return False, "User image read fail"
    u_h, u_w = user_img.shape[:2]
    u_lm = _detect_landmarks(user_img)
    if u_lm is None: return False, "User pose not detected"

    # Product
    with open(clothing_image_path, 'rb') as f:
        img_data = f.read()
    removed = rembg_remove(img_data)
    pil_img = Image.open(io.BytesIO(removed)).convert("RGBA")
    c_bgra = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGBA2BGRA)
    c_h, c_w = c_bgra.shape[:2]
    c_lm = _detect_landmarks(c_bgra[:,:,:3])
    
    garment = _extract_fabric(c_bgra, c_lm)

    # Warp
    if c_lm is None: return False, "Product pose not detected"
    
    def get_quad(lm, w, h):
        ls = _px(lm[LEFT_SHOULDER], w, h); rs = _px(lm[RIGHT_SHOULDER], w, h)
        lh = _px(lm[LEFT_HIP], w, h); rh = _px(lm[RIGHT_HIP], w, h)
        # Expand slightly
        dx = abs(rs[0]-ls[0]) * 0.2
        dy = abs(lh[1]-ls[1]) * 0.1
        return np.float32([[ls[0]-dx, ls[1]-dy], [rs[0]+dx, rs[1]-dy], [rh[0]+dx, rh[1]+dy], [lh[0]-dx, lh[1]+dy]])

    src = get_quad(c_lm, c_w, c_h)
    dst = get_quad(u_lm, u_w, u_h)
    
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(garment, M, (u_w, u_h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))
    
    # Blend
    fg = warped[:,:,:3].astype(np.float32)
    alpha = (warped[:,:,3] / 255.0).astype(np.float32)[:,:,np.newaxis]
    bg = user_img.astype(np.float32)
    
    res = (fg * alpha + bg * (1-alpha)).astype(np.uint8)
    cv2.imwrite(output_path, res)
    return True, output_path
