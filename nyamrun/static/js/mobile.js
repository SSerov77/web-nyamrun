// JavaScript для мобильного бургер-меню
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('mobile-menu');
    const navbar = document.querySelector('.navbar');
    const body = document.body;
    
    // Создаем оверлей для закрытия меню
    const overlay = document.createElement('div');
    overlay.className = 'menu-overlay';
    body.appendChild(overlay);
    
    // Функция открытия/закрытия меню
    function toggleMenu() {
        const isActive = navbar.classList.contains('active');
        
        if (isActive) {
            closeMenu();
        } else {
            openMenu();
        }
    }
    
    // Функция открытия меню
    function openMenu() {
        navbar.classList.add('active');
        menuToggle.classList.add('active');
        overlay.classList.add('active');
        body.style.overflow = 'hidden'; // Отключаем скролл страницы
    }
    
    // Функция закрытия меню
    function closeMenu() {
        navbar.classList.remove('active');
        menuToggle.classList.remove('active');
        overlay.classList.remove('active');
        body.style.overflow = ''; // Включаем скролл страницы
    }
    
    // Обработчик клика по бургер-меню
    menuToggle.addEventListener('click', toggleMenu);
    
    // Закрытие меню при клике на оверлей
    overlay.addEventListener('click', closeMenu);
    
    // Закрытие меню при клике на ссылки внутри меню
    const navLinks = navbar.querySelectorAll('a');
    navLinks.forEach(link => {
        link.addEventListener('click', closeMenu);
    });
    
    // Закрытие меню при нажатии Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && navbar.classList.contains('active')) {
            closeMenu();
        }
    });
    
    // Закрытие меню при изменении размера окна (если переключились на десктоп)
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768 && navbar.classList.contains('active')) {
            closeMenu();
        }
    });
    
    // Обработка свайпов для мобильных устройств
    let touchStartX = 0;
    let touchEndX = 0;
    
    navbar.addEventListener('touchstart', function(e) {
        touchStartX = e.changedTouches[0].screenX;
    });
    
    navbar.addEventListener('touchend', function(e) {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    });
    
    function handleSwipe() {
        const swipeThreshold = 50;
        const diff = touchStartX - touchEndX;
        
        // Свайп влево для закрытия меню
        if (diff > swipeThreshold && navbar.classList.contains('active')) {
            closeMenu();
        }
    }
    
    // Улучшенная доступность
    menuToggle.setAttribute('aria-label', 'Открыть меню');
    menuToggle.setAttribute('aria-expanded', 'false');
    
    // Обновляем атрибуты доступности при открытии/закрытии
    const originalToggle = toggleMenu;
    toggleMenu = function() {
        originalToggle();
        const isActive = navbar.classList.contains('active');
        menuToggle.setAttribute('aria-expanded', isActive.toString());
        menuToggle.setAttribute('aria-label', isActive ? 'Закрыть меню' : 'Открыть меню');
    };
});