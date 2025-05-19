// Tableau pour stocker les plats
let menuItems = [];
let currentIndex = null; // Index du plat en cours d'édition

// Fonction pour ajouter ou modifier un plat
document.getElementById('menuForm').addEventListener('submit', function (e) {
    e.preventDefault();

    // Récupérer les valeurs du formulaire
    const name = document.getElementById('dishName').value;
    const image = document.getElementById('dishImage').files[0];
    const description = document.getElementById('dishDescription').value;
    const price = document.getElementById('dishPrice').value;

    // Vérification que l'image est présente
    if (!image) {
        alert('Veuillez sélectionner une image pour le plat.');
        return;
    }

    const reader = new FileReader();
    reader.onload = function (e) {
        const newDish = {
            name,
            image: e.target.result, // Utiliser l'image encodée en base64
            description,
            price,
        };

        if (currentIndex === null) {
            // Ajouter un plat
            menuItems.push(newDish);
        } else {
            // Modifier un plat existant
            menuItems[currentIndex] = newDish;
            currentIndex = null; // Réinitialiser l'index après modification
        }

        // Re-rendu de la liste des plats
        renderMenu();
        clearForm(); // Réinitialiser le formulaire
    };

    reader.readAsDataURL(image); // Lire l'image
});

// Fonction pour afficher les plats du menu
function renderMenu() {
    const menuList = document.getElementById('menuList');
    menuList.innerHTML = ''; // Réinitialiser la liste

    menuItems.forEach((item, index) => {
        const menuItemDiv = document.createElement('div');
        menuItemDiv.classList.add('menu-item');

        menuItemDiv.innerHTML = `
            <img src="${item.image}" alt="${item.name}">
            <h3>${item.name}</h3>
            <p>${item.description}</p>
            <p>${item.price}fdj</p>
            <button class="edit" onclick="editDish(${index})">Modifier</button>
            <button onclick="deleteDish(${index})">Supprimer</button>
        `;

        menuList.appendChild(menuItemDiv);
    });
}

// Fonction pour supprimer un plat
function deleteDish(index) {
    menuItems.splice(index, 1); // Supprimer le plat du tableau
    renderMenu(); // Re-rendu de la liste des plats
}

// Fonction pour modifier un plat
function editDish(index) {
    const dish = menuItems[index];

    // Remplir le formulaire avec les valeurs du plat à modifier
    document.getElementById('dishName').value = dish.name;
    document.getElementById('dishDescription').value = dish.description;
    document.getElementById('dishPrice').value = dish.price;

    // Changer le titre du formulaire pour "Modifier"
    document.getElementById('formTitle').textContent = "Modifier un Plat";

    // Stocker l'index du plat à modifier
    currentIndex = index;
}

// Fonction pour réinitialiser le formulaire
function clearForm() {
    document.getElementById('menuForm').reset();
    document.getElementById('formTitle').textContent = "Ajouter un Plat"; // Réinitialiser le titre
    currentIndex = null; // Réinitialiser l'index
}

// Initialiser le rendu des plats au cas où il y en a déjà
renderMenu();
