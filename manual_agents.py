from dotenv import load_dotenv
load_dotenv()
import os 
import requests# to search anything on the web means URL based
from langchain_community.tools.tavily_search import TavilySearchResults #Tavily is the real‑time search engine for AI agents and RAG workflows 
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage,ToolMessage 
from langchain_core.tools import tool
from tavily import TavilyClient
from rich import print

#tool1 get weather
@tool
def get_weather(city : str) -> str:
    """get the weather details of this city""" 
    OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather"#yha url dalni h
    if not OPENWEATHER_KEY:
        return "Error: OPENWEATHER_API_KEY not found."
    respond = requests.get(
    url,
    params={
        "q": city,
        "appid": OPENWEATHER_KEY,
        "units": "metric"
    }
)
    variable = respond.json()
    print("Le re lund ke",variable)
    temp = variable ["main"] ["temp"]
    desc = variable ["weather"] [0] ["description"]
    return f"Weather in {city}:{desc}, {temp}°c"



#tool2 latest news about the city
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
client = TavilyClient(api_key=TAVILY_API_KEY)
@tool
def latest_news(city: str) -> str:
    """get the latest news of the city"""
    query=f"latest news of the city is:, {city}"
    response = client.search(
        search_depth = "basic",
        query= query,
        max_results = 5
        )
    result = response.get("results", [])
    
    news_list = []
    if not result:
        return f"No recent news found for {city}."
    for r in result:
        title = r.get("title", "No title")
        url = r.get ("url","")
        snippet = r.get("content", "")
        news_list.append (f"- {title}\n, {url}\n, {snippet[: 100]}...")
    return f"Latest news in {city}: \n\n" + "\n\n".join(news_list)




#connecting with agent 
llm = ChatMistralAI(model_name="mistral-small-2506")
tools = {"get_weather": get_weather,
         "latest_news": latest_news}
#tool bind
toolbind = llm.bind_tools([get_weather,latest_news])#Sequence[dict[str, Any]
message =[]
print("type exit to quit")
while True:
    userinput = input("you:")

    if userinput =="exit":
        break
    message.append(HumanMessage(content=userinput))# appending what the human sends 
    while True:
        result = toolbind.invoke(message)
        message.append(result)#jo result aaya phrr se daal diya append krke
        #if tool is required 
        if result.tool_calls:
            for tool_call in result.tool_calls:
                tool_name = tool_call['name']
                confirm = input(f"agents want to call the tool {tool_name} aprrove yes/no")
                if confirm.lower()== "no":
                    print("ja re laude")

                    break
                #executipn of the tool
                tool_result = tools[tool_name].invoke(tool_call["args"])# because LangChain tools expect only the arguments, not the entire tool_call
                message.append(ToolMessage(content=tool_result, tool_call_id=tool_call["id"]))
            continue
        else:
            print(result.content) 







