document.addEventListener("DOMContentLoaded", function () {
    // Sélection des boutons et des éléments nécessaires
    const incrementButtons = document.querySelectorAll('.increment');
    const decrementButtons = document.querySelectorAll('.decrement');
    const confirmButtons = document.querySelectorAll('.confirm');
    const cancelButtons = document.querySelectorAll('.cancel');
    const quantityCells = document.querySelectorAll('.quantity');
    const stockStatusCells = document.querySelectorAll('.stock-status');

    // Variables pour stocker les quantités originales (avant modification)
    const originalQuantities = Array.from(quantityCells).map(cell => parseInt(cell.innerText));

    // Fonction pour mettre à jour l'état du stock (vert ou rouge)
    function updateStockStatus(index) {
        let quantity = parseInt(quantityCells[index].innerText);
        if (quantity < 15) {
            stockStatusCells[index].classList.remove('green');
            stockStatusCells[index].classList.add('red');
        } else {
            stockStatusCells[index].classList.remove('red');
            stockStatusCells[index].classList.add('green');
        }
    }

    incrementButtons.forEach((button, index) => {
        button.addEventListener('click', function () {
            let quantityCell = quantityCells[index];
            let quantity = parseInt(quantityCell.innerText);
            quantityCell.innerText = quantity + 1;  // Incrémentation
            updateStockStatus(index);  // Mettre à jour l'état du stock
            confirmButtons[index].style.display = 'inline-block';  // Afficher le bouton de confirmation
            cancelButtons[index].style.display = 'inline-block';   // Afficher le bouton d'annulation
        });
    });

    decrementButtons.forEach((button, index) => {
        button.addEventListener('click', function () {
            let quantityCell = quantityCells[index];
            let quantity = parseInt(quantityCell.innerText);
            if (quantity > 0) {
                quantityCell.innerText = quantity - 1;  // Décrémentation
                updateStockStatus(index);  // Mettre à jour l'état du stock
                confirmButtons[index].style.display = 'inline-block';  // Afficher le bouton de confirmation
                cancelButtons[index].style.display = 'inline-block';   // Afficher le bouton d'annulation
            }
        });
    });

    confirmButtons.forEach((button, index) => {
        button.addEventListener('click', function () {
            // Confirmer le changement, cachez les boutons après confirmation
            button.style.display = 'none';
            cancelButtons[index].style.display = 'none';   // Cacher le bouton d'annulation
            originalQuantities[index] = parseInt(quantityCells[index].innerText); // Sauvegarder la nouvelle quantité
        });
    });

    cancelButtons.forEach((button, index) => {
        button.addEventListener('click', function () {
            // Annuler le changement et revenir à la quantité initiale
            let quantityCell = quantityCells[index];
            quantityCell.innerText = originalQuantities[index];  // Restaurer la quantité initiale
            updateStockStatus(index);  // Mettre à jour l'état du stock
            button.style.display = 'none';  // Cacher le bouton d'annulation après annulation
            confirmButtons[index].style.display = 'none';  // Cacher le bouton de confirmation après annulation
        });
    });
});
