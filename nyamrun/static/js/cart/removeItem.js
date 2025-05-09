document.addEventListener('DOMContentLoaded', () => {
    // Удаление товара из корзины
    document.getElementById('cart-sidebar').addEventListener('click', async e => {
        if (e.target.classList.contains('remove-item')) {
            const itemId = e.target.dataset.itemId;
            try {
                const response = await fetch(`/cart/remove-ajax/${itemId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': CSRF_TOKEN,
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                });
                if (!response.ok) throw new Error('Ошибка удаления товара');
                const data = await response.json();
                document.getElementById('cart-sidebar').innerHTML = data.cart_html;
            } catch (error) {
                alert(error.message);
            }
        }
    });
}); 