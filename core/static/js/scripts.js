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
            alert('Something went wrong.');
          } else {
            // Find the row
            const row = this.closest('tr');
    
            // Get the table to append to based on completion status
            const targetTable = isCompleted ? document.getElementById('completed-tasks') : document.getElementById('active-tasks');
            
            // Check if the target table exists before appending
            if (targetTable) {
              // Remove the row from its current position
              row.parentNode.removeChild(row);
              
              // Append it to the target table
              targetTable.appendChild(row);
            } else {
              console.error('Target table not found.');
            }
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
  