from dotenv import load_dotenv
load_dotenv()

import os
import requests

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from tavily import TavilyClient
from rich import print
from langchain.agents import create_agent


# -------------------- Tool 1 : Weather -------------------- #

@tool
def get_weather(city: str) -> str:
    """get the weather details of this city"""

    OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")

    url = "https://api.openweathermap.org/data/2.5/weather"

    if not OPENWEATHER_KEY:
        return "Error: OPENWEATHER_API_KEY not found."

    response = requests.get(
        url,
        params={
            "q": city,
            "appid": OPENWEATHER_KEY,
            "units": "metric"
        }
    )

    data = response.json()

    print(data)

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    return f"Weather in {city}: {desc}, {temp}°C"


# -------------------- Tool 2 : News -------------------- #

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
client = TavilyClient(api_key=TAVILY_API_KEY)


@tool
def latest_news(city: str) -> str:
    """get the latest news of the city"""

    query = f"latest news about {city}"

    response = client.search(
        query=query,
        search_depth="basic",
        max_results=5
    )

    results = response.get("results", [])

    if not results:
        return f"No recent news found for {city}."

    news_list = []

    for r in results:
        title = r.get("title", "No title")
        url = r.get("url", "")
        snippet = r.get("content", "")

        news_list.append(
            f"- {title}\n"
            f"{url}\n"
            f"{snippet[:100]}..."
        )

    return f"Latest news in {city}:\n\n" + "\n\n".join(news_list)


# -------------------- Agent -------------------- #

llm = ChatMistralAI(model="mistral-small-2506")
agent = create_agent(
    model=llm,
    tools=[get_weather,latest_news],#tools which we made
    system_prompt="You are a helpful assistant. Be concise and accurate.",
)
print("city agent | type exit to leave")
while True:
    user=input("you: ")
    if user == "exit":
        break
    result = agent.invoke({
        "messages": [
            {"role": "user", "content": user}
        ]
    })

    print("bot",(result['messages'][-1]).content)
    
