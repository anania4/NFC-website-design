/* ==================== SHOPPING CART LOGIC ==================== */

// State
let cart = JSON.parse(localStorage.getItem('tap_cart')) || [];

// DOM Elements (Cached lazily in functions to ensure load)
const getCartDrawer = () => document.querySelector('.cart-drawer');
const getCartOverlay = () => document.querySelector('.cart-overlay');
const getCartBody = () => document.querySelector('.cart-body');
const getCartCount = () => document.querySelector('.cart-count');
const getCartSubtotal = () => document.querySelector('.cart-subtotal span:last-child');

// Init
document.addEventListener('DOMContentLoaded', () => {
    updateCartUI();
});

// Toggle Drawer
function toggleCart() {
    const drawer = getCartDrawer();
    const overlay = getCartOverlay();
    if (drawer && overlay) {
        drawer.classList.toggle('open');
        overlay.classList.toggle('open');
    }
}

// Add Item
function addToCart(id, name, price, image) {
    const existingItem = cart.find(item => item.id === id);

    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id,
            name,
            price,
            image,
            quantity: 1
        });
    }

    saveCart();
    updateCartUI();

    // Open cart to show user
    const drawer = getCartDrawer();
    if (drawer && !drawer.classList.contains('open')) {
        toggleCart();
    }
}

// Remove Item
function removeFromCart(id) {
    cart = cart.filter(item => item.id !== id);
    saveCart();
    updateCartUI();
}

// Change Quantity
function updateQuantity(id, change) {
    const item = cart.find(item => item.id === id);
    if (item) {
        item.quantity += change;
        if (item.quantity <= 0) {
            removeFromCart(id);
        } else {
            saveCart();
            updateCartUI();
        }
    }
}

// Save to LocalStorage
function saveCart() {
    localStorage.setItem('tap_cart', JSON.stringify(cart));
}

// Update UI
function updateCartUI() {
    const cartBody = getCartBody();
    const cartCount = getCartCount();
    const subtotalEl = getCartSubtotal();

    if (!cartBody) return;

    // Update Count
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    if (cartCount) cartCount.textContent = totalItems;

    // Render Items
    if (cart.length === 0) {
        cartBody.innerHTML = `
            <div class="empty-cart-icon">🛒</div>
            <div class="empty-cart-msg">Your cart is empty</div>
        `;
        if (subtotalEl) subtotalEl.textContent = '$0.00';
    } else {
        cartBody.innerHTML = cart.map(item => `
            <div class="cart-item">
                <img src="${item.image}" alt="${item.name}">
                <div class="cart-item-details">
                    <h4>${item.name}</h4>
                    <p>$${item.price.toFixed(2)}</p>
                    <div class="cart-item-controls">
                        <button onclick="updateQuantity('${item.id}', -1)">-</button>
                        <span>${item.quantity}</span>
                        <button onclick="updateQuantity('${item.id}', 1)">+</button>
                    </div>
                </div>
                <div class="cart-item-remove" onclick="removeFromCart('${item.id}')">×</div>
            </div>
        `).join('');

        // Calculate Subtotal
        const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        if (subtotalEl) subtotalEl.textContent = `$${total.toFixed(2)}`;
    }
}

// Checkout Flow
function checkout() {
    if (cart.length === 0) {
        alert('Your cart is empty!');
        return;
    }
    window.location.href = 'checkout.html';
}
