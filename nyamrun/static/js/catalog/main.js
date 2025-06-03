import { setupModalButtons } from './modalHandlers.js';
import { getCookie } from './utils.js';

document.addEventListener('DOMContentLoaded', () => {
    setupModalButtons(document.getElementById('modal-container'));

    const csrftoken = getCookie('csrftoken');
    const defaultHeaders = {
        'X-CSRFToken': csrftoken,
        'X-Requested-With': 'XMLHttpRequest'
    };

    document.getElementById('cart-sidebar').addEventListener('click', async (e) => {
        if (!e.target.classList.contains('cart-qty-btn')) return;

        const btn = e.target;
        const itemId = btn.dataset.itemId;
        const qtyEl = btn.closest('.cart-item').querySelector('.cart-item-qty');
        let qty = parseInt(qtyEl.textContent, 10);
        let url, options;

        if (btn.classList.contains('plus')) {
            qty += 1;
        } else if (btn.classList.contains('minus')) {
            qty -= 1;
        }

        if (qty <= 0) {
            // удаляем товар
            url = `/cart/remove-ajax/${itemId}/`;
            options = {
                method: 'POST',
                credentials: 'include',
                headers: defaultHeaders
            };
        } else {
            // обновляем количество
            url = `/cart/update-ajax/${itemId}/`;
            const body = new FormData();
            body.append('quantity', qty);

            options = {
                method: 'POST',
                credentials: 'include',
                headers: defaultHeaders,
                body
            };
        }

        try {
            const resp = await fetch(url, options);
            if (!resp.ok) throw new Error('Ошибка обновления корзины');
            const data = await resp.json();
            document.getElementById('cart-sidebar').innerHTML = data.cart_html;
        } catch (err) {
            alert(err.message);
            console.error(err);
        }
    });
});
