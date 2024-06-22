document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.entry-input').forEach(input => {
        input.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                addEntry(input.id.split('-')[0]);
            }
        });
    });
});

function addEntry(type) {
    const input = document.getElementById(`${type}-input`);
    const list = document.getElementById(`${type}-list`);

    if (input.value.trim() !== "") {
        const listItem = document.createElement('li');
        listItem.textContent = input.value;
        list.appendChild(listItem);
        input.value = '';
    }
}
