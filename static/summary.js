function addEntry(inputId) {
    const input = document.getElementById(inputId);
    const list = document.getElementById(inputId + '-list');
    if (input.value.trim() !== '') {
        const li = document.createElement('li');
        const inputField = document.createElement('input');
        inputField.type = 'text';
        inputField.name = inputId;
        inputField.value = input.value;
        inputField.className = 'input-field';
        li.appendChild(inputField);
        list.appendChild(li);
        input.value = '';
    }
}

function handleEnter(event, inputId) {
    if (event.key === 'Enter') {
        event.preventDefault();
        addEntry(inputId);
    }
}

document.getElementById('main-task').addEventListener('keydown', function(event) {
    handleEnter(event, 'main-task');
});

document.getElementById('learning').addEventListener('keydown', function(event) {
    handleEnter(event, 'learning');
});

document.getElementById('special-notes').addEventListener('keydown', function(event) {
    handleEnter(event, 'special-notes');
});

document.getElementById('tomorrow-task').addEventListener('keydown', function(event) {
    handleEnter(event, 'tomorrow-task');
});

document.getElementById('summary-form')?.addEventListener('submit', function(event) {
    event.preventDefault();

    const mainTask = [];
    document.querySelectorAll('#main-task-list li input').forEach(item => {
        mainTask.push(item.value);
    });

    const learning = [];
    document.querySelectorAll('#learning-list li input').forEach(item => {
        learning.push(item.value);
    });

    const specialNotes = [];
    document.querySelectorAll('#special-notes-list li input').forEach(item => {
        specialNotes.push(item.value);
    });

    const tomorrowTask = [];
    document.querySelectorAll('#tomorrow-task-list li input').forEach(item => {
        tomorrowTask.push(item.value);
    });

    const data = {
        'main-task': mainTask,
        'learning': learning,
        'special-notes': specialNotes,
        'tomorrow-task': tomorrowTask
    };

    fetch(event.target.action, {
        method: event.target.method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/history';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
