from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
from restack_ai import Restack
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define request model
class QueryRequest(BaseModel):
    query: str
    count: int

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return "Welcome to the TogetherAI LlamaIndex FastAPI App!"

@app.post("/api/schedule")
async def schedule_workflow(request: QueryRequest):
    try:
        logger.info(f"Received query request: {request.query}")
        client = Restack()
        workflow_id = f"{int(time.time() * 1000)}-llm_complete_workflow"
        
        runId = await client.schedule_workflow(
            workflow_name="hn_workflow",
            workflow_id=workflow_id,
            input={"query": request.query, "count": request.count}
        )
        logger.info(f"Scheduled workflow {runId} for query: {request.query}")
        
        result = await client.get_workflow_result(
            workflow_id=workflow_id,
            run_id=runId
        )
        logger.info(f"Workflow completed for query: {request.query}")
        
        return {
            "result": result,
            "workflow_id": workflow_id,
            "run_id": runId
        }
    except Exception as e:
        logger.error(f"Error processing query {request.query}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Remove Flask-specific run code since FastAPI uses uvicorn
def run_app():
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == '__main__':
    run_app()
