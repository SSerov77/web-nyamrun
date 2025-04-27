// Создание модалки
export function createModal(modalContainer, itemData, onAddCallback) {
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

    // Кнопка добавления
    const addBtn = modal.querySelector('.add-btn');
    addBtn.onclick = () => {
        const quantity = qtyInput.value;
        const checkedOptions = [...modal.querySelectorAll('input[name="option"]:checked')].map(i => i.value);
        onAddCallback(quantity, checkedOptions);
    };
}