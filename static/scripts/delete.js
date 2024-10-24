function deleteLog(docId) {
    if (confirm('Are you sure you want to delete this log?')) {
        fetch(`/delete_log/${docId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'  // If using CSRF protection
            }
        }).then(response => {
            if (response.ok) {
                document.getElementById(`log-${docId}`).remove();  // Remove log from DOM
            } else {
                alert('Error deleting the log.');
            }
        });
    }
}