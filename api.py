from pydantic import BaseModel
from agent import research_graph
from fastapi import FastAPI, HTTPException

class ResearchRequest(BaseModel):
    research_question : str


app = FastAPI()
@app.post("/research")
def research(request : ResearchRequest):
    if not request.research_question.strip():
        raise HTTPException(status_code = 400, detail = "Research Question cannot be empty")
    else:
        result = research_graph.invoke({
            "research_question" : request.research_question,
            "search_results" : [],
            "messages" : [],
            "is_complete" : False,
            "final_report" : ""
        })
        return {"final_report": result["final_report"]}
