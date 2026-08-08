from dotenv import load_dotenv
load_dotenv()
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from rich import print
model = ChatMistralAI(model = "mistral-small-2506")

#creating a tool
@tool #in tool we define a function
def get_text_length(Text : str) -> int:
     #get_text_length this is the name of function,#this recieves the text as string,-> int this retruns the value in integer
    """ Returns the number of characters in the sentence"""# this is description of what tool does
    return len(Text)
tools = {"get_text_length" : get_text_length}# It allows you to look up and execute functions dynamically by name.


 #tool binding
model_with_tool =model.bind_tools([get_text_length]) #binded get_tect_tool with .bindtools
you = input("you :")
message =[] #phle khali messg bnaya store krne ke liye 
query = HumanMessage(you)#messg diya

message.append(query) #phrr khali box me yhi daal diya jisse history save rhe 
result = model_with_tool.invoke(message)# model invoke kiya
message.append(result)#phrr se mesg me sbb daal diya
print(message)

#tool calling
if result.tool_calls:
    tool_name= result.tool_calls[0]["name"]
    tool_messg = tools[tool_name].invoke(result.tool_calls[0])
    message.append(tool_messg)
    print(tool_messg)