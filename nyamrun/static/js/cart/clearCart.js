document.addEventListener('DOMContentLoaded', () => {
    const csrftoken = getCookie('csrftoken');

    document.getElementById('cart-sidebar').addEventListener('click', async e => {
        if (e.target.classList.contains('clear-cart')) {
            try {
                const response = await fetch(CART_CLEAR_URL, {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrftoken,
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

    function getCookie(name) {
        const cookies = document.cookie
            .split(';')
            .map(c => c.trim().split('='));
        const match = cookies.find(([key]) => key === name);
        return match ? decodeURIComponent(match[1]) : null;
    }
});
