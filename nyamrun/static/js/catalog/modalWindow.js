document.addEventListener('DOMContentLoaded', () => {
    const modalContainer = document.getElementById('modal-container');

    // Вспомогательная функция получения CSRF из cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Функция создания модального окна
    function createModal(itemData) {
        const optionsHtml = (itemData.options.length > 0) ? itemData.options.map(opt => `
      <label>
        <input type="checkbox" name="option" value="${opt.id}" />
        ${opt.name} (+${opt.additional_price}₽)
      </label><br/>
    `).join('') : `<p>К этому товару дополнительно ничего не идет</p>`;

        modalContainer.innerHTML = `
      <div class="modal-overlay">
        <div class="modal-window" role="dialog" aria-modal="true" aria-labelledby="modal-title">
          <button class="modal-close" aria-label="Закрыть">&times;</button>
          <div class="modal-content">
            <div class="modal-left">
              <img src="${itemData.image_url}" alt="${itemData.name}" />
            </div>
            <div class="modal-right">
              <h2 id="modal-title">${itemData.name}</h2>
              <div class="price-qty">
                <div class="price">${itemData.price}₽</div>
                <div class="quantity">
                  <button class="qty-btn" aria-label="Уменьшить">−</button>
                  <input type="number" min="1" value="1" />
                  <button class="qty-btn" aria-label="Увеличить">+</button>
                </div>
                <button class="add-btn">Добавить</button>
              </div>
              <div class="options" style="border-top: 1px solid #d4d4d4; padding-top: 20px;">
                <h4>Опции</h4>
                ${optionsHtml}
              </div>
            </div>
          </div>
          <div class="modal-description">
            <p>${itemData.description || ''}</p>
          </div>
        </div>
      </div>
    `;

        modalContainer.style.display = "block";

        const modal = modalContainer.querySelector('.modal-window');

        // Кнопки изменения количества
        const minusBtn = modal.querySelector('.qty-btn:first-child');
        const plusBtn = modal.querySelector('.qty-btn:last-child');
        const qtyInput = modal.querySelector('input[type="number"]');

        minusBtn.addEventListener('click', () => {
            let val = parseInt(qtyInput.value, 10);
            if (val > 1) qtyInput.value = val - 1;
        });

        plusBtn.addEventListener('click', () => {
            let val = parseInt(qtyInput.value, 10);
            qtyInput.value = val + 1;
        });

        // Закрытие модалки
        modal.querySelector('.modal-close').addEventListener('click', () => {
            modalContainer.style.display = 'none';
            modalContainer.innerHTML = '';
        });

        // Добавление в корзину через AJAX
        modal.querySelector('.add-btn').addEventListener('click', async () => {
            const quantity = qtyInput.value;
            const checkedOptions = [...modal.querySelectorAll('input[name="option"]:checked')].map(i => i.value);

            const csrfToken = getCookie('csrftoken');
            const formData = new FormData();
            formData.append('quantity', quantity);
            checkedOptions.forEach(optId => formData.append('options', optId));

            try {
                const response = await fetch(itemData.add_url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    body: formData,
                });

                if (!response.ok) {
                    const text = await response.text();
                    throw new Error(`Ошибка при добавлении товара в корзину:\n${text}`);
                }

                const data = await response.json();
                document.getElementById('cart-sidebar').innerHTML = data.cart_html;

                // Закрываем модалку
                modalContainer.style.display = 'none';
                modalContainer.innerHTML = '';

            } catch (error) {
                alert(error.message);
            }
        });
    }

    // Обработка кнопок открытия модалки
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
                createModal(data);
            } catch (error) {
                alert(error.message);
            }
        });
    });
});