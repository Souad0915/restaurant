document.getElementById('confirmLogout').addEventListener('click', function() {
    // Suppression des informations d'authentification du localStorage ou des cookies
    localStorage.removeItem('user'); // Par exemple, si vous stockez l'utilisateur dans le localStorage
    // Vous pouvez également ajouter un cookie si nécessaire et le supprimer ici
    // Redirection vers la page de connexion après déconnexion
    window.location.href = 'connexion.html'; // Redirige vers la page de connexion
});
