document.addEventListener('DOMContentLoaded', () => {

    // Очистка корзины по кнопке
    document.getElementById('cart-sidebar').addEventListener('click', async e => {
        if (e.target.classList.contains('clear-cart')) {
            try {
                const response = await fetch(CART_CLEAR_URL, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': CSRF_TOKEN,
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                });
                if (!response.ok) throw new Error('Ошибка очистки корзины');
                const data = await response.json();
                document.getElementById('cart-sidebar').innerHTML = data.cart_html;
            } catch (error) {
                alert(error.message);
            }
        }
    });
});