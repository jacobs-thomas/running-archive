// Get the dropdown button and content
const dropdownBtn = document.getElementById('dropdown-btn');
const dropdownContent = document.getElementById('dropdown-content');

// Fields:
const logForm = document.getElementById('log-form');

document.getElementById('log-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Collect the information from the form.
    const formData = new FormData(this);

    // Convert the FormData to a JSON object.
    const data = {
        title: formData.get('title'),
        date: formData.get('date'),
        time: formData.get('time'),
        notes: formData.get('notes')
    }

    // Send the form data via a POST request using fetch.
    fetch('/add_log', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => response.json()) // Assuming Flask returns a JSON response.
    .then(result => {
        // Handle successful response.
        console.log(result);

        if(result.success) {
            const newLog = document.createElement('div');
            newLog.classList.add('log');
            newLog.id = `log-${result.id}`
            newLog.innerHTML = `
                <div class="log-header">
                    <div class="log-details">
                        <p>${result.date} - ${result.time}</p>
                        <h2>${result.title}</h2>
                    </div>
                    <div class="log-actions">
                        <button id="edit-button" class="action-button" aria-label="Edit entry">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button id="delete-button" class="action-button" aria-label="Delete entry" onclick="deleteLog(${result.id})">
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    </div>
                </div>
                <p class="notes-container" id="message">${result.notes}</p>
            `;

            // Ensure logContainer is defined.
            const logContainer = document.getElementById('log-container');
            if (logContainer) {
                logContainer.appendChild(newLog);
            } else {
                console.error('logContainer element not found');
            }
        }
    })
    .catch(error => {
        // Handle error.
        console.error('Error:', error);

    });
});


// Toggle dropdown visibility on button click
dropdownBtn.addEventListener('click', function() {
    // Close the dropdown if it's already open.
    if (dropdownContent.style.display === 'block') {
        dropdownContent.style.display = 'none';
        return;
    }

    // Otherwise, present the dropdown.
    dropdownContent.style.display = 'block';
});

// Optionally, close the dropdown if the user clicks outside of it
window.onclick = function(event) {
    if (!dropdownContent.contains(event.target) && !dropdownBtn.contains(event.target)) {
        if (dropdownContent.style.display === 'block') {
            dropdownContent.style.display = 'none';
        }
    }
};