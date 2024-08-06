from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from langserve import add_routes
from pydantic import BaseModel
from typing import Any

from langchain_core.runnables import Runnable, RunnableLambda
from langchain.schema.runnable import RunnablePassthrough


app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using LangChain's Runnable interfaces",
)

class Input(BaseModel):
    input: str


class Output(BaseModel):
    output: Any
    
@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

from app.agents.decision_agent import agent_executor


add_routes(app, agent_executor.with_types(input_type=Input, output_type=Output).with_config({"run_name": "agent"}), path="/test-chain", playground_type="default")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)