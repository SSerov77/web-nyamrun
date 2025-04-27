import { setupModalButtons } from './modalHandlers.js';

document.addEventListener('DOMContentLoaded', () => {
    const modalContainer = document.getElementById('modal-container');
    setupModalButtons(modalContainer);
});