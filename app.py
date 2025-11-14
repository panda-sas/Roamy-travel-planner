"""
Streamlit Frontend for Roamy - AI Travel Planner
"""
import streamlit as st
import os
from dotenv import load_dotenv
from agents.trip_planner import plan_trip, create_trip_planner_graph

# Load environment variables
# Streamlit Cloud uses st.secrets, local development uses .env
load_dotenv()

# Get API key from Streamlit secrets (production) or environment (local)
def get_api_key():
    """Get OpenAI API key from Streamlit secrets or environment."""
    try:
        # Try Streamlit secrets first (for Streamlit Cloud)
        if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
            return st.secrets['OPENAI_API_KEY']
    except:
        pass
    # Fall back to environment variable (for local development)
    return os.getenv("OPENAI_API_KEY")

# Page configuration
st.set_page_config(
    page_title="Roamy - AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-size: 1.1rem;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
    }
    .stButton>button:hover {
        background-color: #1565c0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">✈️ Roamy</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your AI-powered travel planning assistant</p>', unsafe_allow_html=True)

# Sidebar for inputs
with st.sidebar:
    st.header("📋 Trip Details")
    
    destination = st.text_input(
        "Destination",
        placeholder="e.g., Paris, France",
        help="Enter your desired travel destination"
    )
    
    dates = st.text_input(
        "Travel Dates",
        placeholder="e.g., March 15-20, 2024",
        help="Enter your travel dates"
    )
    
    budget = st.selectbox(
        "Budget Range",
        ["Budget-friendly", "Mid-range", "Luxury", "Flexible"],
        help="Select your budget preference"
    )
    
    interests = st.text_area(
        "Interests & Preferences",
        placeholder="e.g., Museums, food tours, historical sites, nightlife",
        help="Describe what you're interested in during your trip"
    )
    
    st.markdown("---")
    
    # Check API key
    api_key = get_api_key()
    if not api_key or api_key == "your_openai_api_key_here":
        st.error("⚠️ Please set your OPENAI_API_KEY")
        st.info("""
        **For Streamlit Cloud:**
        - Go to Settings → Secrets
        - Add: `OPENAI_API_KEY = "your-key-here"`
        
        **For Local Development:**
        - Create a `.env` file
        - Add: `OPENAI_API_KEY=your-key-here`
        """)
        st.stop()
    else:
        st.success("✅ API Key configured")
    
    st.markdown("---")
    st.markdown("### How it works:")
    st.markdown("""
    1. **Research**: The agent researches your destination
    2. **Planning**: Creates a detailed itinerary
    3. **Budget**: Estimates costs and provides recommendations
    4. **Finalize**: Generates your complete travel plan
    """)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🎯 Your Travel Plan")
    
    if st.button("🚀 Generate Travel Plan", type="primary"):
        if not destination or not dates:
            st.error("Please fill in at least the destination and dates.")
        else:
            with st.spinner("🧭 Planning your trip... This may take a moment."):
                try:
                    # Show progress
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("🔍 Researching destination...")
                    progress_bar.progress(25)
                    
                    status_text.text("📅 Creating itinerary...")
                    progress_bar.progress(50)
                    
                    status_text.text("💰 Estimating budget...")
                    progress_bar.progress(75)
                    
                    status_text.text("✨ Finalizing your travel plan...")
                    progress_bar.progress(90)
                    
                    # Generate the plan
                    itinerary = plan_trip(destination, dates, budget, interests or "general travel")
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Complete!")
                    
                    # Display the itinerary
                    st.markdown("---")
                    st.markdown("### 📝 Your Personalized Travel Plan")
                    st.markdown(itinerary)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Itinerary",
                        data=itinerary,
                        file_name=f"travel_plan_{destination.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.info("Please check your API key and try again.")

with col2:
    st.header("💡 Tips")
    st.markdown("""
    <div class="info-box">
    <strong>For best results:</strong>
    <ul>
    <li>Be specific about your destination</li>
    <li>Include exact dates if possible</li>
    <li>Mention your interests and preferences</li>
    <li>Specify any special requirements</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.header("🎨 Features")
    st.markdown("""
    - ✈️ Destination research
    - 📅 Day-by-day itineraries
    - 💰 Budget estimation
    - 🗺️ Activity recommendations
    - 🍽️ Restaurant suggestions
    - 🚗 Transportation tips
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 2rem;'>"
    "Roamy - Built with ❤️ using LangGraph and Streamlit"
    "</div>",
    unsafe_allow_html=True
)

