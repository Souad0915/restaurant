// Initialisation des graphiques avec Chart.js
window.onload = function() {
    // Graphique en barre
    var barCtx = document.getElementById('bar-chart').getContext('2d');
    var barChart = new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: ['Plat 1', 'Plat 2', 'Plat 3', 'Plat 4'],
            datasets: [{
                label: 'Ventes',
                data: [12, 19, 3, 5], // Remplace ces valeurs par les données dynamiques
                backgroundColor: ['#3498db', '#2ecc71', '#e74c3c', '#f39c12'],
                borderColor: '#2c3e50',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Graphique circulaire
    var pieCtx = document.getElementById('pie-chart').getContext('2d');
    var pieChart = new Chart(pieCtx, {
        type: 'pie',
        data: {
            labels: ['Plat 1', 'Plat 2', 'Plat 3', 'Plat 4'],
            datasets: [{
                label: 'Répartition des ventes',
                data: [12, 19, 3, 5], // Remplace ces valeurs par les données dynamiques
                backgroundColor: ['#3498db', '#2ecc71', '#e74c3c', '#f39c12'],
                borderColor: '#2c3e50',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true
        }
    });
};
