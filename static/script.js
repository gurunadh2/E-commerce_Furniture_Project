document.addEventListener('DOMContentLoaded', () => {
    const productTitleInput = document.getElementById('productTitle');
    const suggestionsContainer = document.getElementById('suggestions');

    let titles = [];

    fetch('/product_titles')
        .then(response => response.json())
        .then(data => titles = data);

    productTitleInput.addEventListener('input', function () {
        const query = this.value.toLowerCase();
        suggestionsContainer.innerHTML = '';
        if (query && titles.length > 0) {
            const matched = titles.filter(title => title.toLowerCase().includes(query)).slice(0, 10);
            matched.forEach(suggestion => {
                const div = document.createElement('div');
                div.className = 'autocomplete-suggestion';
                div.textContent = suggestion;
                div.onclick = () => {
                    productTitleInput.value = suggestion;
                    suggestionsContainer.innerHTML = '';
                };
                suggestionsContainer.appendChild(div);
            });

            const rect = productTitleInput.getBoundingClientRect();
            suggestionsContainer.style.top = `${rect.bottom + window.scrollY}px`;
            suggestionsContainer.style.left = `${rect.left + window.scrollX}px`;
            suggestionsContainer.style.width = `${rect.width}px`;
        }
    });

    document.addEventListener('click', (e) => {
        if (!productTitleInput.contains(e.target)) {
            suggestionsContainer.innerHTML = '';
        }
    });
});
