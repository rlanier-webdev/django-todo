/**
 * TodoDev - Main JavaScript Module
 *
 * Handles task completion toggling, session management,
 * and form interactions.
 */

(function () {
  "use strict";

  // ============================================
  // Utility Functions
  // ============================================

  /**
   * Get CSRF token from cookies for Django requests.
   * @param {string} name - Cookie name (default: 'csrftoken')
   * @returns {string|null} The cookie value or null
   */
  function getCookie(name) {
    if (!document.cookie) return null;

    const cookies = document.cookie.split(";");
    for (const cookie of cookies) {
      const trimmed = cookie.trim();
      if (trimmed.startsWith(name + "=")) {
        return decodeURIComponent(trimmed.substring(name.length + 1));
      }
    }
    return null;
  }

  /**
   * Show a toast notification using SweetAlert2.
   * @param {string} type - 'success', 'error', 'warning', 'info'
   * @param {string} message - Message to display
   */
  function showToast(type, message) {
    if (typeof Swal === "undefined") {
      console.log(`[${type}] ${message}`);
      return;
    }

    const Toast = Swal.mixin({
      toast: true,
      position: "top-end",
      showConfirmButton: false,
      timer: 3000,
      timerProgressBar: true,
    });

    Toast.fire({
      icon: type,
      title: message,
    });
  }

  // ============================================
  // Task Toggle Handler
  // ============================================

  /**
   * Initialize task completion toggle handlers.
   * Uses AJAX to update task status without page reload.
   */
  function initTaskToggle() {
    const checkboxes = document.querySelectorAll(".toggle-completed");

    checkboxes.forEach((checkbox) => {
      checkbox.addEventListener("change", async function () {
        const taskId = this.getAttribute("data-id");
        const isCompleted = this.checked;
        const row = this.closest("tr");

        // Disable checkbox during request
        this.disabled = true;

        try {
          const response = await fetch(
            `/app/tasks/toggle-completed/${taskId}/`,
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
              },
              body: JSON.stringify({ is_completed: isCompleted }),
            }
          );

          const data = await response.json();

          if (data.success) {
            // Update visual feedback
            if (row) {
              row.classList.add("table-transition");
              row.style.opacity = "0.5";

              // Reload after brief delay to show transition
              setTimeout(() => {
                location.reload();
              }, 300);
            } else {
              location.reload();
            }
          } else {
            // Revert checkbox on failure
            this.checked = !isCompleted;
            showToast("error", data.error || "Failed to update task");
          }
        } catch (error) {
          console.error("Toggle error:", error);
          this.checked = !isCompleted;
          showToast("error", "Network error. Please try again.");
        } finally {
          this.disabled = false;
        }
      });
    });
  }

  // ============================================
  // Session Timeout Management
  // ============================================

  /**
   * Initialize session timeout warnings and auto-logout.
   * Warning at 28 minutes, logout at 30 minutes of inactivity.
   */
  function initSessionTimeout() {
    const WARNING_TIME = 28 * 60 * 1000; // 28 minutes
    const LOGOUT_TIME = 30 * 60 * 1000; // 30 minutes
    let warningTimeout;
    let logoutTimeout;

    function resetTimers() {
      clearTimeout(warningTimeout);
      clearTimeout(logoutTimeout);

      warningTimeout = setTimeout(showWarning, WARNING_TIME);
      logoutTimeout = setTimeout(autoLogout, LOGOUT_TIME);
    }

    function showWarning() {
      if (typeof Swal === "undefined") {
        if (confirm("You will be logged out in 2 minutes. Stay logged in?")) {
          pingSession();
        } else {
          autoLogout();
        }
        return;
      }

      Swal.fire({
        title: "Session Expiring",
        text: "You will be logged out in 2 minutes due to inactivity.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Stay Logged In",
        confirmButtonColor: "#0d6efd",
        cancelButtonText: "Log Out",
        cancelButtonColor: "#dc3545",
        reverseButtons: true,
        allowOutsideClick: false,
        allowEscapeKey: false,
      }).then((result) => {
        if (result.isConfirmed) {
          pingSession();
        } else {
          autoLogout();
        }
      });
    }

    function pingSession() {
      fetch("/ping-session/", {
        method: "GET",
        credentials: "same-origin",
      })
        .then(() => {
          resetTimers();
          showToast("success", "Session extended");
        })
        .catch(() => {
          showToast("error", "Could not extend session");
        });
    }

    function autoLogout() {
      window.location.href = "/logout/";
    }

    // Reset timers on user activity (throttled)
    let activityThrottle;
    const activityEvents = ["click", "keydown", "scroll", "touchstart"];

    function handleActivity() {
      if (activityThrottle) return;

      activityThrottle = setTimeout(() => {
        activityThrottle = null;
      }, 1000);

      resetTimers();
    }

    activityEvents.forEach((event) => {
      document.addEventListener(event, handleActivity, { passive: true });
    });

    // Start timers after page load
    setTimeout(resetTimers, 3000);
  }

  // ============================================
  // Form Toggle (Login/Signup)
  // ============================================

  /**
   * Initialize login/signup form toggle on home page.
   */
  function initFormToggle() {
    const showSignupLink = document.getElementById("show-signup");
    const showLoginLink = document.getElementById("show-login");
    const loginForm = document.getElementById("login-form");
    const signupForm = document.getElementById("signup-form");

    if (!showSignupLink || !loginForm) return;

    showSignupLink.addEventListener("click", function (e) {
      e.preventDefault();
      loginForm.classList.add("d-none");
      signupForm.classList.remove("d-none");
    });

    if (showLoginLink) {
      showLoginLink.addEventListener("click", function (e) {
        e.preventDefault();
        signupForm.classList.add("d-none");
        loginForm.classList.remove("d-none");
      });
    }
  }

  // ============================================
  // Category Modal Handler
  // ============================================

  /**
   * Initialize add category modal functionality.
   */
  function initCategoryModal() {
    const addCategoryForm = document.getElementById("addCategoryForm");
    if (!addCategoryForm) return;

    addCategoryForm.addEventListener("submit", async function (e) {
      e.preventDefault();

      const nameInput = document.getElementById("categoryName");
      const name = nameInput.value.trim();

      if (!name) {
        showToast("warning", "Please enter a category name");
        return;
      }

      try {
        const formData = new FormData();
        formData.append("name", name);

        const response = await fetch("/app/categories/add/", {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
          },
          body: formData,
        });

        const data = await response.json();

        if (data.id) {
          // Add new option to category select
          const categorySelect = document.getElementById("id_category");
          if (categorySelect) {
            const option = new Option(data.name, data.id, true, true);
            categorySelect.add(option);
          }

          // Close modal and reset form
          const modal = bootstrap.Modal.getInstance(
            document.getElementById("addCategoryModal")
          );
          if (modal) modal.hide();

          nameInput.value = "";
          showToast("success", "Category added successfully");
        } else {
          showToast("error", data.error || "Failed to add category");
        }
      } catch (error) {
        console.error("Category error:", error);
        showToast("error", "Network error. Please try again.");
      }
    });
  }

  // ============================================
  // Initialize All Modules
  // ============================================

  document.addEventListener("DOMContentLoaded", function () {
    initTaskToggle();
    initSessionTimeout();
    initFormToggle();
    initCategoryModal();
  });

  // Export getCookie for potential external use
  window.getCookie = getCookie;
})();
