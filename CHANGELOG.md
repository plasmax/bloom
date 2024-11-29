# Changelog

All notable changes to the Bloom project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Basic Flask application structure
- User authentication system with login/logout functionality
- Python sandbox implementation with security features:
  - Code validation to prevent dangerous operations
  - Execution timeouts and memory limits
  - Output size restrictions
  - Process isolation
  - Import restrictions
- Basic web interface with:
  - Navigation bar
  - Login page
  - Sandbox page with Ace code editor
- Comprehensive test suite covering:
  - Authentication system
  - Sandbox security
  - API endpoints
- Project setup:
  - Development environment configuration
  - Package installation setup
  - Test configuration

### In Progress
- File management system
- Task management system
- Database migrations
- User dashboard

### Planned
- Remote access via Ngrok integration
- Cloud deployment configuration
- Mobile responsive design improvements
- File upload and management interface
- Task creation and tracking interface
- Real-time notifications
- Project documentation
- API documentation
- Docker configuration
- Continuous Integration setup

### Technical Debt
- Complete the templates for all routes
- Implement proper error pages
- Add database migration system
- Add logging system
- Implement CSRF protection
- Add rate limiting
- Set up proper configuration management
- Complete the file management interface
- Implement user settings

## [0.1.0] - 2024-11-29
### Added
- Initial project structure
- Basic Flask application setup
- Authentication system
- Python sandbox implementation
- Test suite

### Security
- Implemented secure Python code execution
- Added code validation system
- Set up authentication requirements
- Added process isolation

### Development
- Set up development environment
- Added test configuration
- Created package installation setup
