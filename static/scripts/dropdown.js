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
    fetch('/events/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => response.json()) // Assuming Flask returns a JSON response.
    .then(result => {
        // Handle successful response.
        console.log(result);

        if(result.successful) {
            newEvent = createEventHTML(result.event)

            // Ensure logContainer is defined.
            const logContainer = document.getElementById('log-container');
            if (logContainer) {
                logContainer.appendChild(newEvent);
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

// get logs.js...
function createEventHTML(event) {
    const newLog = document.createElement('div');
    newLog.classList.add('log');
    newLog.id = `log-${event.id}`;
    newLog.innerHTML = `
        <div class="log-header">
            <div class="log-details">
                <p>${event.date}</p>
                <h2>${event.title}</h2>
            </div>
            <div class="log-actions">
                <button id="edit-button" class="action-button" aria-label="Edit entry" onclick="openEditModal(${event.id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button id="delete-button" class="action-button" aria-label="Delete entry" onclick="deleteLog(${event.id})">
                    <i class="fas fa-trash-alt"></i>
                </button>
            </div>
        </div>
        <p class="notes-container" id="message">${event.notes}</p>
    `;
    return newLog;
}

document.addEventListener("DOMContentLoaded", () => {
fetch('/events')
    .then(response => response.json())
    .then(result => {
        if (result.successful) {
            const logContainer = document.getElementById('log-container');
            if (!logContainer) {
                console.error('logContainer element not found');
                return;
            }

            logContainer.innerHTML = ''; // Clear existing content

            result.events.forEach(event => {
                const eventElement = createEventHTML(event);
                logContainer.appendChild(eventElement);
            });
        } else {
            console.error(result.message);
        }
    })
    .catch(error => {
        console.error("Error fetching events:", error);
    });
});

function addSingleEvent(event) {
    const logContainer = document.getElementById('log-container');
    const eventElement = createEventHTML(event);

    if (!logContainer) {
        console.error('logContainer element not found');
        return;
    }

    logContainer.appendChild(eventElement);
}