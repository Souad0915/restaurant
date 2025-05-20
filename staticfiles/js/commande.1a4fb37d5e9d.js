document.addEventListener("DOMContentLoaded", function() {
    // Fonction pour approuver une commande
    function approveCommand(event) {
        event.preventDefault();
        const button = event.target;
        button.textContent = 'Approuvé';
        button.style.backgroundColor = '#388E3C';
        button.style.color = 'white';
        button.disabled = true; // Désactive le bouton après clic
    }

    // Fonction pour annuler une commande
    function cancelCommand(event) {
        event.preventDefault();
        const button = event.target;
        button.textContent = 'Annulé';
        button.style.backgroundColor = '#e53935';
        button.style.color = 'white';
        button.disabled = true; // Désactive le bouton après clic
    }

    // Ajouter les événements aux boutons approuver et annuler
    const approveButtons = document.querySelectorAll('.approve');
    const cancelButtons = document.querySelectorAll('.cancel');

    approveButtons.forEach(button => {
        button.addEventListener('click', approveCommand);
    });

    cancelButtons.forEach(button => {
        button.addEventListener('click', cancelCommand);
    });
});
