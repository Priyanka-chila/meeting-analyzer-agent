from langgraph.graph import (
    StateGraph,
    START,
    END
)

from app.state import MeetingState
from app.agents import (
    topic_node,
    summary_node,
    action_item_node,
    priority_node
)

from app.nodes import (
    check_action_items,
    final_output_node
)


def build_graph():

    builder = StateGraph(
        MeetingState
    )


    # Nodes

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
        "final_output",
        final_output_node
    )


    # START → Topic

    builder.add_edge(
        START,
        "topic_agent"
    )


    # Topic → Summary

    builder.add_edge(
        "topic_agent",
        "summary_agent"
    )


    # Summary → Action

    builder.add_edge(
        "summary_agent",
        "action_item_agent"
    )


    # Conditional routing

    builder.add_conditional_edges(

        "action_item_agent",

        check_action_items,

        {
            "no_actions": "final_output",

            "has_actions": "priority_agent"
        }
    )


    # Priority → Final

    builder.add_edge(
        "priority_agent",
        "final_output"
    )


    # Final → END

    builder.add_edge(
        "final_output",
        END
    )


    return builder.compile()