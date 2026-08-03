from typing import TypedDict


class MeetingState(TypedDict):
    transcript: str
    topics: list[str]
    summary: str
    action_items: list[dict]
    priority: str
    final_report: dict