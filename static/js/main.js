let currentSlide = 0;
const wrapper = document.getElementById('carouselWrapper');
const slides = document.querySelectorAll('.carousel-slide');
const totalSlides = slides ? slides.length : 0;
const dotsContainer = document.getElementById('dotsContainer');
let autoSlideInterval;
let wishlistCount = 0;
let cartCount = 0;

function updateBadges() {
    const wishlistBadge = document.getElementById('wishlist-badge');
    const cartBadge = document.getElementById('cart-badge');

    if (wishlistBadge) {
        wishlistBadge.classList.toggle('active', wishlistCount > 0);
        wishlistBadge.textContent = wishlistCount > 0 ? wishlistCount : '';
    }

    if (cartBadge) {
        cartBadge.classList.toggle('active', cartCount > 0);
        cartBadge.textContent = cartCount > 0 ? cartCount : '';
    }
}

function toggleTheme() {
    const isDark = document.documentElement.classList.toggle('dark-mode');
    localStorage.setItem('lomiees_theme', isDark ? 'dark' : 'light');

    // Update icon
    const themeIcon = document.querySelector('#themeToggle i');
    if (themeIcon) {
        if (isDark) {
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
        } else {
            themeIcon.classList.remove('fa-sun');
            themeIcon.classList.add('fa-moon');
        }
    }
}

// Set initial icon state on load
document.addEventListener('DOMContentLoaded', () => {
    const theme = localStorage.getItem('lomiees_theme');
    const themeIcon = document.querySelector('#themeToggle i');
    if (theme === 'dark' && themeIcon) {
        themeIcon.classList.remove('fa-moon');
        themeIcon.classList.add('fa-sun');
    }
});

// Create dots
if (dotsContainer && totalSlides > 0) {
    for (let i = 0; i < totalSlides; i++) {
        const dot = document.createElement('div');
        dot.className = 'dot';
        if (i === 0) dot.classList.add('active');
        dot.onclick = () => goToSlide(i);
        dotsContainer.appendChild(dot);
    }
}

const dots = document.querySelectorAll('.dot');

function updateCarousel() {
    wrapper.style.transform = `translateX(-${currentSlide * 100}%)`;

    dots.forEach((dot, index) => {
        dot.classList.toggle('active', index === currentSlide);
    });
}

function moveSlide(direction) {
    currentSlide += direction;

    if (currentSlide >= totalSlides) {
        currentSlide = 0;
    } else if (currentSlide < 0) {
        currentSlide = totalSlides - 1;
    }

    updateCarousel();
    resetAutoSlide();
}

function goToSlide(index) {
    currentSlide = index;
    updateCarousel();
    resetAutoSlide();
}

function autoSlide() {
    moveSlide(1);
}

function startAutoSlide() {
    autoSlideInterval = setInterval(autoSlide, 3000); // Change slide every 3 seconds
}

function resetAutoSlide() {
    clearInterval(autoSlideInterval);
    startAutoSlide();
}

// Start automatic sliding
if (wrapper && totalSlides > 0) {
    startAutoSlide();

    // Pause on hover
    const container = document.querySelector('.carousel-container');
    if (container) {
        container.addEventListener('mouseenter', () => {
            clearInterval(autoSlideInterval);
        });

        container.addEventListener('mouseleave', () => {
            startAutoSlide();
        });
    }
}

const searchInput = document.querySelector('.search-container input');
if (searchInput) {
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            alert('Search functionality: ' + searchInput.value);
        }
    });
}

// Brand data with placeholder logos 
const brands = [
    { name: 'Zara', logo: '/static/images/zara.png' },
    { name: 'H&M', logo: '/static/images/hm.png' },
    { name: 'Nike', logo: '/static/images/nike.png' },
    { name: 'Adidas', logo: '/static/images/adidas.png' },
    { name: 'Gucci', logo: '/static/images/gucci.png' },
    { name: 'Prada', logo: '/static/images/prada.png' },
    { name: 'Versace', logo: '/static/images/versace.png' },
    { name: 'Dior', logo: '/static/images/dior.png' },
    { name: 'Louis Vuitton', logo: '/static/images/louisvuitton.png' },
    { name: 'Calvin Klein', logo: '/static/images/calvinklein.png' }
];

let currentBrandIndex = 0;
let brandsPerView = 4;

function updateBrandsPerView() {
    if (window.innerWidth <= 480) {
        brandsPerView = 1;
    } else if (window.innerWidth <= 768) {
        brandsPerView = 2;
    } else if (window.innerWidth <= 1200) {
        brandsPerView = 3;
    } else {
        brandsPerView = 4;
    }
}

function renderBrands() {
    const track = document.getElementById('brandsTrack');
    if (!track) return;
    // Duplicate brands for infinite scroll effect
    const duplicatedBrands = [...brands, ...brands, ...brands];
    track.innerHTML = duplicatedBrands.map(brand => `
                <div class="brand-card">
                    <img src="${brand.logo}" alt="${brand.name}" class="brand-logo">
                    <div class="brand-name">${brand.name}</div>
                </div>
            `).join('');
}

function startAutoScroll() {
    const track = document.getElementById('brandsTrack');
    if (!track || !track.children.length) return;
    let scrollPosition = 0;
    const speed = 1; // pixels per frame

    function scroll() {
        scrollPosition += speed;
        const cardWidth = track.children[0].offsetWidth;
        const gap = 30;
        const totalWidth = (cardWidth + gap) * brands.length;

        if (scrollPosition >= totalWidth) {
            scrollPosition = 0;
        }

        track.style.transform = `translateX(-${scrollPosition}px)`;
        requestAnimationFrame(scroll);
    }

    scroll();
}

// Initialized via DOMContentLoaded below

// Initialize
if (document.getElementById('brandsTrack')) {
    updateBrandsPerView();
    renderBrands();
    setTimeout(startAutoScroll, 100);
}

// Modern Reveal Animations
const revealCallback = (entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('active');
        }
    });
};

const revealObserver = new IntersectionObserver(revealCallback, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
});

const setupAnimations = () => {
    // Reveal Observer for all sections and reveal elements
    document.querySelectorAll('section, .reveal').forEach(el => {
        if (!el.classList.contains('brands-section')) {
            el.classList.add('reveal');
            revealObserver.observe(el);
        }
    });

    const productObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('active');
                }, index * 80);
                productObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.product-card').forEach(card => {
        card.classList.add('reveal');
        productObserver.observe(card);
    });
};

// Toast Notification System
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 9999;
        display: flex;
        flex-direction: column;
        gap: 10px;
    `;
    document.body.appendChild(container);
    return container;
}

const toastContainer = createToastContainer();

function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    const icon = type === 'success' ? '✓' : '♥';

    toast.style.cssText = `
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 12px 20px;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        color: #333;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 10px;
        transform: translateX(120%);
        transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        border-left: 4px solid ${type === 'success' ? '#b504a3' : '#ff3366'};
    `;

    toast.innerHTML = `
        <span style="background: ${type === 'success' ? '#b504a3' : '#ff3366'}; color: white; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px;">
            ${icon}
        </span>
        <span>${message}</span>
    `;

    toastContainer.appendChild(toast);

    requestAnimationFrame(() => {
        toast.style.transform = 'translateX(0)';
    });

    setTimeout(() => {
        toast.style.transform = 'translateX(140%)';
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 500);
    }, 3000);
}

// Initialize animations
setTimeout(setupAnimations, 300);

const products = [
    {
        id: 1,
        name: 'Amani Aurelia Linen Wrap Dress',
        brand: 'More Details',
        currentPrice: 'Rs.3400',
        image: '/static/images/card 01.png'
    },
    {
        id: 2,
        name: 'Mens Casual Polo T-shirt',
        brand: 'More Details',
        currentPrice: 'Rs.2890',
        image: '/static/images/card 02.png'
    },
    {
        id: 3,
        name: 'Sleeveless Linen Jumpsuit',
        brand: 'More Details',
        currentPrice: 'Rs.6530',
        image: '/static/images/card 03.png'
    },
    {
        id: 4,
        name: 'Sleeveless Frock',
        brand: 'More Details',
        currentPrice: 'Rs.2750',
        image: '/static/images/card 04.png'
    },
    {
        id: 5,
        name: 'Red Short Sleeve Party Wear',
        brand: 'More Details',
        currentPrice: 'Rs.11390',
        image: '/static/images/card 05.jpg'
    },
    {
        id: 6,
        name: 'Women Linen Office Pant',
        brand: 'More Details',
        currentPrice: 'Rs.2700',
        image: '/static/images/card 06.png'
    },
    {
        id: 7,
        name: 'Long Sleeve Mens White Shirt',
        brand: 'More Details',
        currentPrice: 'Rs.2700',
        image: '/static/images/card 07.jpg'
    },
    {
        id: 8,
        name: 'Short Sleeve Black Frock',
        brand: 'More Details',
        currentPrice: 'Rs.2400',
        image: '/static/images/card 08.jpg'
    }
];

function createProductCard(product) {
    return `
        <div class="product-card">
            <div class="image-container">
                <img src="${product.image}" alt="${product.name}" class="product-image">
                <button class="wishlist-btn red-heart" onclick="toggleWishlist(${product.id}, this)">
                    <i class="fas fa-heart"></i>
                </button>
                <div class="more-details-overlap">
                    <button class="more-details-btn" onclick="showProductDetails(${product.id})">
                        <i class="fas fa-shipping-fast"></i>
                        More Details
                    </button>
                </div>
            </div>
            <div class="product-details-section">
                <div class="product-name">${product.name}</div>
                <div class="product-footer">
                    <div class="product-price">${product.currentPrice}</div>
                    <button class="circular-cart-btn" onclick="addToCart(${product.id}, this)">
                        <i class="fas fa-shopping-cart"></i>
                    </button>
                </div>
            </div>
        </div>
    `;
}


// ===== MISSING FUNCTIONS =====

// Wishlist toggle
async function toggleWishlist(productId, btn) {
    const currentUser = JSON.parse(localStorage.getItem('lomiees_current_user'));
    if (!currentUser) {
        showToast('Please login to add to wishlist', 'error');
        openAuthDrawer();
        return;
    }

    try {
        const response = await fetch('/api/wishlist/toggle', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: currentUser.username,
                product_id: productId
            })
        });

        const data = await response.json();
        if (data.success) {
            const isAdded = data.status === 'added';
            btn.classList.toggle('active', isAdded);
            btn.style.background = isAdded ? '#ff0000' : 'white';
            btn.style.color = isAdded ? 'white' : '#ff0000';

            wishlistCount = data.wishlist_count;
            updateBadges();
            showToast(data.message, isAdded ? 'wishlist' : 'success');
        } else {
            showToast(data.message || 'Error updating wishlist', 'error');
        }
    } catch (error) {
        console.error('Wishlist error:', error);
        showToast('An error occurred', 'error');
    }
}

// Add to cart
async function addToCart(productId, btn) {
    const currentUser = JSON.parse(localStorage.getItem('lomiees_current_user'));
    if (!currentUser) {
        showToast('Please login to add to cart', 'error');
        openAuthDrawer();
        return;
    }

    btn.style.transform = 'scale(0.85) rotate(10deg)';
    setTimeout(() => { btn.style.transform = ''; }, 300);

    try {
        const response = await fetch('/api/cart/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: currentUser.username,
                product_id: productId
            })
        });

        const data = await response.json();
        if (data.success) {
            cartCount = data.cart_count;
            updateBadges();

            const product = products.find(p => p.id === productId);
            if (product) showToast(`"${product.name}" added to cart ✓`);
        } else {
            showToast(data.message || 'Error adding to cart', 'error');
        }
    } catch (error) {
        console.error('Cart error:', error);
        showToast('An error occurred', 'error');
    }
}

async function loadCounts() {
    const currentUser = JSON.parse(localStorage.getItem('lomiees_current_user'));
    if (!currentUser) {
        wishlistCount = 0;
        cartCount = 0;
        updateBadges();
        return;
    }

    try {
        const response = await fetch(`/api/counts?username=${currentUser.username}`);
        const data = await response.json();
        if (data.success) {
            wishlistCount = data.wishlist_count;
            cartCount = data.cart_count;
            updateBadges();
        }
    } catch (error) {
        console.error('Error loading counts:', error);
    }
}

async function removeFromCart(productId, callback) {
    const currentUser = JSON.parse(localStorage.getItem('lomiees_current_user'));
    if (!currentUser) return;

    try {
        const response = await fetch('/api/cart/remove', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: currentUser.username,
                product_id: productId
            })
        });

        const data = await response.json();
        if (data.success) {
            cartCount = data.cart_count;
            updateBadges();
            showToast('Removed from cart');
            if (callback) callback();
        }
    } catch (error) {
        console.error('Remove from cart error:', error);
    }
}

async function removeFromWishlist(productId, callback) {
    const currentUser = JSON.parse(localStorage.getItem('lomiees_current_user'));
    if (!currentUser) return;

    try {
        const response = await fetch('/api/wishlist/remove', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: currentUser.username,
                product_id: productId
            })
        });

        const data = await response.json();
        if (data.success) {
            wishlistCount = data.wishlist_count;
            updateBadges();
            showToast('Removed from wishlist');
            if (callback) callback();
        }
    } catch (error) {
        console.error('Remove from wishlist error:', error);
    }
}

// Show product details (placeholder)
function showProductDetails(productId) {
    const product = products.find(p => p.id === productId);
    if (product) showToast(`Viewing: ${product.name}`);
}

// Countdown timer for Exclusive Offer section
function startCountdown() {
    // Set target: 3 days from now
    const target = new Date();
    target.setDate(target.getDate() + 3);

    function tick() {
        const now = new Date();
        const diff = target - now;
        if (diff <= 0) return;

        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));

        const nums = document.querySelectorAll('.timer-number');
        if (nums.length >= 3) {
            nums[0].textContent = String(days).padStart(2, '0');
            nums[1].textContent = String(hours).padStart(2, '0');
            nums[2].textContent = String(minutes).padStart(2, '0');
        }
    }

    tick();
    setInterval(tick, 60000); // update every minute
}

document.addEventListener('DOMContentLoaded', () => {
    // 1. Header/Hero
    //initCarousel();
    //setupSearch();

    // 2. Brands
    updateBrandsPerView();
    renderBrands();
    const brandsContainer = document.querySelector('.brands-carousel-container');
    if (brandsContainer) {
        brandsContainer.addEventListener('mouseenter', () => {
            const track = document.getElementById('brandsTrack');
            if (track) track.style.animationPlayState = 'paused';
        });
        brandsContainer.addEventListener('mouseleave', () => {
            const track = document.getElementById('brandsTrack');
            if (track) track.style.animationPlayState = 'running';
        });
    }
    setTimeout(() => {
        const track = document.getElementById('brandsTrack');
        if (track && track.children.length > 0) startAutoScroll();
    }, 100);

    // 3. Products
    const productsGrid = document.getElementById('productsGrid');
    if (productsGrid) {
        productsGrid.innerHTML = products.map(createProductCard).join('');
    }

    // 4. Reveal Animations
    setupAnimations();

    // 5. Countdown Timer
    startCountdown();
});


function togglePasswordVisibility(inputId, icon) {
    const input = document.getElementById(inputId);
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// Authentication Drawer Functions
function openAuthDrawer() {
    const currentUser = JSON.parse(localStorage.getItem('lomiees_current_user'));

    // If logged in, redirect to full profile page instead of drawer
    if (currentUser) {
        window.location.href = '/profile';
        return;
    }

    const overlay = document.getElementById('authOverlay');
    const drawer = document.getElementById('authDrawer');
    if (overlay && drawer) {
        switchAuthMode('login'); // Default for guests
        overlay.classList.add('active');
        drawer.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeAuthDrawer() {
    const overlay = document.getElementById('authOverlay');
    const drawer = document.getElementById('authDrawer');
    if (overlay && drawer) {
        overlay.classList.remove('active');
        drawer.classList.remove('active');
        document.body.style.overflow = '';
    }
}

function switchAuthMode(mode) {
    const loginContainer = document.getElementById('loginFormContainer');
    const signupContainer = document.getElementById('signupFormContainer');
    const profileContainer = document.getElementById('userProfileContainer');

    // Hide all first
    loginContainer.classList.remove('active');
    signupContainer.classList.remove('active');
    if (profileContainer) profileContainer.classList.remove('active');

    // Show target
    if (mode === 'signup') {
        signupContainer.classList.add('active');
    } else if (mode === 'profile') {
        if (profileContainer) profileContainer.classList.add('active');
    } else {
        loginContainer.classList.add('active');
    }
}

// Authentication Logic
async function handleSignup(event) {
    event.preventDefault();

    const username = document.getElementById('signup-username').value.trim();
    const email = document.getElementById('signup-email').value.trim();
    const password = document.getElementById('signup-password').value;

    // Basic Validation
    if (!username || !email || !password) {
        showToast('Please fill in all fields', 'error');
        return;
    }

    if (password.length < 6) {
        showToast('Password must be at least 6 characters', 'error');
        return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        showToast('Please enter a valid email', 'error');
        return;
    }

    try {
        const response = await fetch('/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        if (data.success) {
            showToast('Signup successful! Please login.', 'success');
            document.getElementById('signupForm').reset();

            // If on dedicated signup page, scroll to top or redirect to login
            if (window.location.pathname === '/signup') {
                setTimeout(() => {
                    window.location.href = '/login';
                }, 1500);
            } else {
                switchAuthMode('login');
            }
        } else {
            showToast(data.message || 'Signup failed', 'error');
        }
    } catch (error) {
        showToast('An error occurred. Please try again.', 'error');
        console.error('Signup error:', error);
    }
}

async function handleLogin(event) {
    event.preventDefault();

    const username = document.getElementById('login-username').value.trim();
    const password = document.getElementById('login-password').value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (data.success) {
            showToast(data.message, 'success');

            // Save current user session locally for UI persistence
            localStorage.setItem('lomiees_current_user', JSON.stringify({
                username: data.username,
                email: data.email
            }));

            updateUserUI();

            setTimeout(() => {
                const loginForm = document.getElementById('loginForm');
                if (loginForm) loginForm.reset();

                // If on dedicated login page, redirect to home or profile
                if (window.location.pathname === '/login') {
                    window.location.href = '/';
                } else {
                    closeAuthDrawer();
                    window.location.reload(); // Refresh to apply changes globally
                }
            }, 1000);
        } else {
            showToast(data.message || 'Invalid username or password', 'error');
        }
    } catch (error) {
        showToast('An error occurred. Please try again.', 'error');
        console.error('Login error:', error);
    }
}

function updateUserUI() {
    const currentUser = JSON.parse(localStorage.getItem('lomiees_current_user'));
    const profileIconLink = document.getElementById('profile-icon');

    if (currentUser && profileIconLink) {
        const firstLetter = currentUser.username.charAt(0).toUpperCase();
        profileIconLink.innerHTML = `<span class="user-avatar">${firstLetter}</span>`;
        profileIconLink.onclick = null; // Remove the drawer opener
        profileIconLink.setAttribute('href', '/profile'); // Make it go to profile directly

        // Populate Profile Card in Drawer
        const largeAvatar = document.getElementById('profileLargeAvatar');
        const usernameDisplay = document.getElementById('profileUsernameDisplay');
        const emailDisplay = document.getElementById('profileEmailDisplay');

        if (largeAvatar) largeAvatar.textContent = firstLetter;
        if (usernameDisplay) usernameDisplay.textContent = currentUser.username;
        if (emailDisplay) emailDisplay.textContent = currentUser.email || 'Member';
    } else if (profileIconLink) {
        profileIconLink.innerHTML = `<i class="fa-solid fa-user"></i>`;
        profileIconLink.onclick = openAuthDrawer;
        profileIconLink.setAttribute('href', 'javascript:void(0)');
    }
}

function handleLogout() {
    console.log("Logging out...");
    localStorage.removeItem('lomiees_current_user');
    updateUserUI(); // Reset the icon immediately
    showToast('Logged out successfully', 'success');

    setTimeout(() => {
        if (typeof closeAuthDrawer === 'function') closeAuthDrawer();
        window.location.replace('/');
    }, 500);
}

// Initializations
document.addEventListener('DOMContentLoaded', () => {
    // Check if other initializations exist elsewhere, if not add them here
    updateUserUI();
    loadCounts();
    applyCurrencyConversion();
});

function applyCurrencyConversion() {
    const targetCurrency = localStorage.getItem('lomiees_currency') || 'LKR';
    if (targetCurrency === 'LKR') return; // Default, no action needed

    const rates = {
        'USD': { rate: 0.0033, symbol: '$' },     // Approx Rs. 300 = $1
        'EUR': { rate: 0.0030, symbol: '€' },
        'GBP': { rate: 0.0026, symbol: '£' }
    };

    const conversion = rates[targetCurrency];
    if (!conversion) return;

    // Target elements containing prices
    const priceElements = document.querySelectorAll('.item-price-tag, .product-price');

    priceElements.forEach(el => {
        const text = el.innerText;
        // Look for "Rs." followed by numbers and optional commas
        if (text.includes('Rs.')) {
            // Extract the number
            const numberStr = text.replace(/Rs\.?/g, '').replace(/,/g, '').trim();
            const numericValue = parseFloat(numberStr);

            if (!isNaN(numericValue)) {
                const convertedValue = (numericValue * conversion.rate).toFixed(2);
                // Format with commas and new symbol
                const formattedValue = parseFloat(convertedValue).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
                el.innerText = `${conversion.symbol} ${formattedValue}`;
            }
        }
    });
}
