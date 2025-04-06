window.addEventListener('load', function () {
    feather.replace();
})

function deleteCategory(characterId, categoryId) {
    fetch(`/pokemon/${characterId}/categories/${categoryId}`, {
        method: 'DELETE',
    }).then(data => {
        window.location.href = `/pokemon/${characterId}/categories`;
    });
}