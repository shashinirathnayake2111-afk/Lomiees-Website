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
LEFT_SHOULDER = 11;  RIGHT_SHOULDER = 12
LEFT_HIP = 23;       RIGHT_HIP = 24

# Global landmarker
_landmarker = None

def _get_landmarker():
    global _landmarker
    if _landmarker is None:
        base_options = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
        options = mp_vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=mp_vision.RunningMode.IMAGE,
            output_segmentation_masks=False
        )
        _landmarker = mp_vision.PoseLandmarker.create_from_options(options)
    return _landmarker

def _detect_landmarks(img):
    if len(img.shape) == 3 and img.shape[2] == 4:
        img = img[:, :, :3]
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    rgb = np.ascontiguousarray(rgb)
    landmarker = _get_landmarker()
    try:
        mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = landmarker.detect(mp_img)
        if result.pose_landmarks:
            return result.pose_landmarks[0]
    except:
        pass
    return None

def _px(lm_pt, w, h):
    return (int(lm_pt.x * w), int(lm_pt.y * h))

def _get_skin_mask(bgr):
    ycrcb = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, np.array([0, 20, 70]), np.array([25, 255, 255]))
    mask2 = cv2.inRange(ycrcb, np.array([0, 133, 77]), np.array([255, 173, 127]))
    return cv2.bitwise_and(mask1, mask2)

def _extract_garment_mask(bgra, landmarks):
    h, w = bgra.shape[:2]
    alpha = bgra[:, :, 3].copy()
    if landmarks:
        ls = _px(landmarks[LEFT_SHOULDER], w, h)
        rs = _px(landmarks[RIGHT_SHOULDER], w, h)
        shoulder_y = min(ls[1], rs[1])
        alpha[:max(0, shoulder_y - 10), :] = 0
        neck_center = ((ls[0] + rs[0]) // 2, shoulder_y)
        neck_radius = int(abs(ls[0] - rs[0]) * 0.2)
        cv2.circle(alpha, neck_center, neck_radius, 0, -1)
    
    skin = _get_skin_mask(bgra[:,:,:3])
    alpha[skin > 0] = 0
    res = bgra.copy()
    res[:, :, 3] = alpha
    return res

def overlay_clothing(user_image_path, clothing_image_path, output_path):
    user_img = cv2.imread(user_image_path)
    if user_img is None: return False, "User image read fail"
    u_h, u_w = user_img.shape[:2]

    u_lm = _detect_landmarks(user_img)
    if not u_lm: return False, "Err: Pose not detected"

    try:
        with open(clothing_image_path, 'rb') as f: img_data = f.read()
        removed = rembg_remove(img_data)
        pil_img = Image.open(io.BytesIO(removed)).convert("RGBA")
        c_bgra = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGBA2BGRA)
    except: return False, "Err: Clothing processing"

    c_h, c_w = c_bgra.shape[:2]
    c_lm = _detect_landmarks(c_bgra[:,:,:3])
    if not c_lm: return False, "Err: Product pose not detected"

    garment = _extract_garment_mask(c_bgra, c_lm)

    def get_quad(lm, w, h):
        return np.float32([
            _px(lm[LEFT_SHOULDER], w, h), _px(lm[RIGHT_SHOULDER], w, h),
            _px(lm[RIGHT_HIP], w, h), _px(lm[LEFT_HIP], w, h)
        ])
    
    src_quad = get_quad(c_lm, c_w, c_h)
    dst_quad = get_quad(u_lm, u_w, u_h)

    try:
        M = cv2.getPerspectiveTransform(src_quad, dst_quad)
        warped = cv2.warpPerspective(garment, M, (u_w, u_h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))
    except:
        return False, "Err: Warping failed"

    fg = warped[:, :, :3]
    mask = warped[:, :, 3]

    y_indices, x_indices = np.where(mask > 0)
    if len(y_indices) == 0: return False, "Err: Out of bounds"
    
    center = (int((x_indices.min() + x_indices.max()) / 2), int((y_indices.min() + y_indices.max()) / 2))

    try:
        res = cv2.seamlessClone(fg, user_img, mask, center, cv2.NORMAL_CLONE)
    except:
        alpha = (mask / 255.0)[:, :, np.newaxis].astype(np.float32)
        res = (fg.astype(np.float32) * alpha + user_img.astype(np.float32) * (1 - alpha)).astype(np.uint8)

    cv2.imwrite(output_path, res)
    return True, output_path
