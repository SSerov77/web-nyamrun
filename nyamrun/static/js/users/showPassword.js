document.addEventListener('DOMContentLoaded', function () {
    const passwordFields = document.querySelectorAll('input[type="password"], input[type="text"][name*="password"]');

    passwordFields.forEach(field => {
        const wrapper = document.createElement('div');
        wrapper.className = 'password-field';
        field.parentNode.insertBefore(wrapper, field);
        wrapper.appendChild(field);

        const toggle = document.createElement('span');
        toggle.className = 'password-toggle';
        toggle.innerHTML = '<i class="far fa-eye"></i>';
        wrapper.appendChild(toggle);

        toggle.addEventListener('click', function () {
            if (field.type === 'password') {
                field.type = 'text';
                toggle.innerHTML = '<i class="far fa-eye-slash"></i>';
            } else {
                field.type = 'password';
                toggle.innerHTML = '<i class="far fa-eye"></i>';
            }
        });
    });
});