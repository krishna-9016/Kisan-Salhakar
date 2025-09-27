# backend/app/models.py

from pydantic import BaseModel, Field
from typing import List, Optional

class QueryRequest(BaseModel):
    """
    Defines the structure for an incoming chat query from the user.
    """
    query: str = Field(
       ...,  # '...' makes this field required.
        title="User Query",
        description="The question asked by the user in Punjabi.",
        min_length=1,

        max_length=500
    )
    session_id: Optional[str] = Field(
        None,
        title="Session ID",
        description="An optional ID to track conversation history (for future use)."
    )

class ChatResponse(BaseModel):
    """
    Defines the structure for the response sent back to the user.
    """
    answer: str = Field(
       ...,
        title="AI's Answer",
        description="The generated answer from the conversational AI."
    )
    retrieved_context: List[str] = Field(
        default_factory=list,
        title="Retrieved Context",
        description="A list of the source text chunks used to generate the answer. Useful for verification and debugging."
    )