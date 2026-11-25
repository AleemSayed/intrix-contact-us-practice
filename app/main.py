
import os
import secrets
import smtplib

from email.message import EmailMessage

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form
)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Contact, ContactAttachment
from app.schemas import ContactCreate


# Create database tables that do not already exist
Base.metadata.create_all(bind=engine)


# Initialize FastAPI
app = FastAPI(title="Intrix Contact Us API")


# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


# Attachment settings
ALLOWED_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".jpg",
    ".jpeg",
    ".png",
    ".txt",
    ".csv"
}

MAX_FILES = 10
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB per file
MAX_TOTAL_SIZE = 100 * 1024 * 1024  # 100 MB combined


# Generate a unique customer support number
def generate_support_number(db: Session):

    while True:
        support_number = (
            "INTRIX-" + secrets.token_hex(4).upper()
        )

        existing = db.query(Contact).filter(
            Contact.support_number == support_number
        ).first()

        if not existing:
            return support_number


# Send confirmation email
def send_confirmation_email(
    customer_email: str,
    customer_name: str,
    support_number: str
):

    sender_email = os.getenv("SMTP_EMAIL")
    app_password = os.getenv("SMTP_APP_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))

    if not sender_email or not app_password:
        raise ValueError("Email configuration is missing")

    email_message = EmailMessage()

    email_message["Subject"] = (
        f"Your Query Has Been Received - {support_number}"
    )

    email_message["From"] = sender_email
    email_message["To"] = customer_email

    email_message.set_content(
        f"""
Dear {customer_name},

Thank you for contacting Intrix Solutions.

We have successfully received your query.

Your Customer Support Number is:

{support_number}

Please use this reference number for any future
communication regarding your enquiry.

Our team will get back to you.

Regards,
Intrix Solutions Support Team
"""
    )

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(email_message)


# Home route
@app.get("/")
def home():
    return {
        "message": "Intrix Contact API is running"
    }


# Contact form submission
@app.post("/api/contact")
async def create_contact(
    name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
    files: list[UploadFile] = File(default=[]),
    db: Session = Depends(get_db)
):

    try:

        # Validate contact information
        contact_data = ContactCreate.model_validate({
            "name": name,
            "phone": phone,
            "email": email,
            "subject": subject,
            "message": message
        })

        # Check maximum number of attachments
        if len(files) > MAX_FILES:
            raise HTTPException(
                status_code=400,
                detail="You can upload a maximum of 10 files"
            )

        # Prepare attachment data
        attachment_data = []
        total_size = 0

        for uploaded_file in files:

            if not uploaded_file.filename:
                continue

            # Clean the filename
            filename = os.path.basename(
                uploaded_file.filename.replace("\\", "/")
            )

            # Check file extension
            extension = os.path.splitext(filename)[1].lower()

            if extension not in ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail=f"File type not allowed: {filename}"
                )

            # Read at most 10 MB plus one byte
            file_content = await uploaded_file.read(
                MAX_FILE_SIZE + 1
            )

            # Check individual file size
            if len(file_content) > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"{filename} exceeds the 10 MB limit"
                )

            # Reject empty files
            if not file_content:
                raise HTTPException(
                    status_code=400,
                    detail=f"{filename} is empty"
                )

            # Calculate combined attachment size
            total_size += len(file_content)

            if total_size > MAX_TOTAL_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail="Total attachment size cannot exceed 100 MB"
                )

            attachment_data.append({
                "filename": filename,
                "content_type": (
                    uploaded_file.content_type
                    or "application/octet-stream"
                ),
                "file_data": file_content
            })

        # Generate customer support number
        support_number = generate_support_number(db)

        # Create contact record
        new_contact = Contact(
            name=contact_data.name,
            phone=contact_data.phone,
            email=str(contact_data.email),
            subject=contact_data.subject,
            message=contact_data.message,
            support_number=support_number
        )

        db.add(new_contact)
        db.flush()

        # Save attachments in PostgreSQL
        for attachment in attachment_data:

            new_attachment = ContactAttachment(
                contact_id=new_contact.id,
                filename=attachment["filename"],
                content_type=attachment["content_type"],
                file_data=attachment["file_data"]
            )

            db.add(new_attachment)

        # Save enquiry and attachments together
        db.commit()
        db.refresh(new_contact)

    except HTTPException:
        db.rollback()
        raise

    except ValidationError as error:
        db.rollback()

        raise HTTPException(
            status_code=422,
            detail=error.errors(include_context=False)
        )

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Unable to save contact details"
        )

    # Send email after successful database save
    email_sent = True

    try:

        send_confirmation_email(
            customer_email=str(contact_data.email),
            customer_name=contact_data.name,
            support_number=support_number
        )

    except Exception as error:

        email_sent = False

        print(
            f"Confirmation email failed for "
            f"{support_number}: {error}"
        )

    return {
        "success": True,
        "message": "Contact submitted successfully!",
        "contact_id": new_contact.id,
        "support_number": support_number,
        "email_sent": email_sent
    }
