// Fonction pour changer le statut de la commande
function changeStatus(button, action) {
    const row = button.closest('tr'); // Trouve la ligne correspondante
    const statusCell = row.querySelector('.status'); // Trouve la cellule de statut

    if (action === 'serve') {
        statusCell.textContent = 'Commande Servie'; // Changer le texte du statut
        statusCell.className = 'status approved'; // Appliquer la classe "approuvée"
    } else if (action === 'cancel') {
        statusCell.textContent = 'La Commande a été annulée'; // Changer le texte du statut
        statusCell.className = 'status canceled'; // Appliquer la classe "annulée"
    }
}


function changeStatus(button, action) {
    const row = button.closest('tr');
    const commandeId = row.querySelector('td').textContent.trim();
    const newStatus = action === 'serve' ? 'Servie' : 'Annulé';

    fetch(`/update_commande_status/${commandeId}/${newStatus}/`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => {
        if (!response.ok) throw new Error("Échec de la requête");
        return response.json(); // Attente de réponse JSON
    })
    .then(data => {
        if (data.success) {
            const statusCell = row.querySelector('.order-state');
            statusCell.textContent = newStatus;
            statusCell.className = 'order-state';

            if (newStatus === 'Servie') statusCell.classList.add('served');
            else if (newStatus === 'Annulé') statusCell.classList.add('canceled');
            else statusCell.classList.add('pending');

            const buttons = row.querySelectorAll('.action-btn');
            buttons.forEach(btn => {
                btn.disabled = true;
                btn.style.opacity = '0.6';
            });
        } else {
            alert('La mise à jour du statut a échoué.');
        }
    })
    .catch(error => {
        console.error('Erreur lors de la mise à jour:', error);
        alert('Une erreur est survenue.');
    });
}

