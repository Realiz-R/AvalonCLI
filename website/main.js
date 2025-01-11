const animatedBox = document.getElementById('animatedBox');
const toggleButton = document.getElementById('toggleButton');

let isAnimating = true; // Состояние анимации

toggleButton.addEventListener('click', () => {
    if (isAnimating) {
        animatedBox.style.animation = 'none'; // Остановить анимацию
        toggleButton.textContent = 'Запустить анимацию';
    } else {
        animatedBox.style.animation = ''; // Запустить анимацию
        toggleButton.textContent = 'Остановить анимацию';
    }
    isAnimating = !isAnimating; // Переключить состояние
});
