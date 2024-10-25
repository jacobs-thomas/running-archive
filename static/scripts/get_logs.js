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
    logContainer.appendChild(eventElement);
}