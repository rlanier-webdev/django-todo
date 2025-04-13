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
            'X-CSRFToken': getCookie('csrftoken')
          },
          body: JSON.stringify({ is_completed: isCompleted })
        })
        .then(res => res.json())
        .then(data => {
          if (!data.success) {
            alert('Something went wrong: ' + (data.error || 'Unknown error'));
          }
        })
        .catch(error => {
          console.error('Fetch error:', error);
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
               