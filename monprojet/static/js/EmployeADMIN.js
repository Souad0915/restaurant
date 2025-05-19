// Fonction pour afficher les formulaires
function showForm(type, employee) {
    let formId = type === 'edit' ? 'edit-form' : 'delete-form';
    document.getElementById(formId).style.display = 'flex';

    if (type === 'edit') {
        // Préchargez les informations de l'employé si nécessaire
        document.getElementById('nom').value = employee;
        // Ajoutez plus de logiques pour charger les autres champs de l'employé
    }
}

// Fonction pour fermer les formulaires
function closeForm() {
    document.getElementById('edit-form').style.display = 'none';
    document.getElementById('delete-form').style.display = 'none';
    document.getElementById('add-employee-form').style.display = 'none';
}

// Fonction pour afficher le formulaire d'ajout d'employé
function showAddForm() {
    document.getElementById('add-employee-form').style.display = 'flex';
}
