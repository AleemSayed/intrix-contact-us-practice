# Intrix Contact Us Application

A full-stack Contact Us application built using **Python FastAPI, PostgreSQL, HTML, CSS and JavaScript**. The application allows users to submit contact enquiries, upload multiple attachments and receive email confirmation.

## 🚀 Features

- **Contact Form:** Collects user contact information and enquiry details.
- **Email Validation:** Validates email addresses before submission.
- **Multiple File Uploads:** Allows users to attach multiple files to their enquiries.
- **Unique Submission ID:** Generates a unique ID for every successful submission.
- **Database Integration:** Stores contact submissions and related information in PostgreSQL.
- **Email Confirmation:** Sends an email confirmation after successful submission.
- **REST API:** Backend developed using FastAPI.
- **Frontend Interface:** Built using HTML, CSS and JavaScript.

## 🛠️ Technologies Used

### Backend
- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- Psycopg2

### Frontend
- HTML
- CSS
- JavaScript

### Database
- PostgreSQL
- pgAdmin 4

### Python Libraries
- python-dotenv
- email-validator
- python-multipart

## 📁 Project Structure

```text
Intrix-Contact-us/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── styles.css
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/AleemSayed/intrix-contact-us-practice.git
```

### 2. Navigate to the Project Folder

```bash
cd intrix-contact-us-practice
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows PowerShell:

```bash
venv\Scripts\Activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create a `.env` file in the root directory and configure the required database and email credentials.

**Important:** Keep your credentials private. Never upload your `.env` file to GitHub.

### 7. Run the Application

```bash
uvicorn app.main:app --reload
```

The FastAPI development server will start locally.

## 🗄️ Database

The application uses PostgreSQL to store contact form submissions and associated information.

Database management and inspection can be performed using pgAdmin 4.

## 📎 File Uploads

The application supports multiple file attachments through the contact form. Uploaded files are handled by the backend and associated with their respective submissions.

## 📧 Email Confirmation

After a successful contact form submission, the application sends an email confirmation to the user.

## 🔗 Repository

GitHub: https://github.com/AleemSayed/intrix-contact-us-practice

## 👨‍💻 Developer

**Aleem Azhar Sayed**

Developed as a practical full-stack application to demonstrate backend development, database integration, file handling, API development and frontend integration.
