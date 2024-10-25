function openEditModal(eventID) {
    // Fetch current log data (this could be done via an API or from the DOM)
    const logElement = document.getElementById(`log-${eventID}`);
    const title = logElement.querySelector('h2').innerText;
    const dateTime = logElement.querySelector('p').innerText.split(' - ');
    const date = dateTime[0];
    const time = dateTime[1];
    const notes = logElement.querySelector('.notes-container').innerText;

    // Populate the modal fields
    document.getElementById('edit-log-id').value = eventID;
    document.getElementById('edit-title').value = title;
    document.getElementById('edit-date').value = date;
    document.getElementById('edit-time').value = time;
    document.getElementById('edit-notes').value = notes;

    // Show the modal
    document.getElementById('edit-modal').style.display = 'block';
}

function updateEvent(eventID) {
    // Send the form data via a POST request using fetch.
    fetch('/events/update', {
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
}

function closeEditModal() {
    document.getElementById('edit-modal').style.display = 'none';
}