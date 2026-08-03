from app.models import FinalReport


def check_action_items(state):

    if not state["action_items"]:

        return "no_actions"

    return "has_actions"


def final_output_node(state):

    action_items = state[
        "prioritized_action_items"
    ]

    if not action_items:

        report = FinalReport(

            meeting_summary=state["summary"],

            key_topics=state["topics"],

            action_items=[],

            overall_priority="No Action Items",

            message=(
                "No action items identified "
                "in this meeting."
            )
        )

        return {
            "final_report": report.model_dump()
        }


    priorities = [
        item["priority"]
        for item in action_items
    ]


    if "High" in priorities:

        overall_priority = "High"

    elif "Medium" in priorities:

        overall_priority = "Medium"

    else:

        overall_priority = "Low"


    report = FinalReport(

        meeting_summary=state["summary"],

        key_topics=state["topics"],

        action_items=action_items,

        overall_priority=overall_priority
    )


    return {
        "final_report": report.model_dump()
    }