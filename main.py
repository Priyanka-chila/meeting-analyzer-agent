
from app.workflow  import build_graph


graph = build_graph()


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

Product Manager: Please prioritize this issue today.

Mobile Developer: I will review the Android login module.

QA Tester: I will prepare a detailed bug report.

Backend Developer: I will verify the authentication API.

Mobile Developer: I will also add better error handling.

"""


initial_state = {

    "transcript": transcript,

    "topics": [],

    "summary": "",

    "action_items": [],

    "prioritized_action_items": [],

    "final_report": {}
}


result = graph.invoke(
    initial_state
)


print("\n==============================")
print("FINAL REPORT")
print("==============================")

print(
    result["final_report"]
)