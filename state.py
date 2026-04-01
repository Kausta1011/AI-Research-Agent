from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    research_question : str
    search_results : list
    messages : Annotated[list, operator.add]
    is_complete : bool
    final_report : str
    iteration_count : int