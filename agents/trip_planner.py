"""
LangGraph-based Trip Planner Agent
"""
from typing import TypedDict, Annotated, Sequence, Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()

# Define the state structure
class TripPlannerState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    destination: str
    dates: str
    budget: str
    interests: str
    itinerary: str
    research_complete: bool
    planning_complete: bool


# Initialize the LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

# Define tools for the agent
@tool
def research_destination(destination: str, interests: str) -> str:
    """Research a destination and provide information about attractions, weather, culture, and activities."""
    # In a real implementation, this would call external APIs
    # For now, we'll use the LLM to generate research
    research_prompt = f"""
    Research the destination: {destination}
    User interests: {interests}
    
    Provide information about:
    1. Top attractions and must-see places
    2. Best time to visit and weather conditions
    3. Local culture and customs
    4. Recommended activities based on interests
    5. Transportation options
    6. Safety considerations
    
    Format the response in a clear, organized manner.
    """
    response = llm.invoke([HumanMessage(content=research_prompt)])
    return response.content


@tool
def estimate_budget(destination: str, dates: str, interests: str) -> str:
    """Estimate the budget for a trip including accommodation, food, activities, and transportation."""
    budget_prompt = f"""
    Estimate the budget for a trip to {destination} from {dates}.
    User interests: {interests}
    
    Provide a breakdown of estimated costs:
    1. Accommodation (per night)
    2. Food and dining (per day)
    3. Activities and attractions
    4. Transportation (local and to/from destination)
    5. Miscellaneous expenses
    
    Provide both budget-friendly and mid-range options.
    Format as a clear budget breakdown.
    """
    response = llm.invoke([HumanMessage(content=budget_prompt)])
    return response.content


@tool
def generate_itinerary(destination: str, dates: str, interests: str, research: str = "") -> str:
    """Generate a detailed day-by-day itinerary based on research and user preferences.
    
    Args:
        destination: The travel destination
        dates: Travel dates
        interests: User interests and preferences
        research: Optional research information about the destination
    """
    itinerary_prompt = f"""
    Create a detailed day-by-day itinerary for a trip to {destination} from {dates}.
    
    User interests: {interests}
    Research information: {research if research else 'General destination information'}
    
    Create a comprehensive itinerary that includes:
    1. Day-by-day schedule with times
    2. Specific attractions and activities
    3. Restaurant recommendations
    4. Transportation between locations
    5. Tips and recommendations
    
    Make it realistic and enjoyable, considering travel time and rest.
    """
    response = llm.invoke([HumanMessage(content=itinerary_prompt)])
    return response.content


# Create tool node
tools = [research_destination, estimate_budget, generate_itinerary]
tool_node = ToolNode(tools)

# Define agent nodes
def research_node(state: TripPlannerState) -> TripPlannerState:
    """Research the destination and gather information."""
    messages = state["messages"]
    
    if not state.get("research_complete", False):
        research_prompt = f"""
        You are a travel research agent. Research the destination: {state.get('destination', 'unknown')}
        User interests: {state.get('interests', 'general travel')}
        
        Use the research_destination tool to gather comprehensive information about:
        - Top attractions and must-see places
        - Best time to visit and weather conditions
        - Local culture and customs
        - Recommended activities based on interests
        - Transportation options
        - Safety considerations
        """
        
        research_agent = llm.bind_tools(tools)
        response = research_agent.invoke([SystemMessage(content=research_prompt)] + messages)
        messages = messages + [response]
    
    return {
        **state,
        "messages": messages,
        "research_complete": True
    }


def planning_node(state: TripPlannerState) -> TripPlannerState:
    """Generate the itinerary and budget plan."""
    messages = state["messages"]
    
    if not state.get("planning_complete", False):
        # Extract research from tool results in messages
        research_text = ""
        for msg in reversed(messages):
            # Look for tool results (ToolMessage or AIMessage with tool results)
            if isinstance(msg, AIMessage):
                # Check if this is a tool result message
                if "Research results" in msg.content or "research" in msg.content.lower():
                    research_text = msg.content
                    break
        
        planning_prompt = f"""
        You are a travel planning agent. Create a comprehensive travel plan for:
        Destination: {state.get('destination', 'unknown')}
        Dates: {state.get('dates', 'unknown')}
        Budget: {state.get('budget', 'flexible')}
        Interests: {state.get('interests', 'general travel')}
        
        Review the research information from previous messages and use the estimate_budget tool first to estimate costs, 
        then use generate_itinerary to create a detailed day-by-day plan.
        When calling generate_itinerary, pass the research information you found in the previous messages.
        """
        
        planner_agent = llm.bind_tools(tools)
        response = planner_agent.invoke([SystemMessage(content=planning_prompt)] + messages)
        messages = messages + [response]
    
    return {
        **state,
        "messages": messages,
        "planning_complete": True
    }


def finalize_node(state: TripPlannerState) -> TripPlannerState:
    """Finalize the trip plan and format the output."""
    messages = state["messages"]
    
    # Collect all relevant information from messages
    all_content = []
    for msg in messages:
        if isinstance(msg, AIMessage):
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                continue  # Skip tool call messages
            all_content.append(msg.content)
        elif isinstance(msg, HumanMessage):
            all_content.append(f"User: {msg.content}")
    
    context = "\n\n".join(all_content[-10:])  # Get last 10 messages for context
    
    finalize_prompt = f"""
    You are a travel planning assistant. Review all the information gathered and create a final,
    well-formatted travel plan that includes:
    1. Destination overview
    2. Budget breakdown
    3. Detailed day-by-day itinerary
    4. Tips and recommendations
    
    Based on the following information:
    {context}
    
    Format it beautifully and make it easy to read. Use markdown formatting with headers, lists, and clear sections.
    """
    
    final_response = llm.invoke([SystemMessage(content=finalize_prompt)])
    messages = messages + [final_response]
    
    # Extract itinerary from the final response
    itinerary = final_response.content
    
    return {
        **state,
        "messages": messages,
        "itinerary": itinerary
    }


# Helper function to check if agent should continue
def should_continue(state: TripPlannerState) -> Literal["tools", "end"]:
    """Check if we should call tools or end."""
    messages = state["messages"]
    last_message = messages[-1]
    # If there are tool calls, route to tools
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    # Otherwise, we're done
    return "end"


# Build the graph
def create_trip_planner_graph():
    """Create the LangGraph workflow for trip planning."""
    workflow = StateGraph(TripPlannerState)
    
    # Add nodes
    workflow.add_node("research", research_node)
    workflow.add_node("research_tools", tool_node)
    workflow.add_node("planning", planning_node)
    workflow.add_node("planning_tools", tool_node)
    workflow.add_node("finalize", finalize_node)
    
    # Define the flow
    workflow.set_entry_point("research")
    
    # Research flow with conditional tool routing
    workflow.add_conditional_edges(
        "research",
        should_continue,
        {
            "tools": "research_tools",
            "end": "planning"
        }
    )
    workflow.add_edge("research_tools", "planning")
    
    # Planning flow with conditional tool routing
    workflow.add_conditional_edges(
        "planning",
        should_continue,
        {
            "tools": "planning_tools",
            "end": "finalize"
        }
    )
    workflow.add_edge("planning_tools", "finalize")
    
    workflow.add_edge("finalize", END)
    
    # Compile the graph
    app = workflow.compile()
    return app


# Main function to run the planner
def plan_trip(destination: str, dates: str, budget: str, interests: str) -> str:
    """Main function to plan a trip."""
    app = create_trip_planner_graph()
    
    initial_state = {
        "messages": [HumanMessage(content=f"I want to plan a trip to {destination} from {dates}. My budget is {budget} and I'm interested in {interests}.")],
        "destination": destination,
        "dates": dates,
        "budget": budget,
        "interests": interests,
        "itinerary": "",
        "research_complete": False,
        "planning_complete": False
    }
    
    # Run the graph
    final_state = app.invoke(initial_state)
    
    return final_state.get("itinerary", "No itinerary generated")

