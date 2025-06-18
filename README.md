
# Flask Supabase Auth API

This is a simple Flask project that handles user authentication with Supabase as the database backend and JWT for token-based authentication.  
Swagger UI is provided via **Flasgger**.

## 📌 Features

- Flask-based REST API
- Supabase Postgres database connection
- JWT authentication (Bearer Token)
- Swagger UI using Flasgger
- Data validation using **Pydantic** for request payloads
- Automatic code formatting and linting with **Ruff**
- Environment variable configuration via `.env`
- Modular project structure with Blueprints

## 📂 Project Structure

```
.
├── app/
│   ├── api/                # Flask Blueprints (routes)
│   │   ├── auth_routes.py
│   │   └── user_routes.py
│   ├── auth/               # Auth logic and helpers
│   │   ├── auth_utils.py
│   │   └── auth_service.py
│   ├── core/               # Configs, DB connection, etc.
│   │   ├── config.py
│   │   └── db.py
│   └── services/           # Business logic (other services)
│       └── other_service.py
├── main.py                 # App entry point
├── requirements.txt
├── pyproject.toml          # If using Poetry
├── uv.lock                 # uv lock file
├── .env                    # (Not committed)
├── .gitignore
└── ruff.toml               # Ruff configuration
```

## 🚀 Running the project locally

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```
*(Or use Poetry if you prefer)*

2. **Configure environment variables:**

Rename the `.env.example` file to `.env` at the project root and fill in your Supabase database connection details and JWT secret:

```
SUPABASE_HOST=your_host
SUPABASE_PORT=5432
SUPABASE_DB=your_db
SUPABASE_USER=your_user
SUPABASE_PASSWORD=your_password
JWT_SECRET=your_jwt_secret
```

3. **Run the Flask server:**

```bash
python main.py
```

Then access Swagger UI at:  
[http://localhost:5000/apidocs/](http://localhost:5000/apidocs/)

## ✅ Development Tools and Code Quality

- **Data Validation:**  
  All incoming JSON payloads (like login and signup requests) are validated using **Pydantic**, ensuring field types and value constraints (e.g., email formats, string lengths).

- **Linting and Formatting:**  
  This project uses **Ruff** for automatic code formatting, linting, and organizing imports.  
  The VS Code settings include:

```json
{
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
}
```

- **Ruff Configuration:**  
  Found in `ruff.toml`, including formatting preferences (e.g., line length, quote style) and lint rule selections.

## ✅ Project Todo List

- [x] Data validation and serialization using Pydantic
- [ ] Save login attempts and failed login logs (for security monitoring) 

## ✅ License

MIT (or your preferred license)
