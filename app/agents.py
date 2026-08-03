from app.llm import llm

from app.models import SummaryOutput, PriorityOutput, ActionItemsOutput

from app.prompts import SUMMARY_PROMPT,  PRIORITY_PROMPT, ACTION_PROMPT


def topic_node(state):
    transcript = state["transcript"]

    structured_llm = llm.with_structured_output(
        SummaryOutput
    )

    prompt = SUMMARY_PROMPT.format(
        transcript=transcript
    )

    response = structured_llm.invoke(prompt)

    return {
        "summary": response.summary
    }

def summary_node(state):

    transcript = state["transcript"]

    structured_llm = llm.with_structured_output(
        SummaryOutput
    )

    prompt = SUMMARY_PROMPT.format(
        transcript=transcript
    )

    response = structured_llm.invoke(prompt)

    return {
        "summary": response.summary
    }




def action_item_node(state):

    transcript = state["transcript"]

    structured_llm = llm.with_structured_output(
        ActionItemsOutput
    )

    prompt = ACTION_PROMPT.format(
        transcript=transcript
    )

    response = structured_llm.invoke(prompt)

    return {
        "action_items": [
            item.model_dump()
            for item in response.action_items
        ]
    }






def priority_node(state):

    transcript = state["transcript"]

    action_items = state["action_items"]

    structured_llm = llm.with_structured_output(
        PriorityOutput
    )

    prompt = PRIORITY_PROMPT.format(
        transcript=transcript,
        action_items=action_items
    )

    response = structured_llm.invoke(prompt)

    return {
        "prioritized_action_items": [
            item.model_dump()
            for item in response.action_items
        ]
    }