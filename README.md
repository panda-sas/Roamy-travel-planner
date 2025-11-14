# Roamy - AI Travel Planner

**Roamy** is a sophisticated trip planning agent built with **LangGraph** that helps users create personalized travel itineraries. This project replaces CrewAI with LangGraph to create a multi-agent workflow for comprehensive trip planning.

## Features

- **Destination Research**: Analyzes user preferences and researches destinations
- **Itinerary Generation**: Creates detailed day-by-day travel plans with specific times and activities
- **Budget Planning**: Estimates costs and provides budget breakdowns
- **Interactive Frontend**: Beautiful Streamlit-based web interface
- **LangGraph Workflow**: Multi-node agent system with tool execution

## Architecture

The application uses **LangGraph** to create a multi-agent workflow with the following nodes:

1. **Research Node**: 
   - Uses `research_destination` tool to gather comprehensive destination information
   - Collects data on attractions, weather, culture, transportation, and safety

2. **Planning Node**: 
   - Uses `estimate_budget` tool to calculate trip costs
   - Uses `generate_itinerary` tool to create day-by-day schedules
   - Integrates research data into the planning process

3. **Finalize Node**: 
   - Synthesizes all information into a well-formatted travel plan
   - Creates a comprehensive document with destination overview, budget, itinerary, and tips

### Workflow Graph

```
User Input → Research Node → [Tool: research_destination] → Planning Node 
→ [Tool: estimate_budget] → [Tool: generate_itinerary] → Finalize Node → Output
```

## Setup

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone or navigate to the project directory:**
```bash
cd fun-trials/travel-planner
```

2. **Create a virtual environment (recommended):**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
# Create .env file
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
# Or manually create .env and add your key
```

### Running the Application

**Option 1: Using the run script (recommended)**
```bash
./run.sh
```

**Option 2: Manual start**
```bash
streamlit run app.py
```

**Option 3: Test with example script**
```bash
python example.py
```

The Streamlit app will open in your default browser at `http://localhost:8501`

## Usage

### Web Interface

1. Open the Streamlit app in your browser
2. Fill in the sidebar with:
   - **Destination**: e.g., "Paris, France"
   - **Travel Dates**: e.g., "March 15-20, 2024"
   - **Budget Range**: Select from dropdown (Budget-friendly, Mid-range, Luxury, Flexible)
   - **Interests & Preferences**: e.g., "Museums, food tours, historical sites"
3. Click "🚀 Generate Travel Plan"
4. Wait for the agent to process (research → planning → finalization)
5. Review your personalized travel plan
6. Download the itinerary as a text file if desired

### Programmatic Usage

```python
from agents.trip_planner import plan_trip

itinerary = plan_trip(
    destination="Tokyo, Japan",
    dates="March 15-22, 2024",
    budget="Mid-range",
    interests="Technology, food, temples"
)
print(itinerary)
```

## Project Structure

```
travel-planner/
├── agents/
│   ├── __init__.py
│   └── trip_planner.py      # LangGraph agent implementation
├── app.py                    # Streamlit frontend
├── example.py                # Example usage script
├── requirements.txt          # Python dependencies
├── run.sh                    # Quick start script
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker Compose setup
├── Procfile                  # Heroku deployment config
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── DEPLOYMENT.md             # Deployment guide
├── README.md                 # This file
└── .env                      # Environment variables (create this)
```

## Key Technologies

- **LangGraph**: For building the agent workflow graph
- **LangChain**: For LLM integration and tool definitions
- **OpenAI GPT-4**: For natural language processing
- **Streamlit**: For the web interface

## Customization

### Adding New Tools

You can extend the agent by adding new tools in `agents/trip_planner.py`:

```python
@tool
def your_custom_tool(param: str) -> str:
    """Your tool description."""
    # Your implementation
    return result
```

Then add it to the `tools` list and the agent will automatically use it.

### Modifying the Workflow

Edit `create_trip_planner_graph()` in `agents/trip_planner.py` to:
- Add new nodes
- Change the workflow order
- Add conditional routing
- Modify state structure

## Deployment

Roamy can be deployed to production using various platforms. See **[DEPLOYMENT.md](DEPLOYMENT.md)** for detailed deployment guides including:

- 🚀 **Streamlit Cloud** (Easiest - Recommended)
- 🐳 **Docker** (Railway, Render, Fly.io)
- ☁️ **Heroku**
- 🌐 **AWS/Azure/GCP**
- 💻 **VPS** (DigitalOcean, Linode, etc.)

### Quick Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add `OPENAI_API_KEY` in Secrets
5. Deploy! ✨

For detailed instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## Troubleshooting

**Issue**: "OPENAI_API_KEY not found"
- Solution: Make sure you've created a `.env` file with your API key

**Issue**: Import errors
- Solution: Make sure all dependencies are installed: `pip install -r requirements.txt`

**Issue**: Tool execution errors
- Solution: Check that your OpenAI API key has access to the required models

**Issue**: Deployment errors
- Solution: Check [DEPLOYMENT.md](DEPLOYMENT.md) for platform-specific troubleshooting

## License

This project is for educational and personal use.

## Contributing

Feel free to extend this project with:
- Integration with real travel APIs (flights, hotels, weather)
- Multi-destination planning
- Collaborative planning features
- Export to different formats (PDF, calendar)

