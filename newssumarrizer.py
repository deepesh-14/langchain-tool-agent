from dotenv import load_dotenv
load_dotenv()
from langchain_community.tools.tavily_search import TavilySearchResults #Tavily is the real‑time search engine for AI agents and RAG workflows 
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser
parser = StrOutputParser()
tavily = TavilySearchResults(
    max_result = 5
)
model = ChatMistralAI(
    model = "mistral-small-2506"

)
template = ChatPromptTemplate.from_template(
    """
you are helpful ai assistant 
you will summarize the news into bullet points
{news}
"""
)
chain = template | model | parser

newsresult = tavily.run(" latest news for 2026")
result = chain.invoke({
    "news": "newsresult"
})
print(result)
