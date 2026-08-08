# langchain-tool-agent

A series of LangChain + Mistral AI projects exploring tool-calling agents — from a simple news summarizer to manual tool selection to a fully autonomous tool-calling agent.

## Projects

### 1. News Summarizer
Fetches and summarizes the latest news for a given topic/city using Tavily Search.

### 2. Manual Tool Selection
User manually chooses which tool to invoke (weather or news) — no LLM-based routing.

### 3. Autonomous Tool-Calling Agent
The LLM decides on its own which tool to call based on the user's query (dynamic tool binding), with human-in-the-loop approval before execution.

## Features

- **Dynamic tool selection** — the LLM decides which tool to call (no hardcoded routing) in the autonomous agent
- **Human-in-the-loop approval** — every tool call must be approved before execution
- **Multi-turn conversation** — maintains message history across the session
- **Custom tools**:
  - `get_weather` — real-time weather for a city (OpenWeatherMap API)
  - `latest_news` — latest news for a city/topic (Tavily Search API)

## Tech Stack

- [LangChain](https://python.langchain.com/) — agent orchestration and tool binding
- [Mistral AI](https://mistral.ai/) — LLM (`mistral-small-2506`)
- [Tavily](https://tavily.com/) — real-time web search
- [OpenWeatherMap](https://openweathermap.org/api) — weather data

## Setup

1. Clone the repo
   ```bash
   git clone https://github.com/deepesh-14/langchain-tool-agent.git
   cd langchain-tool-agent
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables

   Copy `.env.example` to `.env` and add your API keys:
   ```bash
   cp .env.example .env
   ```
   ```
   MISTRAL_API_KEY=your_mistral_api_key
   TAVILY_API_KEY=your_tavily_api_key
   OPENWEATHER_API_KEY=your_openweather_api_key
   ```

## Usage

Each project can be run independently:

```bash
python news_summarizer.py       # News summarizer
python manual_tool_select.py    # Manual tool selection
python auto_tool_agent.py       # Autonomous tool-calling agent
```

(Update filenames above to match your actual script names.)

For the autonomous agent, type your query (e.g. "What's the weather in Lucknow?" or "Latest news in Mumbai"). The agent will propose a tool call — approve it with `yes` or reject with `no`. Type `exit` to quit.

### Example (autonomous agent)

```
you: what's the weather in Delhi?
agent wants to call the tool get_weather approve yes/no: yes
Weather in Delhi: clear sky, 34°c
```

## How the autonomous agent works

1. User sends a message
2. The LLM (bound with tool definitions) decides whether a tool is needed
3. If a tool call is proposed, the user approves or rejects it
4. On approval, the tool executes and the result is fed back to the LLM
5. The LLM responds using the tool's output, or asks a follow-up

## License

MIT
