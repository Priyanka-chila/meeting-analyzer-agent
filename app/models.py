from typing import Literal

from pydantic import BaseModel, Field


class TopicOutput(BaseModel):

    topics: list[str] = Field(
        description="Main discussion topics"
    )


class SummaryOutput(BaseModel):

    summary: str = Field(
        description="Concise 3-5 sentence meeting summary"
    )


class ActionItem(BaseModel):

    task: str = Field(
        description="Specific task that needs to be completed"
    )

    owner: str = Field(
        description=(
            "Person responsible for the task. "
            "Use 'Not specified' if unknown."
        )
    )


class ActionItemsOutput(BaseModel):

    action_items: list[ActionItem]


class PrioritizedActionItem(BaseModel):

    task: str

    owner: str

    priority: Literal[
        "High",
        "Medium",
        "Low"
    ]


class PriorityOutput(BaseModel):

    action_items: list[PrioritizedActionItem]


class FinalReport(BaseModel):

    meeting_summary: str

    