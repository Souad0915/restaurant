
document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".delete");

    deleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            const row = this.closest("tr");
            row.remove();
        });
    });

    const editButtons = document.querySelectorAll(".edit");

    editButtons.forEach(button => {
        button.addEventListener("click", function () {
            alert("Modifier l'utilisateur !");
        });
    });
});