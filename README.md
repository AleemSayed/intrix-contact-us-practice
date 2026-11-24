# Intrix Contact Us Web Application

A modern, responsive Contact Us web application built using **Python, FastAPI, PostgreSQL, HTML, CSS, and JavaScript**.

The application allows users to submit enquiries through an interactive contact form. Submitted information is processed by a FastAPI backend and stored in a PostgreSQL database.

## Features

- Responsive and modern user interface
- Full Name, Phone Number and Email Address inputs
- Subject selection dropdown
- Message submission form
- Client-side form validation
- Backend API integration using FastAPI
- PostgreSQL database integration
- Automatic storage of submitted contact details
- Submission success and error messages
- Interactive button hover effects

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API development |
| PostgreSQL | Database management |
| SQLAlchemy | Database ORM |
| HTML5 | Frontend structure |
| CSS3 | Styling and responsiveness |
| JavaScript | Form handling and API communication |
| Git & GitHub | Version control |

## Project Structure

```text
Intrix-Contact-us/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
│
├── .env
├── .gitignore
└── requirements.txt
```

## How It Works

1. A user opens the Contact Us webpage.
2. The user enters their name, phone number, email address, subject and message.
3. JavaScript collects and validates the form information.
4. The frontend sends the information to the FastAPI backend through a POST request.
5. FastAPI processes the request.
6. SQLAlchemy communicates with PostgreSQL.
7. The submitted contact information is stored in the database.
8. The user receives a submission confirmation.

## API Endpoint

**POST** `/api/contact`

Accepts contact form submissions and stores the information in the PostgreSQL database.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/AleemSayed/intrix-contact-us-practice.git
```

### 2. Navigate to the project folder

```bash
cd intrix-contact-us-practice
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment (Windows)

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the database

- Install and configure PostgreSQL.
- Create the required database.
- Configure your database connection settings in the `.env` file according to `app/database.py`.

### 7. Start the backend server

```bash
uvicorn app.main:app --reload
```

The backend will run at:

`http://127.0.0.1:8000`

### 8. Launch the frontend

Open `frontend/index.html` using VS Code Live Server.

## Future Improvements

- Email notifications after successful submissions
- Admin dashboard to manage enquiries
- Search and filter submitted contacts
- Deployment to a cloud hosting platform

## Author

**Aleem Sayed**

GitHub: [AleemSayed](https://github.com/AleemSayed)

---

*Built as a practical full-stack web development project to explore frontend development, REST API integration, backend processing and relational database management.*
