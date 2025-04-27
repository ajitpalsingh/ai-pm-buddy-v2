import streamlit as st
import pandas as pd
import time
from utils.data_utils import load_agile_knowledge
from utils.openai_utils import get_agile_response

def show_agile_coach():
    """
    Display the Agile Coach Bot module to answer Agile/Scrum related queries.
    """
    st.subheader("Agile Coach Bot")
    
    st.write("""
    The Agile Coach Bot provides answers to your questions about Agile methodologies, 
    Scrum, Kanban, and related practices. It uses AI to provide helpful and accurate responses.
    """)
    
    # Load Agile knowledge data
    agile_data = load_agile_knowledge()
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Ask a Question", "Browse Knowledge Base"])
    
    with tab1:
        # Check for OpenAI API key
        if not st.session_state.openai_api_key:
            st.warning("⚠️ Please provide your OpenAI API key in the sidebar settings to use the Agile Coach Bot.")
        else:
            st.write("Ask me anything about Agile methodologies, Scrum, Kanban, or other Agile practices.")
            
            # Initialize chat history if not exists
            if "agile_chat_history" not in st.session_state:
                st.session_state.agile_chat_history = []
            
            # Display chat history
            for message in st.session_state.agile_chat_history:
                if message["role"] == "user":
                    st.chat_message("user").write(message["content"])
                else:
                    st.chat_message("assistant").write(message["content"])
            
            # Get user input
            user_query = st.chat_input("Ask a question about Agile...")
            
            if user_query:
                # Display user message
                st.chat_message("user").write(user_query)
                
                # Add to chat history
                st.session_state.agile_chat_history.append({"role": "user", "content": user_query})
                
                # Get response using OpenAI
                with st.spinner("Thinking..."):
                    response = get_agile_response(user_query, agile_data)
                
                # Display assistant response
                st.chat_message("assistant").write(response)
                
                # Add to chat history
                st.session_state.agile_chat_history.append({"role": "assistant", "content": response})
            
            # Clear chat button
            if st.session_state.agile_chat_history and st.button("Clear Chat History", key="clear_agile_chat"):
                st.session_state.agile_chat_history = []
                st.rerun()
    
    with tab2:
        st.write("Browse the Agile knowledge base for common questions and answers.")
        
        # Filter by topic
        all_topics = ["All Topics"] + sorted(agile_data["topic"].unique().tolist())
        selected_topic = st.selectbox("Filter by Topic", all_topics)
        
        # Apply filter
        if selected_topic == "All Topics":
            filtered_data = agile_data
        else:
            filtered_data = agile_data[agile_data["topic"] == selected_topic]
        
        # Search box
        search_query = st.text_input("Search", placeholder="Type to search...")
        
        if search_query:
            # Simple case-insensitive search across question and answer columns
            mask = (
                filtered_data["question"].str.lower().str.contains(search_query.lower()) | 
                filtered_data["answer"].str.lower().str.contains(search_query.lower())
            )
            filtered_data = filtered_data[mask]
        
        # Display FAQ items as expandable sections
        if not filtered_data.empty:
            for i, row in filtered_data.iterrows():
                with st.expander(f"**{row['topic']}**: {row['question']}"):
                    st.write(row['answer'])
        else:
            st.info("No matching entries found.")
        
        # Button to suggest new topics
        with st.expander("Suggest a New Topic", expanded=False):
            st.write("""
            If you can't find the information you're looking for, you can suggest 
            a new topic or question to be added to the knowledge base.
            """)
            
            with st.form("suggest_topic_form"):
                suggested_topic = st.text_input("Topic")
                suggested_question = st.text_area("Question")
                
                submit = st.form_submit_button("Submit Suggestion")
                if submit:
                    if suggested_topic and suggested_question:
                        st.success("Thank you for your suggestion! It will be reviewed by the project team.")
                    else:
                        st.error("Please enter both a topic and a question.")
