# xrwvm-fullstack_developer_capstone

**Project Name:** Cars Dealership Web Application

A full-stack web application for browsing car makes and models. This project is being developed as part of a full-stack developer capstone.

## Technologies Used

- **Frontend:** React.js, JavaScript, HTML, CSS
- **Backend:** Python, Django
- **Database:** SQLite for local development
- **Version Control:** Git and GitHub

## Features Implemented

- Manage car makes and models through Django Admin
- Populate sample car makes and models
- Retrieve car makes and models through a Django API
- Register users with duplicate-username validation
- Login and logout endpoints
- React registration page with password confirmation
- React routes for the home, login, and registration pages

## Project Structure

```text
.
├── server/
│   ├── djangoapp/
│   ├── djangoproj/
│   ├── frontend/
│   ├── manage.py
│   └── requirements.txt
├── .gitignore
└── README.md
```

## Local Development Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/jaina496/xrwvm-fullstack_developer_capstone.git
   cd xrwvm-fullstack_developer_capstone
   ```

2. Navigate to the server directory:

   ```bash
   cd server
   ```

3. Activate the virtual environment if it already exists:

   ```bash
   source djangoenv/bin/activate
   ```

4. Install the Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Apply database migrations:

   ```bash
   python3 manage.py migrate --run-syncdb
   ```

6. Start the Django development server:

   ```bash
   python3 manage.py runserver 0.0.0.0:8000
   ```

## Repository

[GitHub Repository](https://github.com/jaina496/xrwvm-fullstack_developer_capstone)

## Project Status

Development is ongoing. Additional dealership APIs, review functionality, sentiment analysis, frontend integration, and deployment tasks remain to be completed.
