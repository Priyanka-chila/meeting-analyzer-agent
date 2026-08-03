import streamlit as st

from app.workflow import build_graph


st.set_page_config(
    page_title="AI Meeting Notes Analyzer",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 AI Meeting Notes Analyzer")

st.write(
    "Convert meeting transcripts into structured "
    "meeting notes using Gemini + LangGraph."
)


@st.cache_resource
def get_graph():

    return build_graph()


graph = get_graph()


transcript = st.text_area(
    "Paste your meeting transcript",
    height=400,
    placeholder=(
        "John: We need to improve the website performance.\n"
        "Sarah: Page load time is too slow.\n"
        "David: I will optimize the database queries."
    )
)


analyze_button = st.button(
    "🚀 Analyze Meeting",
    type="primary"
)


if analyze_button:

    if not transcript.strip():

        st.warning(
            "Please enter a meeting transcript."
        )

        st.stop()


    initial_state = {

        "transcript": transcript,

        "topics": [],

        "summary": "",

        "action_items": [],

        "prioritized_action_items": [],

        "final_report": {}
    }


    try:

        with st.spinner(
            "Analyzing meeting transcript..."
        ):

            result = graph.invoke(
                initial_state
            )


        report = result[
            "final_report"
        ]


        # Summary

        st.subheader(
            "📝 Meeting Summary"
        )

        st.write(
            report["meeting_summary"]
        )


        # Topics

        st.subheader(
            "🎯 Key Topics"
        )

        for topic in report[
            "key_topics"
        ]:

            st.markdown(
                f"- {topic}"
            )


        # Overall Priority

        st.subheader(
            "🔥 Overall Priority"
        )

        overall_priority = report[
            "overall_priority"
        ]


        if overall_priority == "High":

            st.error(
                f"Overall Priority: "
                f"{overall_priority}"
            )

        elif overall_priority == "Medium":

            st.warning(
                f"Overall Priority: "
                f"{overall_priority}"
            )

        elif overall_priority == "Low":

            st.success(
                f"Overall Priority: "
                f"{overall_priority}"
            )

        else:

            st.info(
                "No action items identified."
            )


        # Actions

        st.subheader(
            "✅ Action Items"
        )


        action_items = report[
            "action_items"
        ]


        if not action_items:

            st.info(
                "No action items identified "
                "in this meeting."
            )


        for index, item in enumerate(
            action_items,
            start=1
        ):

            with st.container(
                border=True
            ):

                st.markdown(
                    f"### {index}. "
                    f"{item['task']}"
                )

                st.write(
                    f"**Owner:** "
                    f"{item['owner']}"
                )


                priority = item[
                    "priority"
                ]


                if priority == "High":

                    st.error(
                        f"Priority: {priority}"
                    )

                elif priority == "Medium":

                    st.warning(
                        f"Priority: {priority}"
                    )

                else:

                    st.success(
                        f"Priority: {priority}"
                    )


    except Exception as e:

        st.error(
            "An error occurred while "
            "analyzing the meeting."
        )

        st.exception(e)