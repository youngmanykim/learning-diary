document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.entry-input').forEach(input => {
        input.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                event.preventDefault(); // 폼 제출 방지
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

        // Add hidden input to form
        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = type;
        hiddenInput.value = input.value;
        document.querySelector('form').appendChild(hiddenInput);

        input.value = '';
    }
}
