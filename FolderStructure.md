# Complete Charity Directory Folder Structure

```
charity-directory/
│
├── frontend/                                    # React + Vite (UI for users & orgs)
│   ├── public/                                  # Static files
│   │   ├── favicon.ico
│   │   ├── index.html
│   │   ├── manifest.json
│   │   └── robots.txt
│   │
│   ├── src/
│   │   ├── assets/                              # Images, logos, styles
│   │   │   ├── images/
│   │   │   │   ├── logo.png
│   │   │   │   ├── hero-banner.jpg
│   │   │   │   └── default-org-logo.png
│   │   │   ├── icons/
│   │   │   │   ├── category-icons/
│   │   │   │   └── social-icons/
│   │   │   └── styles/
│   │   │       ├── globals.css
│   │   │       └── variables.css
│   │   │
│   │   ├── components/                          # Reusable React components
│   │   │   ├── common/                          # Generic reusable components
│   │   │   │   ├── Navbar.jsx
│   │   │   │   ├── Footer.jsx
│   │   │   │   ├── FormInput.jsx
│   │   │   │   ├── Button.jsx
│   │   │   │   ├── Modal.jsx
│   │   │   │   ├── Loading.jsx
│   │   │   │   ├── ErrorBoundary.jsx
│   │   │   │   ├── ProtectedRoute.jsx
│   │   │   │   └── Pagination.jsx
│   │   │   │
│   │   │   ├── organization/                    # Organization-specific components
│   │   │   │   ├── OrgCard.jsx
│   │   │   │   ├── OrgGallery.jsx
│   │   │   │   ├── OrgContactForm.jsx
│   │   │   │   ├── OrgDetails.jsx
│   │   │   │   ├── VerificationBadge.jsx
│   │   │   │   └── StatusIndicator.jsx
│   │   │   │
│   │   │   ├── search/                          # Search & filter components
│   │   │   │   ├── SearchBar.jsx
│   │   │   │   ├── FilterPanel.jsx
│   │   │   │   ├── CategoryTabs.jsx
│   │   │   │   ├── LocationFilter.jsx
│   │   │   │   └── SearchResults.jsx
│   │   │   │
│   │   │   ├── admin/                           # Admin-specific components
│   │   │   │   ├── ReviewCard.jsx
│   │   │   │   ├── AdminStats.jsx
│   │   │   │   ├── PendingQueue.jsx
│   │   │   │   ├── AuditLogTable.jsx
│   │   │   │   └── UserManagementTable.jsx
│   │   │   │
│   │   │   └── forms/                           # Form components
│   │   │       ├── LoginForm.jsx
│   │   │       ├── SignupForm.jsx
│   │   │       ├── OrgRegistrationForm.jsx
│   │   │       └── ContactForm.jsx
│   │   │
│   │   ├── pages/                               # Screens/Pages
│   │   │   ├── public/                          # Public pages
│   │   │   │   ├── Home.jsx
│   │   │   │   ├── Browse.jsx                   # Organization directory
│   │   │   │   ├── OrgProfile.jsx
│   │   │   │   ├── Search.jsx
│   │   │   │   ├── About.jsx
│   │   │   │   └── Contact.jsx
│   │   │   │
│   │   │   ├── auth/                            # Authentication pages
│   │   │   │   ├── Login.jsx
│   │   │   │   ├── Signup.jsx
│   │   │   │   ├── ForgotPassword.jsx
│   │   │   │   └── ResetPassword.jsx
│   │   │   │
│   │   │   ├── user/                            # User dashboard pages
│   │   │   │   ├── Dashboard.jsx
│   │   │   │   ├── Bookmarks.jsx
│   │   │   │   ├── Profile.jsx
│   │   │   │   └── SearchHistory.jsx
│   │   │   │
│   │   │   ├── organization/                    # Org admin pages
│   │   │   │   ├── OrgRegistration.jsx
│   │   │   │   ├── OrgDashboard.jsx
│   │   │   │   ├── EditOrg.jsx
│   │   │   │   ├── PhotoManager.jsx
│   │   │   │   └── Messages.jsx
│   │   │   │
│   │   │   ├── admin/                           # Platform admin pages
│   │   │   │   ├── AdminDashboard.jsx
│   │   │   │   ├── ReviewSubmissions.jsx
│   │   │   │   ├── ManageOrgs.jsx
│   │   │   │   ├── ManageUsers.jsx
│   │   │   │   ├── ManageCategories.jsx
│   │   │   │   ├── Analytics.jsx
│   │   │   │   ├── AuditLogs.jsx
│   │   │   │   └── Advertisements.jsx
│   │   │   │
│   │   │   └── error/                           # Error pages
│   │   │       ├── NotFound.jsx
│   │   │       ├── Unauthorized.jsx
│   │   │       └── ServerError.jsx
│   │   │
│   │   ├── hooks/                               # Custom React hooks
│   │   │   ├── useAuth.js
│   │   │   ├── useApi.js
│   │   │   ├── useSearch.js
│   │   │   ├── useNotifications.js
│   │   │   └── useLocalStorage.js
│   │   │
│   │   ├── services/                            # API calls & external services
│   │   │   ├── api.js                           # Axios instance & interceptors
│   │   │   ├── authService.js
│   │   │   ├── organizationService.js
│   │   │   ├── userService.js
│   │   │   ├── searchService.js
│   │   │   ├── uploadService.js
│   │   │   └── notificationService.js
│   │   │
│   │   ├── context/                             # Global state management
│   │   │   ├── AuthContext.jsx
│   │   │   ├── NotificationContext.jsx
│   │   │   └── SearchContext.jsx
│   │   │
│   │   ├── utils/                               # Frontend utilities
│   │   │   ├── constants.js
│   │   │   ├── helpers.js
│   │   │   ├── validation.js
│   │   │   ├── formatters.js
│   │   │   └── dateUtils.js
│   │   │
│   │   ├── styles/                              # Global styles
│   │   │   ├── index.css
│   │   │   ├── globals.css
│   │   │   └── components.css
│   │   │
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── .env.example                             # Environment variables template
│   ├── .eslintrc.js
│   ├── .prettierrc
│   ├── vite.config.js
│   ├── package.json
│   ├── package-lock.json
│   ├── tailwind.config.js
│   └── README.md
│
├── backend/                                     # Flask API
│   ├── app/
│   │   ├── __init__.py                          # Flask app factory
│   │   ├── config.py                            # Settings (DB, JWT, OAuth keys)
│   │   ├── models/                              # SQLAlchemy models (organized)
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── organization.py
│   │   │   ├── category.py
│   │   │   ├── location.py
│   │   │   ├── notification.py
│   │   │   ├── audit_log.py
│   │   │   └── advertisement.py
│   │   │
│   │   ├── routes/                              # API endpoints (blueprints)
│   │   │   ├── __init__.py
│   │   │   ├── auth.py                          # Authentication routes
│   │   │   ├── users.py                         # End user endpoints
│   │   │   ├── organizations.py                 # Organization CRUD
│   │   │   ├── admin.py                         # Admin approval endpoints
│   │   │   ├── search.py                        # Search & filter endpoints
│   │   │   ├── categories.py                    # Category management
│   │   │   ├── locations.py                     # Location endpoints
│   │   │   ├── notifications.py                 # Notification endpoints
│   │   │   ├── uploads.py                       # File upload endpoints
│   │   │   └── advertisements.py                # Ad management
│   │   │
│   │   ├── services/                            # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py                  # Encryption, JWT, OAuth
│   │   │   ├── organization_service.py          # Org business logic
│   │   │   ├── search_service.py                # Search & filtering logic
│   │   │   ├── notification_service.py          # Simple notifications
│   │   │   ├── file_service.py                  # File upload handling
│   │   │   ├── email_service.py                 # Email notifications
│   │   │   └── analytics_service.py             # Basic analytics
│   │   │
│   │   ├── middleware/                          # Custom middleware
│   │   │   ├── __init__.py
│   │   │   ├── auth_middleware.py               # JWT validation
│   │   │   ├── logging_middleware.py            # Request logging
│   │   │   └── cors_middleware.py               # CORS handling
│   │   │
│   │   ├── utils/                               # Backend utilities
│   │   │   ├── __init__.py
│   │   │   ├── decorators.py                    # Role-based access decorators
│   │   │   ├── validators.py                    # Form & data validation
│   │   │   ├── helpers.py                       # General utilities
│   │   │   ├── email_templates.py               # Email template functions
│   │   │   └── file_utils.py                    # File handling utilities
│   │   │
│   │   ├── admin/                               # Flask-Admin setup
│   │   │   ├── __init__.py
│   │   │   ├── views.py                         # Admin view classes
│   │   │   └── forms.py                         # Admin form classes
│   │   │
│   │   ├── extensions.py                        # Flask extensions (db, jwt, etc.)
│   │   └── database.py                          # Database initialization
│   │
│   ├── migrations/                              # Database migrations
│   │   ├── versions/
│   │   ├── alembic.ini
│   │   ├── env.py
│   │   └── script.py.mako
│   │
│   ├── tests/                                   # Unit & integration tests
│   │   ├── __init__.py
│   │   ├── conftest.py                          # Test configuration
│   │   ├── test_auth.py
│   │   ├── test_organizations.py
│   │   ├── test_admin.py
│   │   ├── test_search.py
│   │   ├── test_users.py
│   │   └── test_api_integration.py
│   │
│   ├── .env.example                             # Environment variables template
│   ├── requirements.txt                         # Python dependencies
│   ├── requirements-dev.txt                     # Development dependencies
│   ├── wsgi.py                                  # WSGI entry point
│   ├── run.py                                   # Development server entry
│   └── README.md
│
├── uploads/                                     # Local file storage (development)
│   ├── logos/
│   │   └── .gitkeep
│   ├── photos/
│   │   └── .gitkeep
│   └── documents/
│       └── .gitkeep
│
├── logs/                                        # Application logs
│   ├── app.log
│   ├── error.log
│   └── .gitkeep
│
├── scripts/                                     # Utility scripts
│   ├── seed_database.py                         # Sample data seeding
│   ├── backup_db.py                             # Database backup
│   ├── restore_db.py                            # Database restore
│   ├── deploy.sh                                # Deployment script
│   ├── setup_dev.py                             # Development setup
│   └── migrate_data.py                          # Data migration utilities
│
├── docs/                                        # Documentation
│   ├── api/
│   │   ├── authentication.md
│   │   ├── organizations.md
│   │   ├── users.md
│   │   ├── admin.md
│   │   └── search.md
│   ├── deployment/
│   │   ├── production_setup.md
│   │   ├── environment_variables.md
│   │   └── server_configuration.md
│   ├── development/
│   │   ├── getting_started.md
│   │   ├── coding_standards.md
│   │   └── testing_guide.md
│   ├── uml_diagrams/
│   │   ├── system_architecture.png
│   │   ├── class_diagram.png
│   │   ├── database_schema.png
│   │   └── user_flow_diagram.png
│   ├── api_endpoints.md
│   ├── system_design.md
│   ├── user_stories.md
│   └── changelog.md
│
├── config/                                      # Configuration files
│   ├── development.py
│   ├── production.py
│   ├── testing.py
│   └── docker/
│       ├── Dockerfile.frontend
│       ├── Dockerfile.backend
│       └── nginx.conf
│
├── database/                                    # Database files & backups
│   ├── charity_directory.db                     # SQLite database (development)
│   ├── schema.sql                               # Database schema
│   ├── seed_data.sql                            # Initial data
│   └── backups/
│       └── .gitkeep
│
├── monitoring/                                  # Monitoring & health checks
│   ├── health_check.py
│   ├── performance_monitor.py
│   └── error_tracker.py
│
├── .github/                                     # GitHub workflows
│   ├── workflows/
│   │   ├── ci.yml                               # Continuous Integration
│   │   ├── cd.yml                               # Continuous Deployment
│   │   └── test.yml                             # Automated testing
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── pull_request_template.md
│
├── .env.example                                 # Environment variables template
├── .env.development                             # Development environment (gitignored)
├── .env.production                              # Production environment (gitignored)
├── .gitignore
├── .gitattributes
├── docker-compose.yml                           # Container orchestration
├── docker-compose.prod.yml                      # Production containers
├── Makefile                                     # Common commands
├── README.md                                    # Project overview
├── LICENSE
├── CONTRIBUTING.md                              # Contribution guidelines
├── SECURITY.md                                  # Security policy
└── jira_tasks_charity_directory.csv             # Project management
```

## Key Configuration Files Content:

### .env.example
```
# Database
DATABASE_URL=sqlite:///charity_directory.db

# JWT
JWT_SECRET_KEY=your-secret-key-here
JWT_ACCESS_TOKEN_EXPIRES=3600

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Email Service
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# File Upload
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE=5242880
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif,pdf

# Application
FLASK_ENV=development
FLASK_DEBUG=True
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:5000
```

### .gitignore
```
# Environment files
.env
.env.local
.env.development
.env.production

# Database
*.db
*.sqlite
*.sqlite3

# Logs
logs/
*.log

# Uploads
uploads/*
!uploads/.gitkeep

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Backup files
database/backups/*
!database/backups/.gitkeep
```