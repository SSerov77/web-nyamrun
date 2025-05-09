import { setupModalButtons } from './modalHandlers.js';
import { getCookie } from './utils.js';

document.addEventListener('DOMContentLoaded', () => {
    const modalContainer = document.getElementById('modal-container');
    setupModalButtons(modalContainer);

    // Cart quantity change logic
    document.getElementById('cart-sidebar').addEventListener('click', async (e) => {
        if (e.target.classList.contains('cart-qty-btn')) {
            const btn = e.target;
            const itemId = btn.dataset.itemId;
            const qtySpan = btn.parentElement.querySelector('.cart-item-qty');
            let currentQty = parseInt(qtySpan.textContent, 10);
            let newQty = currentQty;
            if (btn.classList.contains('plus')) {
                newQty = currentQty + 1;
            } else if (btn.classList.contains('minus')) {
                newQty = currentQty - 1;
            }
            if (newQty <= 0) {
                // Remove item from cart
                const response = await fetch(`/cart/remove-ajax/${itemId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                });
                if (response.ok) {
                    const data = await response.json();
                    document.getElementById('cart-sidebar').innerHTML = data.cart_html;
                } else {
                    alert('Ошибка удаления товара из корзины');
                }
            } else {
                // Update item quantity (need backend endpoint)
                const formData = new FormData();
                formData.append('quantity', newQty);
                const response = await fetch(`/cart/update-ajax/${itemId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    body: formData,
                });
                if (response.ok) {
                    const data = await response.json();
                    document.getElementById('cart-sidebar').innerHTML = data.cart_html;
                } else {
                    alert('Ошибка обновления количества товара');
                }
            }
        }
    });
});