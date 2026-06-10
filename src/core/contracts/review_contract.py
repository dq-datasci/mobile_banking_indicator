from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

from src.core.security.anonymizer import PIIAnonymizer


class PlayStoreReviewContract(BaseModel):
    """
    Data Contract for Play Store reviews.
    Ensures that data extracted from the Play Store adheres to the expected schema
    before being ingested into the Bronze layer of the database.
    """

    reviewId: str = Field(..., description="Unique identifier for the review")
    userName: str = Field(..., description="Name of the user who posted the review")
    userImage: Optional[str] = Field(
        None, description="URL of the user's profile image"
    )
    content: Optional[str] = Field(None, description="Text content of the review")
    score: int = Field(..., description="Rating score given by the user (e.g., 1 to 5)")
    thumbsUpCount: int = Field(0, description="Number of thumbs up the review received")
    reviewCreatedVersion: Optional[str] = Field(
        None, description="App version when the review was created"
    )
    at: datetime = Field(..., description="Timestamp of the review")
    replyContent: Optional[str] = Field(
        None, description="Content of the developer's reply"
    )
    repliedAt: Optional[datetime] = Field(
        None, description="Timestamp of the developer's reply"
    )
    appVersion: Optional[str] = Field(
        None, description="Current app version of the user"
    )

    class Config:
        frozen = True  # Ensures instances are immutable

    @field_validator("userName", "userImage", mode="before")
    @classmethod
    def anonymize_pii(cls, v: Optional[str]) -> Optional[str]:
        return PIIAnonymizer.hash_sha256(v)
