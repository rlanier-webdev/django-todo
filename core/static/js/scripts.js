document.addEventListener('DOMContentLoaded', function () {
  // Task Toggle Handler
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
              if (data.success) {
                  location.reload();
              } else {
                  alert('Something went wrong.');
                  console.error(data.error);
                  this.checked = !isCompleted;
              }
          })
          .catch(error => {
              console.error('Fetch error:', error);
              this.checked = !isCompleted;
          });
      });
  });

  // Session Timeout Logic
  const warningTime = 28 * 60 * 1000; // 28 mins
  const logoutTime = 30 * 60 * 1000;  // 30 mins
  let warningTimeout;
  let logoutTimeout;

  function resetSessionTimers() {
      clearTimeout(warningTimeout);
      clearTimeout(logoutTimeout);

      warningTimeout = setTimeout(showSessionWarning, warningTime);
      logoutTimeout = setTimeout(autoLogout, logoutTime);
  }

  function showSessionWarning() {
      Swal.fire({
          title: 'Are you still there?',
          text: 'You will be logged out in 2 minutes due to inactivity.',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonText: 'Stay Logged In',
          cancelButtonText: 'Log Out',
          reverseButtons: true,
          allowOutsideClick: false,
          allowEscapeKey: false
      }).then(result => {
          if (result.isConfirmed) {
              fetch('/ping-session/', {
                  method: 'GET',
                  credentials: 'same-origin'
              }).then(() => resetSessionTimers());
          } else {
              autoLogout();
          }
      });
  }

    function autoLogout() {
        window.location.href = '/logout/';
    }

    // Reset the session timer on user activity
    ['click', 'mousemove', 'keydown', 'scroll'].forEach(event => {
        document.addEventListener(event, resetSessionTimers);
    });

    // Delay timer start by 3 seconds to avoid instant logout after load
    setTimeout(() => {
        resetSessionTimers();
    }, 3000);
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
