from app.models import FinalReport
from app.state import MeetingState

def check_action_items(state: MeetingState) -> str  :

    if not state["action_items"]:

        return "no_actions"

    return "has_actions"


def final_output_node(state: MeetingState) -> dict:
    


    summary = state["summary"] if "summary" in state else "No summary available"
    report = FinalReport(

        meeting_summary=summary,

        
    )

    # report = state["final_report"]
    return {
        "final_report": report.model_dump()
    }