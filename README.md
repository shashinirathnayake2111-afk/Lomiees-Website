# Lomiees: A Premium E-Commerce Experience

Lomiees is a modern, high-end e-commerce platform built with Flask and Vanilla JS. It features a sleek, purple-themed design with advanced shopping features like a size recommender and a virtual try-on engine.

## 🚀 Key Features

### 🛍️ Smart Shopping
- **Dynamic Cart**: Real-time quantity updates, subtotals, and seamless item removal.
- **Wishlist**: Save your favorite items to your profile with a single click.
- **Real-time Badges**: Notification dots on the header icons alert you when items are in your bag or wishlist.
- **Dark Mode**: Toggle between light and dark themes for a personalized viewing experience. Choice is persisted in your browser!

### 📐 Sizely: AI Size Recommender
- Input your gender, weight, and height to receive a personalized clothing size recommendation (XS-XXL) based on our precision size charts.

### 👗 Lookly: Virtual Try-On
- Upload a photo of yourself and select an item from our collection to see how it looks on you using our AI-powered overlay engine.

### 👤 User Accounts
- Secure signup and login system.
- Personalized dashboard with profile management and wishlists.

## 🛠️ Technology Stack
- **Backend**: Python 3.x, Flask, Flask-SQLAlchemy (SQLite)
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript (ES6+)
- **Icons**: Font Awesome 6.0+
- **Typography**: Google Fonts (Outfit, Inter, Fredoka)

## 🏁 Getting Started

### 1. Prerequisites
- Python 3.8+ installed on your system.

### 2. Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/shashinirathnayake2111-afk/Lomiees.git
   cd Lomiees
   ```
2. Install dependencies (create a virtual environment recommended):
   ```bash
   pip install flask flask-sqlalchemy opencv-python Pillow numpy
   ```

### 3. Running the App
Run the Flask server:
```bash
python app.py
```
Visit `http://127.0.0.1:5000` in your web browser.

## 📁 Project Structure
- `app.py`: Main Flask application and API endpoints.
- `templates/`: HTML structures and layouts.
- `static/css/`: Modular stylesheets for each page.
- `static/js/`: Frontend logic (animations, carousels, cart management).
- `static/images/`: Product photography and branding assets.
- `utils/`: AI and utility modules (Overlay Engine).

## � API Keys & Configuration
While the current version of Lomiees runs most AI features locally using MediaPipe and `rembg`, it is designed to be extensible.
- **Database**: Uses SQLite by default (`instance/database.db`).
- **Secret Keys**: Flask session keys and any future third-party APIs should be configured in an environment file or directly in `app.py` for development.

## 🛡️ Form Validations
We prioritize data integrity and user experience with a two-layer validation system:
- **Frontend**: HTML5 `required` attributes and custom JavaScript checks ensure that users provide valid usernames, emails, and passwords before submission.
- **Backend**: Flask-SQLAlchemy filters prevent duplicate usernames and emails, while ensuring all mandatory fields are present before database commits.

## 🌍 Multi-language Support
Lomiees is built for a global audience, featuring integrated translation support powered by Google Translate.
- **Supported Languages**: English, Sinhala (සිංහල), French (Français), and Spanish.
- **Implementation**: A discreet background script allows users to switch the entire site's interface into their preferred language, ensuring accessibility for both local and international shoppers.

## 🌙 Dark Mode
The website features a fully integrated Dark Mode that adapts the entire interface—from the header to the product cards and footer—for comfortable browsing in low-light environments.
- **Persistence**: Your theme preference is saved in `localStorage`, so the site remembers your choice the next time you visit.
- **UI Sync**: The toggle icon dynamically switches between moon and sun icons to reflect the current state.

## �📄 License
This project is for demonstration and portfolio purposes. All rights reserved.