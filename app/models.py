from sqlalchemy import (
    Column, Integer, String, Text, DateTime,
    LargeBinary, ForeignKey, func
)
from sqlalchemy.orm import relationship
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

    support_number = Column(
        String(30),
        unique=True,
        nullable=True,
        index=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    attachments = relationship(
        "ContactAttachment",
        back_populates="contact",
        cascade="all, delete-orphan"
    )


class ContactAttachment(Base):
    __tablename__ = "contact_attachments"

    id = Column(Integer, primary_key=True, index=True)

    contact_id = Column(
        Integer,
        ForeignKey("contacts.id", ondelete="CASCADE"),
        nullable=False
    )

    filename = Column(String(255), nullable=False)
    content_type = Column(String(100), nullable=False)
    file_data = Column(LargeBinary, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    contact = relationship(
        "Contact",
        back_populates="attachments"
    )