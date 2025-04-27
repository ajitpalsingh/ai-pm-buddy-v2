import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils.openai_utils import analyze_team_sentiment
from utils.visualization import create_sentiment_gauge, create_wordcloud

def show_sentiment_analyzer(project_data):
    """
    Display the team sentiment analyzer module.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.subheader("Team Sentiment Analyzer")
    
    # Get team feedback data
    team_feedback = project_data.get('team_feedback', [])
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Sentiment Analysis", "Manage Feedback"])
    
    with tab1:
        st.write("""
        The Team Sentiment Analyzer uses AI to analyze feedback from team members, 
        detect positive and negative sentiment, and identify key themes in the feedback.
        """)
        
        if not team_feedback:
            st.info("No team feedback available. Use the 'Manage Feedback' tab to add feedback.")
        else:
            # Create columns for metrics and wordcloud
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # Analyze team sentiment with OpenAI
                if st.button("Analyze Sentiment", key="analyze_sentiment"):
                    with st.spinner("Analyzing team sentiment..."):
                        sentiment_results = analyze_team_sentiment(team_feedback)
                        
                        # Store the results in session state for persistence
                        st.session_state.sentiment_results = sentiment_results
                
                # Get sentiment results from session state or initialize
                if 'sentiment_results' not in st.session_state:
                    st.session_state.sentiment_results = {"overall_sentiment": 0, "themes": [], "concerns": [], "positives": []}
                
                # Create sentiment gauge
                sentiment_score = st.session_state.sentiment_results.get("overall_sentiment", 0)
                sentiment_fig = create_sentiment_gauge(sentiment_score)
                st.plotly_chart(sentiment_fig, use_container_width=True)
                
                # Display number of feedback entries
                st.metric("Feedback Entries", len(team_feedback))
                
                # Map sentiment score to description
                sentiment_desc = ""
                if sentiment_score <= -0.5:
                    sentiment_desc = "Very Negative"
                elif sentiment_score <= -0.2:
                    sentiment_desc = "Negative"
                elif sentiment_score <= 0.2:
                    sentiment_desc = "Neutral"
                elif sentiment_score <= 0.5:
                    sentiment_desc = "Positive"
                else:
                    sentiment_desc = "Very Positive"
                
                st.write(f"Overall Team Sentiment: **{sentiment_desc}**")
            
            with col2:
                # Create wordcloud from feedback
                st.subheader("Feedback Word Cloud")
                wordcloud_fig = create_wordcloud(team_feedback)
                if wordcloud_fig:
                    st.pyplot(wordcloud_fig)
                else:
                    st.info("Not enough feedback data to generate word cloud.")
            
            # Display key themes, concerns, and positives
            st.subheader("Key Insights from Feedback")
            
            # Get themes, concerns, and positives from sentiment results
            themes = st.session_state.sentiment_results.get("themes", [])
            concerns = st.session_state.sentiment_results.get("concerns", [])
            positives = st.session_state.sentiment_results.get("positives", [])
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Themes")
                if themes:
                    for theme in themes:
                        st.write(f"• {theme}")
                else:
                    st.info("No themes identified.")
                
                st.subheader("Concerns")
                if concerns:
                    for concern in concerns:
                        st.write(f"• {concern}")
                else:
                    st.info("No concerns identified.")
            
            with col2:
                st.subheader("Positive Aspects")
                if positives:
                    for positive in positives:
                        st.write(f"• {positive}")
                else:
                    st.info("No positive aspects identified.")
            
            # Display all feedback
            with st.expander("View All Feedback", expanded=False):
                for i, feedback in enumerate(team_feedback):
                    st.write(f"{i+1}. {feedback}")
    
    with tab2:
        st.write("Add, edit, or remove team feedback entries.")
        
        # Action selection
        action = st.radio("Select action:", ["Add New Feedback", "Edit Existing Feedback", "Remove Feedback"])
        
        if action == "Add New Feedback":
            with st.form("add_feedback_form"):
                st.write("Add a new feedback entry")
                
                # Feedback details
                feedback_text = st.text_area("Feedback Text", height=100)
                
                # Submit button
                submit_button = st.form_submit_button("Add Feedback")
                
                if submit_button:
                    if feedback_text:
                        # Add to feedback data
                        if 'team_feedback' not in project_data:
                            project_data['team_feedback'] = []
                        
                        project_data['team_feedback'].append(feedback_text)
                        st.success("Feedback added successfully!")
                        
                        # Reset sentiment results to trigger reanalysis
                        if 'sentiment_results' in st.session_state:
                            del st.session_state.sentiment_results
                        
                        st.rerun()
                    else:
                        st.error("Feedback text is required!")
        
        elif action == "Edit Existing Feedback":
            if not team_feedback:
                st.info("No feedback available to edit.")
            else:
                # Select feedback to edit
                feedback_options = {f"Feedback {i+1}: {feedback[:40]}...": i for i, feedback in enumerate(team_feedback)}
                selected_feedback_label = st.selectbox("Select feedback to edit", options=list(feedback_options.keys()))
                selected_feedback_idx = feedback_options[selected_feedback_label]
                
                # Get the selected feedback
                feedback_to_edit = team_feedback[selected_feedback_idx]
                
                with st.form("edit_feedback_form"):
                    st.write(f"Editing Feedback {selected_feedback_idx + 1}")
                    
                    # Feedback details
                    feedback_text = st.text_area("Feedback Text", value=feedback_to_edit, height=100)
                    
                    # Submit button
                    submit_button = st.form_submit_button("Update Feedback")
                    
                    if submit_button:
                        if feedback_text:
                            # Update the feedback
                            project_data['team_feedback'][selected_feedback_idx] = feedback_text
                            st.success("Feedback updated successfully!")
                            
                            # Reset sentiment results to trigger reanalysis
                            if 'sentiment_results' in st.session_state:
                                del st.session_state.sentiment_results
                            
                            st.rerun()
                        else:
                            st.error("Feedback text is required!")
        
        elif action == "Remove Feedback":
            if not team_feedback:
                st.info("No feedback available to remove.")
            else:
                # Select feedback to remove
                feedback_options = {f"Feedback {i+1}: {feedback[:40]}...": i for i, feedback in enumerate(team_feedback)}
                selected_feedback_label = st.selectbox("Select feedback to remove", options=list(feedback_options.keys()))
                selected_feedback_idx = feedback_options[selected_feedback_label]
                
                if st.button("Remove Feedback"):
                    # Remove the feedback
                    project_data['team_feedback'].pop(selected_feedback_idx)
                    st.success("Feedback removed successfully!")
                    
                    # Reset sentiment results to trigger reanalysis
                    if 'sentiment_results' in st.session_state:
                        del st.session_state.sentiment_results
                    
                    st.rerun()
