from pydantic import BaseModel, Field
from typing import  Literal, Optional, Annotated
from datetime import datetime
from uuid import UUID


class Ticket(BaseModel):
    """Immutable raw customer ticket as received from the user.
    This record is append-only and must never be modified after creation."""    
    id: Annotated[UUID, Field(..., description="Unique identifier for the ticket")]
    raw_text: Annotated[str, Field(..., description="Raw text of the ticket")]
    created_at: Annotated[datetime, Field(..., description="Timestamp when the ticket was created")]


class TicketSummary(BaseModel):
    """Human-facing summary of the raw ticket text.
    Used only to reduce reading time, not for decision-making."""
    ticket_id: Annotated[UUID, Field(..., description="Unique identifier for the ticket")]
    summary: Annotated[str, Field(..., description="Summary of the ticket")]
    confidence: Annotated[
    float,
    Field(
        ...,
        description=(
            "Confidence that the summary faithfully represents the raw ticket text. "
            "Probability in the range [0.0, 1.0]. "
            "This is NOT a decision confidence."
            ),
        ),
    ]
    created_at: Annotated[datetime, Field(..., description="Timestamp when the summary was created")]


class DecisionProposal(BaseModel):
    """AI-proposed decision and draft response based solely on the ticket text.
    This is a recommendation only; humans always make the final decision."""
    ticket_id: Annotated[UUID, Field(..., description="Unique identifier for the ticket")]  
    decision: Annotated[Literal["approve", "deny", "cant_decide"], Field(..., description="Decision made on the ticket")]
    confidence: Annotated[
    float,
    Field(
        ...,
        description=(
            "Probability in the range [0.0, 1.0] that a human reviewer will agree "
            "with this proposed decision without making changes."
        ),
    ),
    ]
    reason_codes: Annotated[list[str], Field(..., description="Reason codes for the decision")]
    response_draft: Annotated[str, Field(..., description="Draft response for the decision")]
    created_at: Annotated[datetime, Field(..., description="Timestamp when the proposal was created")]

class HumanFeedback(BaseModel):
    """Human reviewer action on an AI proposal.
    Multiple feedback records may exist for the same ticket."""
    ticket_id: Annotated[UUID, Field(..., description="Unique identifier for the ticket")]
    action: Annotated[Literal["approved", "edited", "rejected"], Field(..., description="Action taken by the human")]
    confidence_at_time: Annotated[
    float,
    Field(
        ...,
        description=(
            "Confidence value associated with the AI proposal at the time "
            "the human feedback was recorded. Range [0.0, 1.0]."
        ),
    ),
    ]   
    rejection_reason: Annotated[Optional[str], Field(description="Reason for rejection if applicable; required when action == 'rejected'")] = None
    edited_diff: Optional[str] = None
    created_at: Annotated[datetime, Field(..., description="Timestamp when the feedback was created")]
