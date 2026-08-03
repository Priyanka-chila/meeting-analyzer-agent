import os

from typing import TypedDict

from dotenv import load_dotenv

from pydantic import BaseModel, Field

from langchain_google_genai import ChatGoogleGenerativeAI

from langgraph.graph import StateGraph, START, END
from google import genai
from models import TopicOutput, SummaryOutput, ActionItem, ActionItemsOutput
# ==================================================
# 1. Load environment variables
# ==================================================

load_dotenv()

# client = genai.Client(
#     api_key=os.getenv("GOOGLE_API_KEY")
# )

# for model in client.models.list():
#     print(model.name)
# ==================================================
# 2. LangGraph State
# ==================================================

class MeetingState(TypedDict):

    transcript: str

    topics: list[str]

    summary: str

    action_items: list[dict]

    priority: str

    final_report: dict


# ==================================================
# 3. Pydantic Schema
# ==================================================

class TopicOutput(BaseModel):

    topics: list[str] = Field(
        description="Main discussion topics identified from the meeting"
    )


# ==================================================
# 4. Gemini Model
# ==================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0
)


# ==================================================
# 5. Structured Gemini
# ==================================================

structured_llm = llm.with_structured_output(
    TopicOutput
)


# ==================================================
# 5. Topic Agent
# ==================================================

def topic_node(state: MeetingState):

    transcript = state["transcript"]

    structured_llm = llm.with_structured_output(
        TopicOutput
    )

    prompt = f"""
You are an expert meeting topic extraction agent.

Analyze the meeting transcript below.

Identify the main discussion topics.

Rules:

- Return meaningful topics only.
- Don't return complete sentences.
- Don't invent information.
- Avoid duplicate topics.
- Keep topics concise.
- Return between 3 and 10 topics.

Meeting Transcript:

{transcript}
"""

    response = structured_llm.invoke(prompt)

    return {
        "topics": response.topics
    }


# ==================================================
# 6. Summary Agent
# ==================================================

def summary_node(state: MeetingState):

    transcript = state["transcript"]

    structured_llm = llm.with_structured_output(
        SummaryOutput
    )

    prompt = f"""
You are an expert meeting summarization agent.

Analyze the following meeting transcript.

Generate a concise summary in 3 to 5 sentences.

Rules:

- Explain what the meeting was about.
- Mention the main problem or objective.
- Mention important findings or decisions.
- Mention important next steps if discussed.
- Do not invent information.
- Do not list every individual action item.
- Keep the summary concise.

Meeting Transcript:

{transcript}
"""

    response = structured_llm.invoke(prompt)

    return {
        "summary": response.summary
    }

def action_item_node(state: MeetingState):

    transcript = state["transcript"]

    structured_llm = llm.with_structured_output(
        ActionItemsOutput
    )

    prompt = f"""
You are an expert meeting action-item extraction agent.

Analyze the meeting transcript and identify all tasks
that participants agreed to perform.

For every action item extract:

1. Task description
2. Person responsible

Rules:

- Only identify actual tasks or commitments.
- Do not treat general discussion as an action item.
- Do not invent tasks.
- If a person explicitly says "I will", they are the owner.
- If the owner cannot be determined, use "Not specified".
- Keep task descriptions concise.
- Avoid duplicate tasks.
- Include follow-up tasks and testing tasks.
- Preserve important deadlines in the task description.

Meeting Transcript:

{transcript}
"""

    response = structured_llm.invoke(prompt)

    return {
        "action_items": [
            item.model_dump()
            for item in response.action_items
        ]
    }

def priority_node(state: MeetingState):

    transcript = state["transcript"]

    action_items = state["action_items"]

    structured_llm = llm.with_structured_output(
        PriorityOutput
    )

    prompt = f"""
You are an expert project management priority classification agent.

Analyze the meeting transcript and action items.

Assign a priority to every action item.

Allowed priorities:

- High
- Medium
- Low

Priority rules:

HIGH:
Use High when the task is urgent, critical, blocking,
customer-impacting, or has an immediate deadline.

Examples:
- urgent
- ASAP
- immediately
- today
- within the next hour
- by tomorrow
- critical
- blocking
- customers cannot access accounts

MEDIUM:
Use Medium when the task is important but does not
require immediate action.

LOW:
Use Low when the task is useful but not urgent.

Important:
- Do not invent deadlines.
- Use the transcript as evidence.
- Preserve the original task and owner.
- Every action item must receive a priority.

Meeting Transcript:

{transcript}

Action Items:

{action_items}
"""

    response = structured_llm.invoke(prompt)

    return {
        "action_items": [
            item.model_dump()
            for item in response.action_items
        ]
    }

def check_action_items(state: MeetingState):

    if not state["action_items"]:
        return "no_actions"

    return "has_actions"


def final_output_node(state: MeetingState):

    if not state["action_items"]:

        return {
            "final_report": {
                "meeting_summary": state["summary"],
                "key_topics": state["topics"],
                "message": "No action items identified in this meeting."
            }
        }

    return {
        "final_report": {
            "meeting_summary": state["summary"],
            "key_topics": state["topics"],
            "action_items": state["action_items"]
        }
    }
# ==================================================
# 7. Create Graph
# ==================================================

builder = StateGraph(MeetingState)


builder.add_node(
    "topic_agent",
    topic_node
)

builder.add_node(
    "summary_agent",
    summary_node
)

builder.add_node(
    "action_item_agent",
    action_item_node
)

builder.add_node(
    "priority_agent",
    priority_node
)

builder.add_node(
    "final_output_agent",
    final_output_node
)

# ==================================================
# 8. Edges
# ==================================================

builder.add_edge(
    START,
    "topic_agent"
)

builder.add_edge(
    "topic_agent",
    "summary_agent"
)

builder.add_edge(
    "summary_agent",
    "action_item_agent"
)


builder.add_conditional_edges(
    "action_item_agent",
    check_action_items,
    {
        "no_actions": "final_output_agent",
        "has_actions": "priority_agent"
    }
)

# builder.add_edge(
#     "action_item_agent",
#     "priority_agent"
# )

builder.add_edge(
    "priority_agent",
    "final_output_agent"
)

builder.add_edge(
    "final_output_agent",
    END
)



# ==================================================
# 9. Compile
# ==================================================

graph = builder.compile()


# ==================================================
# 10. Transcript
# ==================================================

transcript = """
Product Manager: Good morning everyone. We have received
several complaints about the mobile app crashing during login.

Customer Support Lead: Yes, our support team received more
than 120 complaints in the last two days.

Product Manager: That is quite serious. We need to identify
the root cause quickly.

Mobile Developer: I checked some of the crash logs yesterday
and noticed that most of the issues are coming from Android users.

QA Tester: I also tried reproducing the issue on an Android
device and the app crashed right after entering login credentials.

Backend Developer: Could the issue be related to the
authentication API?

Mobile Developer: That is possible. The login request might
be failing due to some recent backend changes.

Product Manager: When was the last update deployed to production?

Backend Developer: We deployed a small update to the
authentication service three days ago.

QA Tester: The crash reports also started appearing around
the same time.

Mobile Developer: I suspect the issue might be related to
how the mobile app handles the API response.

Backend Developer: Let me check whether the API response
format has changed.

Product Manager: Good idea. We need to investigate both the
mobile and backend components.

Customer Support Lead: Customers are getting frustrated
because they cannot access their accounts.

Product Manager: Yes, we must resolve this issue urgently.

Mobile Developer: I will review the Android login module
and check if any error handling is missing.

QA Tester: I will prepare a detailed bug report with
screenshots and logs.

Backend Developer: I will verify the authentication API
and check if there are any breaking changes.

Product Manager: Please prioritize this issue today.
"""


# ==================================================
# 11. Initial State
# ==================================================

initial_state = {

    "transcript": transcript,

    "topics": [],

    "summary": "",

    "action_items": [],

    "priority": "",

    "final_report": {}
}


# ==================================================
# 12. Execute
# ==================================================

result = graph.invoke(
    initial_state
)


# ==================================================
# 13. Display
# ==================================================

print("\n==============================")
print("KEY TOPICS")
print("==============================")

for topic in result["topics"]:
    print("-", topic)


print("\n==============================")
print("MEETING SUMMARY")
print("==============================")

print(result["summary"])