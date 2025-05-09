## [1.8.2] - 2025-04-24
### Changed
- Switched from `python-decouple` to `django-environ` for environment variable management.
  - Updated settings to use `env()` instead of `config()`.
  - Replaced `config("ENVIRONMENT")` with `env('ENVIRONMENT', default='development')`.

### Removed
- Removed `python-decouple` from the project dependencies.

## [1.8.1] - 2025-04-20
### Enhanced
- Task detail page now uses a two-column layout.
- Activity log is displayed beside task details for improved visibility and user experience.


## [v1.8.0] - 2025-04-20
### Added
- Category model allowing users to categorize tasks (e.g., "Work", "Personal").
- Modal with AJAX to add categories from task form via plus icon.
- Category field to task form and templates.
- Category field to task filter interface.
- Category change tracking in task activity logs.

### Changed
- Improved UI layout for category input and dropdown.
- Enhanced form widgets with support for multiple CSS classes.

## [v1.7.1] - 2025-04-19
### Changed
- Task model: Reduced maximum length of the `title` field from 255 to 100 characters for improved data consistency.
- `Task.title` field max length reduced from 255 to 100 characters for consistency with UI display.
- Dashboard table now limits task title display to 25 characters with full title shown on hover.
- 
### Added
- UI enhancement: Task descriptions in the dashboard table are now truncated to 75 characters for better readability.
- Full task descriptions are still accessible via tooltips when hovering over the truncated text.

### Removed
- Removed the `description` column from the TaskTable to avoid horizontal expansion issues.
- Updated the layout to prevent overflow and ensure proper table display.

## [v1.7] - 2025-04-18
### Added
- **Task Activity Log functionality**
  - Captures task creation and updates with detailed field-level tracking (Title, Priority, Deadline, Status).
  - User-friendly change format:
    - Title Changed from ... to ...
    - Priority Changed from ... to ...
    - Deadline Changed from ... to ...
    - Status Changed from ... to ...
  - **Only fields that have changed** are logged, reducing noise in the activity log.
  - **Implemented `post_save` signal** to capture task updates and store activities.
- **Improved UI** to display task activity in a clean, readable format.
  - Activity logs now show the user, action (Created/Updated), timestamp, and changes made.

## [v1.6] - 2025-04-18
### Added
- New `status` field to `Task` model with options: `pending`, `in progress`, `completed`.
- Admins and users can now manually set task status via the UI.

### Enhanced
- `TaskForm` updated to include an editable `status` dropdown.
- Custom `save()` method in `TaskForm` syncs `status` and `is_completed`:
  - If status is 'completed', `is_completed` is auto-checked.
  - If status is 'pending' or 'in progress', `is_completed` is auto-unchecked.
  - If status is not set, it defaults based on `is_completed`.
- Ensures consistent logic across form submission, UI, and model updates.

## [v1.5.3] - 2025-04-18
### Added
- "Clear" button to the task filter form for improved usability.

### Fixed
- Resolved duplicate id_username field warning when both login and signup forms are rendered on the homepage by adding unique form prefixes.
- Resolved `MultiValueDictKeyError` in the signup form by ensuring unique `name` and `id` attributes for all form fields.
- Corrected form field conflicts between the login and signup forms.
- Enhanced error handling in the signup form for improved user experience.
- 
## [v1.5.2] - 2025-04-18
### Added
- Added visual clarity to incomplete tasks by styling their checkboxes with a border.

## [v1.5.1] - 2025-04-18

### Added
- **Session Timeout Warning**
  - Users receive a SweetAlert2 warning modal 1 minute before session expiration.
  - Sessions automatically expire after 28 minutes of inactivity.
  - Timeout logic added to `scripts.js`.

- **Overdue task deadline highlight**: 
  - Tasks with a deadline that has passed now have their background highlighted in red to indicate overdue status.

### Changed
- Updated settings for static file management and included necessary configurations.

### Fixed
- **Static Files Loading**
  - Corrected `BASE_DIR` path to point to the correct project root.
  - Updated `STATICFILES_DIRS` to reference the actual `static` directory.
  - Resolved `ImproperlyConfigured` error by skipping `STATIC_ROOT` in development.

## [v1.5.0] - 2025-04-18

### Added
- Refactored settings into modular files for improved environment management:
  - `base.py`: Shared settings for both dev and prod environments.
  - `dev.py`: Development-specific settings for a local environment.
  - `prod.py`: Production-specific settings for deployment.
- Integrated **python-decouple** to securely load environment variables from a `.env` file.
- Updated `manage.py` to load settings dynamically based on the `ENVIRONMENT` variable in `.env`.
- Moved `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, and database configuration to environment-specific `.env` files.
- Refined path resolution for `STATICFILES_DIRS` using `pathlib`.

### Changed
- Updated project configuration for smoother deployment (dev and prod environments).
- Cleaned up static files setup to prevent potential path errors.

### Fixed
- Improved codebase organization and readiness for production deployments.

