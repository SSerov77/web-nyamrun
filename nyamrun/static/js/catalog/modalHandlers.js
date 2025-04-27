import { getCookie } from './utils.js';
import { createModal } from './modal.js';

export function setupModalButtons(modalContainer) {

    document.querySelectorAll('.open-modal-btn').forEach(button => {
        button.addEventListener('click', async () => {
            const modalUrl = button.dataset.modalUrl;
            try {
                const response = await fetch(modalUrl, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                });

                if (!response.ok) {
                    const text = await response.text();
                    throw new Error(`Ошибка загрузки данных товара: ${response.status} ${text}`);
                }

                const data = await response.json();

                // callback который вызывается при добавлении в корзину
                const onAddCallback = async (quantity, options) => {
                    const csrfToken = getCookie('csrftoken');
                    const formData = new FormData();
                    formData.append('quantity', quantity);
                    options.forEach(optId => formData.append('options', optId));

                    try {
                        const addResponse = await fetch(data.add_url, {
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrfToken,
                                'X-Requested-With': 'XMLHttpRequest',
                            },
                            body: formData,
                        });

                        if (!addResponse.ok) {
                            const text = await addResponse.text();
                            throw new Error(`Ошибка при добавлении товара в корзину:\n${text}`);
                        }

                        const addData = await addResponse.json();
                        document.getElementById('cart-sidebar').innerHTML = addData.cart_html;

                        // Закрыть модалку
                        modalContainer.style.display = 'none';
                        modalContainer.innerHTML = '';

                    } catch (error) {
                        alert(error.message);
                    }
                };

                createModal(modalContainer, data, onAddCallback);

            } catch (error) {
                alert(error.message);
            }
        });
    });
}