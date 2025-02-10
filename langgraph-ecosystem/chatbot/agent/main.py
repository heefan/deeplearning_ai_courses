from fastapi import FastAPI
from pydantic import BaseModel
from agent import create_agent
from utility import print_agent_graph
    
app = FastAPI()
graph = create_agent()

print_agent_graph(graph)

class ChatInput(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(chat_input: ChatInput):
    responses = []
    for event in graph.stream({"messages": [{"role": "user", "content": chat_input.message}]}):
        for value in event.values():
            responses.append(value["messages"][-1].content)
    return {"response": responses[-1]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,           
        reload_dirs=["./"],    
    )