from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)

class SizeChart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(10), nullable=False)  # 'Men', 'Women', 'Kids'
    size = db.Column(db.String(10), nullable=False)    # 'S', 'M', 'L', 'XL', etc.
    min_height = db.Column(db.Float, nullable=False)   # in cm
    max_height = db.Column(db.Float, nullable=False)
    min_weight = db.Column(db.Float, nullable=False)   # in kg
    max_weight = db.Column(db.Float, nullable=False)

def seed_size_chart():
    if SizeChart.query.first():
        return
    
    # Sample data for Men
    men_sizes = [
        ('Men', 'S', 160, 170, 50, 65),
        ('Men', 'M', 165, 175, 60, 75),
        ('Men', 'L', 170, 185, 70, 85),
        ('Men', 'XL', 180, 195, 80, 100),
        ('Men', 'XXL', 185, 205, 95, 120),
    ]
    
    # Sample data for Women
    women_sizes = [
        ('Women', 'XS', 150, 160, 40, 50),
        ('Women', 'S', 155, 165, 45, 55),
        ('Women', 'M', 160, 170, 55, 65),
        ('Women', 'L', 165, 175, 65, 75),
        ('Women', 'XL', 170, 185, 75, 90),
    ]

    # Sample data for Kids
    kids_sizes = [
        ('Kids', '2-4Y', 90, 105, 12, 18),
        ('Kids', '4-6Y', 105, 115, 18, 24),
        ('Kids', '6-8Y', 115, 125, 24, 30),
        ('Kids', '8-10Y', 125, 135, 30, 38),
        ('Kids', '10-12Y', 135, 150, 38, 48),
    ]
    
    all_data = men_sizes + women_sizes + kids_sizes
    
    for gender, size, min_h, max_h, min_w, max_w in all_data:
        db.session.add(SizeChart(
            gender=gender, 
            size=size, 
            min_height=min_h, 
            max_height=max_h, 
            min_weight=min_w, 
            max_weight=max_w
        ))
    db.session.commit()

with app.app_context():
    db.create_all()
    seed_size_chart()

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
        
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
        
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'success': False, 'message': 'All fields are required'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'success': False, 'message': 'Username already exists'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'message': 'Email already exists'}), 400

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Signup successful!'})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
        
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password are required'}), 400
    
    user = User.query.filter_by(username=username, password=password).first()
    
    if user:
        return jsonify({
            'success': True, 
            'message': f'Welcome back, {username}!', 
            'username': user.username,
            'email': user.email,
            'phone': user.phone or '',
            'address': user.address or ''
        })
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/orders')
def orders():
    return render_template('orders.html')

@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/api/profile/update', methods=['POST'])
def update_profile():
    data = request.get_json()
    username = data.get('username')
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404
        
    user.email = data.get('email', user.email)
    user.phone = data.get('phone', user.phone)
    user.address = data.get('address', user.address)
    
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': 'Profile updated successfully!',
        'user': {
            'username': user.username,
            'email': user.email,
            'phone': user.phone,
            'address': user.address
        }
    })

@app.route('/sizely', methods=['GET', 'POST'])
def sizely():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
            
        gender = data.get('gender')
        height = float(data.get('height', 0))
        weight = float(data.get('weight', 0))
        
        # Recommendation logic
        # First filter by gender
        potential_sizes = SizeChart.query.filter_by(gender=gender).all()
        
        best_size = None
        # Simple algorithm: find size where height and weight fall within range
        for s in potential_sizes:
            if s.min_height <= height <= s.max_height and s.min_weight <= weight <= s.max_weight:
                best_size = s.size
                break
        
        # If no exact match, find closest by weighted distance (height has more weight usually)
        if not best_size and potential_sizes:
            min_dist = float('inf')
            for s in potential_sizes:
                # Normalize height and weight diffs
                h_diff = min(abs(height - s.min_height), abs(height - s.max_height)) if not (s.min_height <= height <= s.max_height) else 0
                w_diff = min(abs(weight - s.min_weight), abs(weight - s.max_weight)) if not (s.min_weight <= weight <= s.max_weight) else 0
                
                dist = h_diff + (w_diff * 2) # Weight usually matters more in modern brands for fit
                if dist < min_dist:
                    min_dist = dist
                    best_size = s.size

        if request.is_json:
            return jsonify({'success': True, 'recommended_size': best_size})
        return render_template('sizely.html', recommended_size=best_size)

    return render_template('sizely.html')

import os
from werkzeug.utils import secure_filename
from utils.ai_overlay import overlay_clothing

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/lookly')
def lookly():
    # Provide some sample clothing items for the virtual try-on
    clothing_options = [
        {'id': 'c1', 'name': 'Amani Aurelia Linen Wrap Dress', 'image': 'images/card 01.png'},
        {'id': 'c2', 'name': 'Mens Casual Polo', 'image': 'images/card 02.png'},
        {'id': 'c3', 'name': 'Classic White Shirt', 'image': 'images/card 03.png'}
    ]
    return render_template('lookly.html', clothing_options=clothing_options)

@app.route('/api/try-on', methods=['POST'])
def try_on_api():
    if 'user_image' not in request.files:
        return jsonify({'success': False, 'message': 'No image uploaded'}), 400
        
    file = request.files['user_image']
    clothing_id = request.form.get('clothing_id')
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'}), 400
        
    if not clothing_id:
        return jsonify({'success': False, 'message': 'No clothing item selected'}), 400

    if file:
        # Save user image
        filename = secure_filename(file.filename)
        user_img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(user_img_path)
        
        # Determine clothing image path based on ID (simplified for demo)
        clothing_mapping = {
            'c1': 'static/images/card 01.png',
            'c2': 'static/images/card 02.png',
            'c3': 'static/images/card 03.png'
        }
        
        clothing_img_path = clothing_mapping.get(clothing_id)
        if not clothing_img_path or not os.path.exists(clothing_img_path):
             return jsonify({'success': False, 'message': 'Invalid clothing item selected'}), 400

        # Define output path
        output_filename = f"result_{filename}"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Run AI Overlay
        success, result_message = overlay_clothing(user_img_path, clothing_img_path, output_path)
        
        if success:
            # Return relative path for frontend rendering
            return jsonify({
                'success': True, 
                'result_url': f"/{UPLOAD_FOLDER}/{output_filename}"
            })
        else:
            return jsonify({'success': False, 'message': result_message}), 400

if __name__ == "__main__":
    app.run(debug=True)
