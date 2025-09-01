from pydantic import BaseModel


class UserPrompt(BaseModel):
    """Schema for user prompt input."""

    user_prompt: str | None = None


class TechDescriptionMetadata(BaseModel):
    """Schema for tech description metadata."""

    topic: str
    tech_stack: str
    difficulty: str
    tags: str


class TechDescription(BaseModel):
    """Schema for tech description input."""

    description: str
    metadata: TechDescriptionMetadata
