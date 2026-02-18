let currentSlide = 0;
const wrapper = document.getElementById('carouselWrapper');
const slides = document.querySelectorAll('.carousel-slide');
const totalSlides = slides.length;
const dotsContainer = document.getElementById('dotsContainer');
let autoSlideInterval;

// Create dots
for (let i = 0; i < totalSlides; i++) {
    const dot = document.createElement('div');
    dot.className = 'dot';
    if (i === 0) dot.classList.add('active');
    dot.onclick = () => goToSlide(i);
    dotsContainer.appendChild(dot);
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
startAutoSlide();

// Pause on hover
const container = document.querySelector('.carousel-container');
container.addEventListener('mouseenter', () => {
    clearInterval(autoSlideInterval);
});

container.addEventListener('mouseleave', () => {
    startAutoSlide();
});

const searchInput = document.querySelector('.search-container input');
searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        alert('Search functionality: ' + searchInput.value);
    }
});

// Brand data with placeholder logos 
const brands = [
    { name: 'Zara', logo: 'images/zara.png' },
    { name: 'H&M', logo: 'images/hm.png' },
    { name: 'Nike', logo: 'images/nike.png' },
    { name: 'Adidas', logo: 'images/adidas.png' },
    { name: 'Gucci', logo: 'images/gucci.png' },
    { name: 'Prada', logo: 'images/prada.png' },
    { name: 'Versace', logo: 'images/versace.png' },
    { name: 'Dior', logo: 'images/dior.png' },
    { name: 'Louis Vuitton', logo: 'images/louisvuitton.png' },
    { name: 'Calvin Klein', logo: 'images/calvinklein.png' }
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
updateBrandsPerView();
renderBrands();
setTimeout(startAutoScroll, 100);

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
        image: 'images/card 01.png'
    },
    {
        id: 2,
        name: 'Mens Casual Polo T-shirt',
        brand: 'More Details',
        currentPrice: 'Rs.2890',
        image: 'images/card 02.png'
    },
    {
        id: 3,
        name: 'Sleeveless Linen Jumpsuit',
        brand: 'More Details',
        currentPrice: 'Rs.6530',
        image: 'images/card 03.png'
    },
    {
        id: 4,
        name: 'Sleeveless Frock',
        brand: 'More Details',
        currentPrice: 'Rs.2750',
        image: 'images/card 04.png'
    },
    {
        id: 5,
        name: 'Red Short Sleeve Party Wear',
        brand: 'More Details',
        currentPrice: 'Rs.11390',
        image: 'images/card 05.jpg'
    },
    {
        id: 6,
        name: 'Women Linen Office Pant',
        brand: 'More Details',
        currentPrice: 'Rs.2700',
        image: 'images/card 06.png'
    },
    {
        id: 7,
        name: 'Long Sleeve Mens White Shirt',
        brand: 'More Details',
        currentPrice: 'Rs.2700',
        image: 'images/card 07.jpg'
    },
    {
        id: 8,
        name: 'Short Sleeve Black Frock',
        brand: 'More Details',
        currentPrice: 'Rs.2400',
        image: 'images/card 08.jpg'
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

    // 5. Features/Countdown
    startCountdown();
});
