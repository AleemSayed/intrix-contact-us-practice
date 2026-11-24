
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Contact
from app.schemas import ContactCreate

# Create database tables
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



@app.get("/")
def home():
    return {"message": "Intrix Contact API is running"}


@app.post("/api/contact")
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db)
):
    try:
        new_contact = Contact(
            name=contact.name,
            phone=contact.phone,
            email=contact.email,
            subject=contact.subject,
            message=contact.message
        )

        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)

        return {
            "success": True,
            "message": "Contact submitted successfully!",
            "contact_id": new_contact.id
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to save contact details"
        )
