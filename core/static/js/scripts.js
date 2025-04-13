document.addEventListener('DOMContentLoaded', function () {
    const checkboxes = document.querySelectorAll('.toggle-completed');

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            const taskId = this.getAttribute('data-id');
            const isCompleted = this.checked;

            fetch(`/app/tasks/toggle-completed/${taskId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Include the CSRF token here
                },
                body: JSON.stringify({ is_completed: isCompleted })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    // Instead of moving the row, simply reload the page
                    // to re-render both tables with the updated data.
                    location.reload();
                } else {
                    alert('Something went wrong.');
                    console.error(data.error);
                    // Optionally, revert the checkbox state on error
                    this.checked = !isCompleted;
                }
            })
            .catch(error => {
                console.error('Fetch error:', error);
                // Optionally, revert the checkbox state on error
                this.checked = !isCompleted;
            });
        });
    });
});
  
  // Utility: Get CSRF token from cookie
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
