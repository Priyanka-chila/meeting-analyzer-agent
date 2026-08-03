TOPIC_PROMPT = """
You are an expert meeting topic extraction agent.

Analyze the meeting transcript below.

Identify the main discussion topics.

Rules:

- Return meaningful topics only.
- Do not return complete sentences.
- Do not invent information.
- Avoid duplicate topics.
- Keep topics concise.
- Return between 3 and 10 topics.

Meeting Transcript:

{transcript}
"""


SUMMARY_PROMPT = """
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

ACTION_PROMPT = """
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
- Include follow-up and testing tasks.
- Preserve important deadlines in the task description.

Meeting Transcript:

{transcript}
"""


PRIORITY_PROMPT = """
You are an expert project management priority
classification agent.

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