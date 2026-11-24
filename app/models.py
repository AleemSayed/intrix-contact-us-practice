
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    phone = Column(String(30), nullable=False)
    email = Column(String(255), nullable=False)
    subject = Column(
        String(100),
        nullable=False,
        server_default="General Enquiry"
    )
    message = Column(Text, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
