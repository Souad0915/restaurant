document.addEventListener("DOMContentLoaded", function () {
    const messageElement = document.getElementById("dynamic-text");
    const message = "Bienvenue dans l'interface des chefs cuisiniers !";
    let index = 0;

    // Fonction pour afficher les lettres une par une
    function typeLetter() {
        if (index < message.length) {
            messageElement.textContent += message.charAt(index);
            index++;
            setTimeout(typeLetter, 100); // Vitesse d'apparition des lettres
        }
    }

    // Lancer l'animation au chargement de la page
    typeLetter();
});
