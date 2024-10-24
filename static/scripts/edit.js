function openEditModal(logId) {
    // Fetch current log data (this could be done via an API or from the DOM)
    const logElement = document.getElementById(`log-${logId}`);
    const title = logElement.querySelector('h2').innerText;
    const dateTime = logElement.querySelector('p').innerText.split(' - ');
    const date = dateTime[0];
    const time = dateTime[1];
    const notes = logElement.querySelector('.notes-container').innerText;

    // Populate the modal fields
    document.getElementById('edit-log-id').value = logId;
    document.getElementById('edit-title').value = title;
    document.getElementById('edit-date').value = date;
    document.getElementById('edit-time').value = time;
    document.getElementById('edit-notes').value = notes;

    // Show the modal
    document.getElementById('edit-modal').style.display = 'block';
}

function closeEditModal() {
    document.getElementById('edit-modal').style.display = 'none';
}