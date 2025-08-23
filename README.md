# Charity Directory

A platform for users and organizations to connect and manage charity data.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/directory-for-charities.git
cd directory-for-charities
```

---

### 2. Install & Run the Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```
- The frontend will be available at [http://localhost:5173/](http://localhost:5173/).

---

### 3. Install & Run the Backend (Flask)

```bash
cd ../backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```
- The backend will be available at [http://localhost:5000/](http://localhost:5000/).

---

### 4. Development Notes

- Make sure you have Node.js (v20.19+ or v22.12+) and Python 3.8+ installed.
- The frontend is set up to proxy API requests to the backend during development.
- Update environment variables and configuration files as needed.

---

## Folder Structure

See [FolderStructure.md](FolderStructure.md) for details.
