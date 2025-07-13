from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum

class LinkPrecedence(str, Enum):
    primary = "primary"
    secondary = "secondary"

class Contact(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    phoneNumber: str | None = Field(default=None, nullable=True)
    email: str | None = Field(default=None, nullable=True)
    linkedId: int | None = Field(default=None, nullable=True)
    linkPrecedence: LinkPrecedence = Field(default=LinkPrecedence.primary)
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)
    deletedAt: datetime | None = Field(default=None, nullable=True)

class ContactCreate(BaseModel):
    phoneNumber: str | None = None
    email: str | None = None

class IdentificationModel(BaseModel):
    primaryContactId: int
    emails: list[str]
    phoneNumbers: list[str]
    secondaryContactIds: list[int]