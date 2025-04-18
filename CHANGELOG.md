# Changelog

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

