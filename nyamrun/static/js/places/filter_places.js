document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('filter-form');
    const checkboxes = form.querySelectorAll('input[type=checkbox]');
    const container = document.getElementById('places-container');

    function getSelectedValues(name) {
        return Array.from(form.querySelectorAll(`input[name="${name}"]:checked`)).map(el => el.value);
    }

    async function updatePlaces() {
        const params = new URLSearchParams();

        // Добавление всех выбранных типов и кухни к параметрам
        getSelectedValues('type').forEach(val => params.append('type', val));
        getSelectedValues('cuisine').forEach(val => params.append('cuisine', val));

        try {
            const response = await fetch(`${form.action}?${params.toString()}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            if (!response.ok) throw new Error('Ошибка загрузки данных');

            const html = await response.text();
            container.innerHTML = html;
        } catch (err) {
            console.error(err);
        }
    }

    checkboxes.forEach(chk => {
        chk.addEventListener('change', () => {
            updatePlaces();
        });
    });
});