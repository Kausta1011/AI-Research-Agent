from state import AgentState
from langgraph.graph import StateGraph, START, END
from groq import Groq
import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


groq_client = Groq(api_key = os.getenv("GROQ_API_KEY"))
tavily_client = TavilyClient(api_key = os.getenv("TAVILY_API_KEY"))


def thinking(state : AgentState):
    print("THINKING")
    if state["messages"] == []:
        question = state["research_question"]
    else:
        question = state["messages"][-1]
    prompt = f"Understand the question: {question}, frame it nicely/ rewrite it in a way a research question should be asked but don't change the question. Make sure the context and reframed question by you is single consice (under 100 characters)that would find the most relevant information.. RETURN ONLY THE SEARCH QUERY, NOTHING ELSE"
    groq_response = groq_client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = [{"role" : "user", "content" : prompt}]
    )
    return {"messages" : [groq_response.choices[0].message.content]}


def acting(state: AgentState):
    print("ACTING")
    research_query = state["messages"][-1]
    tavily_response = tavily_client.search(
        query = research_query,
        search_depth = "advanced"
    )
    return {"search_results" : tavily_response["results"]}


def should_continue(state : AgentState):
    print("SHOULD CONTINUE?")
    #is the task done? Can I stop or should I continue?
    question = state["research_question"]
    search_result = state["search_results"]
    prompt = f""" 
                Based on the user query {question} and the search results {search_result}, what do you think? Is it enough to provide the user with an answer?
                If yes, just return/ say "yes". If no, return/ say "no". Nothing more, Nothing less
            """
    groq_continue_response = groq_client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = [{"role" : "user", "content" : prompt}]
    )
    response_check = groq_continue_response.choices[0].message.content.strip().lower()
    if response_check == 'yes':
        return {"is_complete" : True}

    else:
        print("CONTINUING")
        missing_prompt = f""" 
                            Whatever is missing according to you based on {question} and {search_result}, mention it here
                        """
        
        groq_missing_response = groq_client.chat.completions.create(
            model = "llama-3.3-70b-versatile",
            messages = [{"role" : "user", "content": missing_prompt}]
        )
        response_text = groq_missing_response.choices[0].message.content
        return {"is_complete" : False, "messages": [response_text]}

    

def final_answer(state : AgentState):
    print("FINAL ANSWER COOKING")
    question = state["research_question"]
    formatted = ""
    for i, result in enumerate(state["search_results"]):
        formatted += f"""
        Source {i+1}: {result["title"]}
        URL: {result["url"]}
        Content: {result["content"]}
        """
    final_answer_prompt = f"""
    You are a "RESEARCH ASSISTANT", the user has asked you: {question}.
    Here are the search results and resources: {formatted}, neatly structure them and write a structured report."""
    groq_final_response = groq_client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = [{"role" : "user", "content" : final_answer_prompt}]
    )
    return {"final_report" : groq_final_response.choices[0].message.content}

graph = StateGraph(AgentState)
graph.add_node("thinking" , thinking)
graph.add_node("acting", acting)
graph.add_node("should_continue", should_continue)
graph.add_node("final_answer", final_answer)

graph.set_entry_point("thinking")
graph.add_edge("thinking", "acting")
graph.add_edge("acting", "should_continue")

def route(state : AgentState):
    if state ["is_complete"]:
        return "final_answer"
    else:
        return "thinking"
graph.add_conditional_edges("should_continue", route)
graph.add_edge("final_answer", END)

app = graph.compile()
