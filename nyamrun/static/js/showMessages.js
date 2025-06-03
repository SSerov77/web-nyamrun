// Закрытие уведомлений по клику
document.addEventListener('DOMContentLoaded', function() {
  const closeButtons = document.querySelectorAll('.close-btn');
  
  closeButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      this.parentElement.style.opacity = '0';
      setTimeout(() => this.parentElement.remove(), 300);
    });
  });

  // Автоматическое скрытие через 3 секунды
  const notifications = document.querySelectorAll('.notification');
  notifications.forEach(notification => {
    setTimeout(() => {
      notification.style.opacity = '0';
      setTimeout(() => notification.remove(), 180);
    }, 5000);
  });
});