function confirmDelete(sightTypeId) {
  if (confirm('Are you sure you want to delete this sight type?')) {
    var deleteUrl = deleteSightTypeUrlTemplate.replace('0', sightTypeId);
    fetch(deleteUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrfToken // Use the global variable
      },
      body: 'sight_type_id=' + encodeURIComponent(sightTypeId)
    }).then(response => {
      if (response.ok) {
        window.location.reload(); // Reload the page to reflect the changes
      } else {
        alert('Error deleting sight type.');
      }
    }).catch(error => {
      console.error('Error:', error);
    });
  }
}