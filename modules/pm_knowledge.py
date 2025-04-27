import streamlit as st
import pandas as pd
import time
from utils.data_utils import load_pm_knowledge
from utils.openai_utils import get_pm_knowledge_response

def show_pm_knowledge():
    """
    Display the PM Knowledge Assistant module to answer PMO policy/documentation queries.
    """
    st.subheader("PM Knowledge Assistant")
    
    st.write("""
    The PM Knowledge Assistant provides answers to your questions about project management 
    practices, methodologies, tools, techniques, and PMO policies. It uses AI to provide 
    helpful and accurate responses based on best practices.
    """)
    
    # Load PM knowledge data
    pm_data = load_pm_knowledge()
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Ask a Question", "Browse Knowledge Base"])
    
    with tab1:
        # Check for OpenAI API key
        if not st.session_state.openai_api_key:
            st.warning("⚠️ Please provide your OpenAI API key in the sidebar settings to use the PM Knowledge Assistant.")
        else:
            st.write("Ask me anything about project management practices, methodologies, or PMO policies.")
            
            # Initialize chat history if not exists
            if "pm_chat_history" not in st.session_state:
                st.session_state.pm_chat_history = []
            
            # Display chat history
            for message in st.session_state.pm_chat_history:
                if message["role"] == "user":
                    st.chat_message("user").write(message["content"])
                else:
                    st.chat_message("assistant").write(message["content"])
            
            # Get user input
            user_query = st.chat_input("Ask a question about Project Management...")
            
            if user_query:
                # Display user message
                st.chat_message("user").write(user_query)
                
                # Add to chat history
                st.session_state.pm_chat_history.append({"role": "user", "content": user_query})
                
                # Get response using OpenAI
                with st.spinner("Thinking..."):
                    response = get_pm_knowledge_response(user_query, pm_data)
                
                # Display assistant response
                st.chat_message("assistant").write(response)
                
                # Add to chat history
                st.session_state.pm_chat_history.append({"role": "assistant", "content": response})
            
            # Clear chat button
            if st.session_state.pm_chat_history and st.button("Clear Chat History", key="clear_pm_chat"):
                st.session_state.pm_chat_history = []
                st.rerun()
    
    with tab2:
        st.write("Browse the Project Management knowledge base for common topics and guidance.")
        
        # Filter by area
        all_areas = ["All Areas"] + sorted(pm_data["area"].unique().tolist())
        selected_area = st.selectbox("Filter by Area", all_areas)
        
        # Apply filter
        if selected_area == "All Areas":
            filtered_data = pm_data
        else:
            filtered_data = pm_data[pm_data["area"] == selected_area]
        
        # Search box
        search_query = st.text_input("Search", placeholder="Type to search...")
        
        if search_query:
            # Simple case-insensitive search across topic and guidance columns
            mask = (
                filtered_data["topic"].str.lower().str.contains(search_query.lower()) | 
                filtered_data["guidance"].str.lower().str.contains(search_query.lower())
            )
            filtered_data = filtered_data[mask]
        
        # Display knowledge items as expandable sections
        if not filtered_data.empty:
            for i, row in filtered_data.iterrows():
                with st.expander(f"**{row['area']}**: {row['topic']}"):
                    st.write(row['guidance'])
        else:
            st.info("No matching entries found.")
        
        # Button to suggest new topics
        with st.expander("Suggest New Knowledge", expanded=False):
            st.write("""
            If you can't find the information you're looking for, you can suggest 
            new project management knowledge to be added to the knowledge base.
            """)
            
            with st.form("suggest_knowledge_form"):
                suggested_area = st.text_input("Project Management Area")
                suggested_topic = st.text_input("Topic")
                suggested_guidance = st.text_area("Guidance/Information")
                
                submit = st.form_submit_button("Submit Suggestion")
                if submit:
                    if suggested_area and suggested_topic and suggested_guidance:
                        st.success("Thank you for your suggestion! It will be reviewed by the PMO team.")
                    else:
                        st.error("Please fill in all fields.")
