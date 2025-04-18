# Changelog

## [1.5.1] - 2025-04-18

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

