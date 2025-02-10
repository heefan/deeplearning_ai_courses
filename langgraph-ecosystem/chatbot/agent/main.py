from fastapi import FastAPI
from pydantic import BaseModel
from agent import create_agent
from utility import print_agent_graph
import uuid
    
app = FastAPI()
graph = create_agent()

print_agent_graph(graph)

class ChatInput(BaseModel):
    message: str
    session_id: str | None = None

@app.post("/chat")
async def chat_endpoint(chat_input: ChatInput):
    try:
        # Create or use existing session ID
        session_id = chat_input.session_id or str(uuid.uuid4())
        
        # Initialize state with the user message
        state = {
            "messages": [{"role": "user", "content": chat_input.message}]
        }
        
        # Process the message and get all responses
        responses = []
        full_conversation = []
        
        # Add the required configurable key for checkpointing
        config = {
            "configurable": {
                "thread_id": session_id  # Using thread_id as the configurable key
            }
        }
        
        for event in graph.stream(state, config=config):
            for value in event.values():
                latest_message = value["messages"][-1]
                responses.append(latest_message.content)
                full_conversation.extend(value["messages"])
        
        return {
            "response": responses[-1],
            "status": "success",
            "session_id": session_id,
            "conversation": full_conversation
        }
    except Exception as e:
        return {
            "response": str(e), 
            "status": "error",
            "session_id": None,
            "conversation": []
        }

@app.get("/conversation/{session_id}")
async def get_conversation(session_id: str):
    try:
        state = {
            "messages": [{"role": "user", "content": "Show me our conversation"}]
        }
        
        config = {
            "configurable": {
                "thread_id": session_id
            }
        }
        
        conversation = []
        for event in graph.stream(state, config=config):
            for value in event.values():
                conversation.extend(value["messages"])
        
        return {
            "status": "success",
            "conversation": conversation
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,           
        reload_dirs=["./"],    
    )