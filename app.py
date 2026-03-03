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

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    size = db.Column(db.String(20), nullable=True) # Added size support
    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))

class WishlistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref=db.backref('wishlist_items', lazy=True))

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

@app.route('/cart')
def cart_page():
    return render_template('cart.html')

@app.route('/wishlist')
def wishlist_page():
    return render_template('wishlist.html')

@app.route('/checkout')
def checkout_page():
    return render_template('checkout.html')

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

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    username = data.get('username')
    product_id = data.get('product_id')
    size = data.get('size') # Optional size
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'message': 'User not found. Please login.'}), 401
    
    # Unique combination of (user, product, size)
    item = CartItem.query.filter_by(user_id=user.id, product_id=product_id, size=size).first()
    if not item:
        new_item = CartItem(user_id=user.id, product_id=product_id, size=size)
        db.session.add(new_item)
    
    db.session.commit()
    cart_count = CartItem.query.filter_by(user_id=user.id).count()
    return jsonify({'success': True, 'cart_count': cart_count})

@app.route('/api/wishlist/toggle', methods=['POST'])
def toggle_wishlist_api():
    data = request.get_json()
    username = data.get('username')
    product_id = data.get('product_id')
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'message': 'User not found. Please login.'}), 401
    
    item = WishlistItem.query.filter_by(user_id=user.id, product_id=product_id).first()
    if item:
        db.session.delete(item)
        message = 'Removed from Wishlist'
        status = 'removed'
    else:
        new_item = WishlistItem(user_id=user.id, product_id=product_id)
        db.session.add(new_item)
        message = 'Added to Wishlist'
        status = 'added'
        
    db.session.commit()
    wishlist_count = WishlistItem.query.filter_by(user_id=user.id).count()
    return jsonify({'success': True, 'message': message, 'status': status, 'wishlist_count': wishlist_count})

@app.route('/api/counts', methods=['GET'])
def get_counts():
    username = request.args.get('username')
    if not username:
        return jsonify({'success': False, 'cart_count': 0, 'wishlist_count': 0})
        
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'cart_count': 0, 'wishlist_count': 0})
        
    cart_count = CartItem.query.filter_by(user_id=user.id).count()
    wishlist_count = WishlistItem.query.filter_by(user_id=user.id).count()
    
    return jsonify({
        'success': True, 
        'cart_count': cart_count, 
        'wishlist_count': wishlist_count
    })

@app.route('/api/cart/remove', methods=['POST'])
def remove_from_cart():
    data = request.get_json()
    username = data.get('username')
    cart_item_id = data.get('cart_item_id') # Changed to specific item ID
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 401
    
    item = CartItem.query.filter_by(user_id=user.id, id=cart_item_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        
    cart_count = CartItem.query.filter_by(user_id=user.id).count()
    return jsonify({'success': True, 'cart_count': cart_count})

@app.route('/api/wishlist/remove', methods=['POST'])
def remove_from_wishlist():
    data = request.get_json()
    username = data.get('username')
    product_id = data.get('product_id')
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 401
    
    item = WishlistItem.query.filter_by(user_id=user.id, product_id=product_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
    
    wishlist_count = WishlistItem.query.filter_by(user_id=user.id).count()
    return jsonify({'success': True, 'wishlist_count': wishlist_count})

# Central product catalog — shared by all category routes and cart / wishlist API
ALL_PRODUCTS = [
    # ── WOMEN ──
    {'id': 1,  'name': 'Amani Aurelia Linen Wrap Dress',     'price': 3400,  'old_price': None,  'image': '/static/images/card 01.png',      'category': 'women',      'is_new': True,  'is_sale': False},
    {'id': 3,  'name': 'Sleeveless Linen Jumpsuit',           'price': 6530,  'old_price': None,  'image': '/static/images/card 03.png',      'category': 'women',      'is_new': False, 'is_sale': False},
    {'id': 5,  'name': 'Red Short Sleeve Party Wear',         'price': 8490,  'old_price': 11390, 'image': '/static/images/card 05.jpg',      'category': 'women',      'is_new': False, 'is_sale': True},
    {'id': 6,  'name': 'Women Linen Office Pant',             'price': 2700,  'old_price': None,  'image': '/static/images/card 06.png',      'category': 'women',      'is_new': False, 'is_sale': False},
    {'id': 8,  'name': 'Short Sleeve Black Frock',            'price': 2400,  'old_price': None,  'image': '/static/images/card 08.jpg',      'category': 'women',      'is_new': False, 'is_sale': False},
    {'id': 9,  'name': 'Floral Midi Wrap Skirt',              'price': 3150,  'old_price': None,  'image': 'https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=600&q=80', 'category': 'women', 'is_new': True,  'is_sale': False},
    {'id': 10, 'name': 'Elegant Off-Shoulder Evening Gown',   'price': 14500, 'old_price': 18900, 'image': 'https://images.unsplash.com/photo-1518611012118-696072aa579a?w=600&q=80', 'category': 'women', 'is_new': False, 'is_sale': True},
    {'id': 11, 'name': 'Cropped Linen Blazer',                'price': 5800,  'old_price': None,  'image': 'https://images.unsplash.com/photo-1487222477894-8943e31ef7b2?w=600&q=80', 'category': 'women', 'is_new': True,  'is_sale': False},
    {'id': 12, 'name': 'High-Waist Tailored Trousers',        'price': 4200,  'old_price': 5500,  'image': 'https://images.unsplash.com/photo-1509631179647-0177f2f1b5b5?w=600&q=80', 'category': 'women', 'is_new': False, 'is_sale': True},
    {'id': 13, 'name': 'Satin Slip Midi Dress',               'price': 7800,  'old_price': None,  'image': 'https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=600&q=80', 'category': 'women', 'is_new': True,  'is_sale': False},
    {'id': 14, 'name': 'Cotton Ruffle Puff-Sleeve Blouse',    'price': 2350,  'old_price': None,  'image': 'https://images.unsplash.com/photo-1464207687429-7505649dae38?w=600&q=80', 'category': 'women', 'is_new': False, 'is_sale': False},
    # ── MEN ──
    {'id': 2,  'name': 'Mens Casual Polo T-Shirt',            'price': 2190,  'old_price': 2890,  'image': '/static/images/card 02.png',      'category': 'men',        'is_new': False, 'is_sale': True},
    {'id': 7,  'name': 'Long Sleeve Classic White Shirt',     'price': 2700,  'old_price': None,  'image': '/static/images/card 07.jpg',      'category': 'men',        'is_new': True,  'is_sale': False},
    {'id': 15, 'name': 'Formal Slim-Fit Suit Shirt',          'price': 4500,  'old_price': None,  'image': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&q=80', 'category': 'men', 'is_new': True,  'is_sale': False},
    {'id': 16, 'name': 'Men Linen Relaxed Summer Shirt',      'price': 3200,  'old_price': 4100,  'image': 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=600&q=80', 'category': 'men', 'is_new': False, 'is_sale': True},
    {'id': 17, 'name': 'Graphic Print Oversized Tee',         'price': 1950,  'old_price': None,  'image': 'https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=600&q=80', 'category': 'men', 'is_new': True,  'is_sale': False},
    {'id': 18, 'name': 'Chino Stretch Jogger Pants',          'price': 3800,  'old_price': 5200,  'image': 'https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=600&q=80', 'category': 'men', 'is_new': False, 'is_sale': True},
    # ── KIDS ──
    {'id': 4,  'name': 'Sleeveless Floral Frock',             'price': 2750,  'old_price': None,  'image': '/static/images/card 04.png',      'category': 'kids',       'is_new': False, 'is_sale': False},
    {'id': 19, 'name': 'Kids Rainbow Dungaree Set',            'price': 3100,  'old_price': None,  'image': 'https://images.unsplash.com/photo-1532452119098-a3650b3c46d3?w=600&q=80', 'category': 'kids', 'is_new': True,  'is_sale': False},
    {'id': 20, 'name': 'Girls Puff-Sleeve Party Dress',       'price': 2600,  'old_price': 3400,  'image': 'https://images.unsplash.com/photo-1518831959646-742c3a14ebf0?w=600&q=80', 'category': 'kids', 'is_new': False, 'is_sale': True},
    {'id': 21, 'name': 'Boys Printed Tee & Shorts Set',       'price': 1890,  'old_price': None,  'image': 'https://images.unsplash.com/photo-1567880905822-56f8e06fe630?w=600&q=80', 'category': 'kids', 'is_new': True,  'is_sale': False},
    # ── JEWELLERY ──
    {'id': 22, 'name': 'Gold-Plated Floral Necklace Set',     'price': 4800,  'old_price': None,  'image': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=600&q=80', 'category': 'jewellery', 'is_new': True,  'is_sale': False},
    {'id': 23, 'name': 'Oxidised Silver Jhumka Earrings',     'price': 1950,  'old_price': 2800,  'image': 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=600&q=80', 'category': 'jewellery', 'is_new': False, 'is_sale': True},
    {'id': 24, 'name': 'Pearl Drop Statement Earrings',       'price': 2300,  'old_price': None,  'image': 'https://images.unsplash.com/photo-1576022162879-edf9d3b6f92c?w=600&q=80', 'category': 'jewellery', 'is_new': True,  'is_sale': False},
    {'id': 25, 'name': 'Rose Gold Bangle Stack Set',          'price': 3750,  'old_price': 5000,  'image': 'https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=600&q=80', 'category': 'jewellery', 'is_new': False, 'is_sale': True},
    # ── SHOES ──
    {'id': 26, 'name': 'Block Heel Leather Sandal',           'price': 5900,  'old_price': None,  'image': 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=600&q=80', 'category': 'shoes', 'is_new': True,  'is_sale': False},
    {'id': 27, 'name': 'White Canvas Platform Sneaker',       'price': 4200,  'old_price': 5800,  'image': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&q=80', 'category': 'shoes', 'is_new': False, 'is_sale': True},
    {'id': 28, 'name': 'Ankle Strap Stiletto Heel',           'price': 7500,  'old_price': None,  'image': 'https://images.unsplash.com/photo-1515347619252-60a4bf4fff4f?w=600&q=80', 'category': 'shoes', 'is_new': True,  'is_sale': False},
    {'id': 29, 'name': 'Mens Suede Slip-On Loafer',           'price': 6800,  'old_price': 8900,  'image': 'https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?w=600&q=80', 'category': 'shoes', 'is_new': False, 'is_sale': True},
    # ── ACCESSORIES ──
    {'id': 30, 'name': 'Quilted Chain Shoulder Bag',          'price': 8900,  'old_price': None,  'image': 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=600&q=80', 'category': 'accessories', 'is_new': True,  'is_sale': False},
    {'id': 31, 'name': 'Woven Straw Tote Bag',                'price': 3400,  'old_price': 4500,  'image': 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600&q=80', 'category': 'accessories', 'is_new': False, 'is_sale': True},
    {'id': 32, 'name': 'Classic Leather Crossbody Bag',       'price': 6500,  'old_price': None,  'image': 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600&q=80', 'category': 'accessories', 'is_new': True,  'is_sale': False},
]

def get_product_by_id(pid):
    return next((p for p in ALL_PRODUCTS if p['id'] == pid), None)

def get_all_products():
    return ALL_PRODUCTS


@app.route('/product/<int:product_id>')
def product_details(product_id):
    product = get_product_by_id(product_id)
    if not product:
        return "Product not found", 404
    
    # Related products (same category, excluding current)
    related = [p for p in ALL_PRODUCTS if p['category'] == product['category'] and p['id'] != product_id][:4]
    
    return render_template('product_details.html', product=product, related_products=related)

@app.route('/api/search')
def search_api():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])
    
    results = []
    for p in ALL_PRODUCTS:
        if query in p['name'].lower() or query in p['category'].lower():
            results.append({
                'id': p['id'],
                'name': p['name'],
                'price': p['price'],
                'image': p['image'],
                'category': p['category']
            })
    return jsonify(results[:8]) # Limit to 8 results for the dropdown

@app.route('/category/<name>')
def category_page(name):
    products = [p for p in get_all_products() if p['category'] == name.lower()]
    return render_template('category.html', category_name=name.capitalize(), products=products)

@app.route('/new-arrivals')
def new_arrivals():
    products = [p for p in get_all_products() if p.get('is_new')]
    return render_template('category.html', category_name='New Arrivals', products=products)

@app.route('/sale')
def sale_page():
    products = [p for p in get_all_products() if p.get('is_sale')]
    return render_template('category.html', category_name='Special Sale', products=products)

@app.route('/accessories')
def accessories_page():
    products = [p for p in get_all_products() if p['category'] == 'accessories']
    return render_template('category.html', category_name='Accessories', products=products)

@app.route('/jewellery')
def jewellery_page():
    products = [p for p in get_all_products() if p['category'] == 'jewellery']
    return render_template('category.html', category_name='Jewellery', products=products)

@app.route('/shoes')
def shoes_page():
    products = [p for p in get_all_products() if p['category'] == 'shoes']
    return render_template('category.html', category_name='Shoes', products=products)

@app.route('/api/cart', methods=['GET'])
def get_cart_items():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'items': []})
    
    items = []
    for ci in user.cart_items:
        product = get_product_by_id(ci.product_id)
        if product:
            items.append({
                'id': ci.product_id, # This is the product_id, not cart_item_id
                'cart_item_id': ci.id, # Added unique ID for quantity/remove ops
                'name': product['name'],
                'price': product['price'],
                'qty': ci.quantity,
                'size': ci.size,
                'image': product['image']
            })
    return jsonify({'success': True, 'items': items})

@app.route('/api/wishlist/items', methods=['GET'])
def get_wishlist_items():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'items': []})
    
    items = []
    for wi in user.wishlist_items:
        product = get_product_by_id(wi.product_id)
        if product:
            items.append({
                'id': wi.product_id,
                'name': product['name'],
                'price': product['price'],
                'image': product['image']
            })
    return jsonify({'success': True, 'items': items})

@app.route('/api/cart/update_qty', methods=['POST'])
def update_cart_qty():
    data = request.get_json()
    username = data.get('username')
    cart_item_id = data.get('cart_item_id') # Changed to specific item ID
    change = data.get('change') # +1 or -1
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 401
    
    item = CartItem.query.filter_by(user_id=user.id, id=cart_item_id).first()
    if item:
        item.quantity += change
        if item.quantity <= 0:
            db.session.delete(item)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Item not found'}), 404

if __name__ == "__main__":
    app.run(debug=True)
