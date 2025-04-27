import os
import json
import pandas as pd
import numpy as np
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

# Try to load API key from .env file (for local development)
try:
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, continue without it

def get_openai_client():
    """Get OpenAI client instance with the API key from session state or environment."""
    # First try to get API key from environment variable
    api_key = os.environ.get("OPENAI_API_KEY")
    
    # If not found in environment, try session state
    if not api_key and hasattr(st, 'session_state') and 'openai_api_key' in st.session_state:
        api_key = st.session_state.openai_api_key
    
    if not api_key:
        st.error("Please provide your OpenAI API key in the sidebar settings or set the OPENAI_API_KEY environment variable.")
        return None
    
    # Update session state with the valid API key
    if hasattr(st, 'session_state'):
        st.session_state.openai_api_key = api_key
        
    return OpenAI(api_key=api_key)

def analyze_project_risks(project_data):
    """
    Analyze project data to identify potential risks using OpenAI.
    
    Args:
        project_data: Dictionary containing project information
        
    Returns:
        List of identified risks and recommendations
    """
    client = get_openai_client()
    if not client:
        return []
    
    # Prepare project data summary for AI analysis
    tasks = project_data.get('wbs', [])
    resources = project_data.get('resources', [])
    risks = project_data.get('raid', {}).get('risks', [])
    
    project_summary = {
        "tasks": tasks,
        "resources": resources,
        "current_risks": risks
    }
    
    try:
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """You are an AI project management assistant. Analyze the project data provided 
                    and identify potential risks, issues, and recommendations. Focus on schedule risks, resource 
                    overallocation, and potential scope creep. Provide actionable recommendations.
                    
                    Respond with a JSON object containing a 'risks' array of objects, each with the following structure:
                    {
                        "risks": [
                            {
                                "risk_type": "schedule|resource|scope|quality|other",
                                "severity": "high|medium|low",
                                "description": "detailed description of the risk",
                                "recommendation": "specific recommendation to mitigate the risk"
                            },
                            ...
                        ]
                    }
                    
                    Limit your response to the 5 most important risks."""
                },
                {
                    "role": "user",
                    "content": json.dumps(project_summary)
                }
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        if isinstance(result, dict) and "risks" in result:
            return result["risks"]
        elif isinstance(result, list):
            return result
        else:
            # Fallback if result is not in expected format
            return []
    except Exception as e:
        st.error(f"Error analyzing project risks: {str(e)}")
        return []

def analyze_team_sentiment(feedback_data):
    """
    Analyze team feedback to determine sentiment and key themes.
    
    Args:
        feedback_data: List of feedback text entries
        
    Returns:
        Dict with sentiment scores and key themes
    """
    client = get_openai_client()
    if not client:
        return {"overall_sentiment": 0, "themes": []}
    
    if not feedback_data:
        return {"overall_sentiment": 0, "themes": []}
    
    feedback_text = "\n".join(feedback_data)
    
    try:
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """Analyze the team feedback provided and determine:
                    1. Overall sentiment score (-1 to 1, where -1 is very negative, 0 is neutral, 1 is very positive)
                    2. Key themes or topics mentioned (limit to 5)
                    3. Important concerns or issues raised
                    4. Positive aspects mentioned
                    
                    Return your analysis as a JSON object with these keys: 
                    overall_sentiment, themes, concerns, positives"""
                },
                {
                    "role": "user",
                    "content": feedback_text
                }
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        st.error(f"Error analyzing team sentiment: {str(e)}")
        return {"overall_sentiment": 0, "themes": []}

def get_agile_response(query, agile_data):
    """
    Get response to agile/scrum related queries using OpenAI.
    
    Args:
        query: User's question
        agile_data: DataFrame with agile knowledge
        
    Returns:
        String response to the query
    """
    client = get_openai_client()
    if not client:
        return "Please provide your OpenAI API key to use this feature."
    
    # Convert agile data to a string for context
    agile_context = "\n\n".join([
        f"Topic: {row['topic']}\nQuestion: {row['question']}\nAnswer: {row['answer']}"
        for _, row in agile_data.iterrows()
    ])
    
    try:
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """You are an Agile Coach assistant. Use the provided reference data to answer 
                    questions about Agile methodologies, Scrum, Kanban, and related practices. If the answer 
                    isn't in the reference data, provide a helpful response based on standard Agile practices. 
                    Keep responses concise and practical."""
                },
                {
                    "role": "user",
                    "content": f"Reference data:\n{agile_context}\n\nQuestion: {query}"
                }
            ]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting response: {str(e)}"

def get_pm_knowledge_response(query, pm_data):
    """
    Get response to project management knowledge queries using OpenAI.
    
    Args:
        query: User's question
        pm_data: DataFrame with PM knowledge
        
    Returns:
        String response to the query
    """
    client = get_openai_client()
    if not client:
        return "Please provide your OpenAI API key to use this feature."
    
    # Convert PM knowledge data to a string for context
    pm_context = "\n\n".join([
        f"Area: {row['area']}\nTopic: {row['topic']}\nGuidance: {row['guidance']}"
        for _, row in pm_data.iterrows()
    ])
    
    try:
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """You are a Project Management knowledge assistant. Use the provided reference 
                    data to answer questions about project management practices, methodologies, tools, and 
                    techniques. If the answer isn't in the reference data, provide a helpful response based on 
                    standard PM practices from the PMBOK and other recognized PM standards. Keep responses 
                    concise, practical and actionable."""
                },
                {
                    "role": "user",
                    "content": f"Reference data:\n{pm_context}\n\nQuestion: {query}"
                }
            ]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting response: {str(e)}"
