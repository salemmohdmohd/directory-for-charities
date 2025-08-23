charity-directory/
│
├── frontend/                        # React + Vite (UI for users & orgs)
│   ├── public/                      # Static files (favicon, index.html)
│   ├── src/
│   │   ├── assets/                  # Images, logos, styles
│   │   ├── components/              # Reusable React components
│   │   │   ├── Navbar.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── FormInput.jsx
│   │   │   └── ProtectedRoute.jsx
│   │   ├── pages/                   # Screens
│   │   │   ├── Home.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Signup.jsx
│   │   │   ├── OrgForm.jsx          # Org submission
│   │   │   ├── OrgProfile.jsx
│   │   │   ├── AdminDashboard.jsx   # View for admins
│   │   │   └── NotFound.jsx
│   │   ├── services/                # API calls
│   │   │   ├── api.js               # Axios instance
│   │   │   └── authService.js
│   │   ├── context/                 # Global state (auth, org data)
│   │   │   └── AuthContext.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── vite.config.js
│   ├── package.json
│   └── README.md
│
├── backend/                         # Flask API (admin + data)
│   ├── app/
│   │   ├── __init__.py              # Flask app factory
│   │   ├── config.py                # Settings (DB, JWT secret, OAuth keys)
│   │   ├── models.py                # SQLAlchemy models
│   │   ├── routes/
│   │   │   ├── auth.py              # JWT + Google login routes
│   │   │   ├── users.py             # End user endpoints
│   │   │   ├── orgs.py              # Organization endpoints (CRUD)
│   │   │   └── admin.py             # Admin approval endpoints
│   │   ├── services/
│   │   │   ├── auth_service.py      # Encryption, JWT, OAuth
│   │   │   └── email_service.py     # Approval notification emails
│   │   ├── utils/
│   │   │   ├── decorators.py        # Role-based access
│   │   │   └── validators.py        # Form validation
│   │   └── db.py                    # DB initialization
│   ├── migrations/                  # Alembic or simple migration scripts
│   ├── tests/                       # Unit & integration tests
│   │   ├── test_auth.py
│   │   ├── test_orgs.py
│   │   └── test_admin.py
│   ├── requirements.txt
│   └── wsgi.py                      # Entry point for server
│
├── docs/                            # Documentation
│   ├── api_endpoints.md
│   ├── system_design.md
│   └── uml_diagrams/
│
├── .gitignore
├── docker-compose.yml               # (optional) for container setup
├── README.md
└── jira_tasks_charity_directory.csv # Import Jira tasks