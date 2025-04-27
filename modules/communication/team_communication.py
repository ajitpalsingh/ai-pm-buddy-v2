import streamlit as st
import pandas as pd
import datetime
from utils.openai_utils import get_openai_client

def show_team_communication(project_data):
    """
    Display the Team Communication Management module.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.markdown("<h2 class='module-header'>Team Communication Management</h2>", unsafe_allow_html=True)
    
    # Create tabs for different communication features
    tab1, tab2, tab3, tab4 = st.tabs(["📣 Announcements", "🗓️ Meeting Notes", "📱 SMS Notifications", "👥 Team Feedback"])
    
    with tab1:
        show_announcements(project_data)
    
    with tab2:
        show_meeting_notes(project_data)
        
    with tab3:
        show_sms_notifications(project_data)
    
    with tab4:
        show_team_feedback(project_data)

def show_announcements(project_data):
    """
    Display project announcements section.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.markdown("### Project Announcements")
    
    # Initialize announcements if not present
    if 'announcements' not in project_data:
        project_data['announcements'] = []
    
    # Display existing announcements
    if project_data['announcements']:
        st.markdown("#### Recent Announcements")
        for i, announcement in enumerate(reversed(project_data['announcements'])):
            if i < 5:  # Show only 5 most recent announcements
                with st.expander(f"{announcement['title']} ({announcement['date']})"):
                    st.write(announcement['message'])
                    st.caption(f"By: {announcement['author']} | Priority: {announcement['priority']}")
    
    # Add new announcement
    st.markdown("#### Create New Announcement")
    with st.form("new_announcement_form"):
        title = st.text_input("Title")
        message = st.text_area("Message")
        priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
        author = st.text_input("Your Name")
        
        submitted = st.form_submit_button("Post Announcement")
        if submitted and title and message and author:
            new_announcement = {
                'title': title,
                'message': message,
                'author': author,
                'priority': priority,
                'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            project_data['announcements'].append(new_announcement)
            st.success("Announcement posted successfully!")
            st.experimental_rerun()

def show_meeting_notes(project_data):
    """
    Display meeting notes section.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.markdown("### Meeting Notes")
    
    # Initialize meeting notes if not present
    if 'meeting_notes' not in project_data:
        project_data['meeting_notes'] = []
    
    # Display existing meeting notes
    if project_data['meeting_notes']:
        st.markdown("#### Recent Meeting Notes")
        for i, meeting in enumerate(reversed(project_data['meeting_notes'])):
            if i < 5:  # Show only 5 most recent meetings
                with st.expander(f"{meeting['meeting_type']} - {meeting['date']}"):
                    st.markdown(f"**Attendees:** {meeting['attendees']}")
                    st.markdown("**Discussion:**")
                    st.write(meeting['notes'])
                    if meeting['action_items']:
                        st.markdown("**Action Items:**")
                        for item in meeting['action_items']:
                            st.markdown(f"- {item}")
    
    # Add new meeting notes
    st.markdown("#### Add New Meeting Notes")
    with st.form("new_meeting_form"):
        meeting_type = st.selectbox("Meeting Type", ["Sprint Planning", "Daily Standup", "Sprint Review", "Sprint Retrospective", "Stakeholder Meeting", "Other"])
        meeting_date = st.date_input("Meeting Date", datetime.datetime.now())
        attendees = st.text_input("Attendees (comma separated)")
        notes = st.text_area("Meeting Notes")
        
        # Action items as a list
        st.markdown("Action Items (add one per line)")
        action_items_text = st.text_area("Action Items", height=100)
        
        submitted = st.form_submit_button("Save Meeting Notes")
        if submitted and meeting_type and attendees and notes:
            # Process action items into a list
            action_items = [item.strip() for item in action_items_text.split('\n') if item.strip()]
            
            new_meeting = {
                'meeting_type': meeting_type,
                'date': meeting_date.strftime("%Y-%m-%d"),
                'attendees': attendees,
                'notes': notes,
                'action_items': action_items
            }
            project_data['meeting_notes'].append(new_meeting)
            st.success("Meeting notes saved successfully!")
            st.experimental_rerun()

def show_sms_notifications(project_data):
    """
    Display SMS notification management.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.markdown("### SMS Notifications")
    
    # Initialize SMS notifications settings if not present
    if 'sms_settings' not in project_data:
        project_data['sms_settings'] = {
            'enabled': False,
            'recipients': [],
            'notification_types': []
        }
    
    # Check if Twilio credentials are configured
    twilio_configured = st.session_state.get('twilio_configured', False)
    if not twilio_configured:
        st.warning("Twilio SMS integration is not configured. Please configure it in the settings.")
        
        # Demo configuration form for Twilio
        with st.expander("Configure Twilio Integration"):
            with st.form("twilio_config_form"):
                account_sid = st.text_input("Twilio Account SID")
                auth_token = st.text_input("Twilio Auth Token", type="password")
                phone_number = st.text_input("Twilio Phone Number (with country code)")
                
                submit_twilio = st.form_submit_button("Save Twilio Configuration")
                if submit_twilio and account_sid and auth_token and phone_number:
                    # In a real implementation, store these securely
                    # Here, we'll just set a flag for the demo
                    st.session_state.twilio_account_sid = account_sid
                    st.session_state.twilio_auth_token = auth_token
                    st.session_state.twilio_phone_number = phone_number
                    st.session_state.twilio_configured = True
                    st.success("Twilio configured successfully!")
                    st.experimental_rerun()
    
    # SMS notification settings
    st.markdown("#### Notification Settings")
    
    enabled = st.checkbox("Enable SMS Notifications", value=project_data['sms_settings']['enabled'])
    project_data['sms_settings']['enabled'] = enabled
    
    if enabled:
        st.markdown("#### Recipient Management")
        
        # Display current recipients
        if project_data['sms_settings']['recipients']:
            st.markdown("Current Recipients:")
            recipient_df = pd.DataFrame(project_data['sms_settings']['recipients'])
            st.dataframe(recipient_df)
        
        # Add new recipient
        with st.form("add_recipient_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name")
            with col2:
                phone = st.text_input("Phone Number (with country code)")
            
            role = st.selectbox("Role", ["Project Manager", "Team Member", "Stakeholder", "Client", "Other"])
            
            add_recipient = st.form_submit_button("Add Recipient")
            if add_recipient and name and phone:
                if 'recipients' not in project_data['sms_settings']:
                    project_data['sms_settings']['recipients'] = []
                
                new_recipient = {
                    'name': name,
                    'phone': phone,
                    'role': role
                }
                project_data['sms_settings']['recipients'].append(new_recipient)
                st.success(f"Added {name} to recipients list")
                st.experimental_rerun()
        
        # Configure notification types
        st.markdown("#### Notification Types")
        notification_types = st.multiselect(
            "Select events to send SMS notifications for:",
            [
                "Critical Path Delay",
                "High Risk Identified",
                "Major Milestone Completion",
                "Budget Overrun",
                "Team Member Overallocation",
                "Scope Change Approved",
                "Meeting Reminders"
            ],
            default=project_data['sms_settings'].get('notification_types', [])
        )
        project_data['sms_settings']['notification_types'] = notification_types
        
        # Send test message
        if st.session_state.get('twilio_configured', False) and project_data['sms_settings']['recipients']:
            st.markdown("#### Test Notification")
            col1, col2 = st.columns(2)
            
            with col1:
                test_recipient = st.selectbox(
                    "Select recipient for test message",
                    [r['name'] for r in project_data['sms_settings']['recipients']]
                )
            
            with col2:
                test_button = st.button("Send Test SMS")
                
            if test_button:
                # This would use the actual Twilio integration in production
                st.info("In a production environment, this would send an actual SMS using Twilio.")
                st.success(f"Test message sent to {test_recipient}")
                
                # Sample code for production (commented out):
                """
                from utils.sms_utils import send_twilio_message
                
                # Get recipient phone number
                recipient_phone = next(r['phone'] for r in project_data['sms_settings']['recipients'] if r['name'] == test_recipient)
                
                # Send test message
                message = f"This is a test notification from AI PM Buddy for {project_data['name']}."
                send_twilio_message(recipient_phone, message)
                """

def show_team_feedback(project_data):
    """
    Display team feedback collection and analysis.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.markdown("### Team Feedback Collection")
    
    # Initialize feedback collection if not present
    if 'feedback_campaigns' not in project_data:
        project_data['feedback_campaigns'] = []
    
    # Display existing feedback campaigns
    if project_data['feedback_campaigns']:
        st.markdown("#### Active Feedback Campaigns")
        for i, campaign in enumerate(project_data['feedback_campaigns']):
            with st.expander(f"{campaign['title']} (Created: {campaign['created_date']})"):
                st.markdown(f"**Description:** {campaign['description']}")
                st.markdown(f"**Status:** {'Active' if campaign['active'] else 'Inactive'}")
                st.markdown(f"**Questions:**")
                for q in campaign['questions']:
                    st.markdown(f"- {q}")
                
                if 'responses' in campaign:
                    st.markdown(f"**Responses:** {len(campaign['responses'])}")
                    
                    # Show response analysis if there are responses
                    if campaign['responses']:
                        st.markdown("**Response Summary:**")
                        
                        # In a real implementation, this would use OpenAI to analyze responses
                        if st.button(f"Analyze Responses for '{campaign['title']}'"):
                            st.info("Analyzing feedback responses...")
                            
                            # This would be implemented with actual OpenAI integration
                            analysis_result = {
                                'sentiment_score': 0.75,
                                'common_themes': [
                                    "Communication improvements needed",
                                    "Appreciation for regular updates",
                                    "Concerns about timeline"
                                ],
                                'action_items': [
                                    "Schedule more frequent status meetings",
                                    "Provide written summaries of decisions",
                                    "Review timeline with the team"
                                ]
                            }
                            
                            st.markdown("**Analysis Results:**")
                            st.markdown(f"Sentiment Score: {analysis_result['sentiment_score']:.2f}")
                            
                            st.markdown("**Common Themes:**")
                            for theme in analysis_result['common_themes']:
                                st.markdown(f"- {theme}")
                            
                            st.markdown("**Recommended Action Items:**")
                            for item in analysis_result['action_items']:
                                st.markdown(f"- {item}")
    
    # Create new feedback campaign
    st.markdown("#### Create New Feedback Campaign")
    with st.form("new_feedback_campaign"):
        title = st.text_input("Campaign Title")
        description = st.text_area("Campaign Description")
        
        # Question management
        st.markdown("Add Questions (one per line)")
        questions_text = st.text_area("Questions", height=150)
        
        anonymous = st.checkbox("Make responses anonymous", value=True)
        
        submitted = st.form_submit_button("Create Feedback Campaign")
        if submitted and title and description and questions_text:
            questions = [q.strip() for q in questions_text.split('\n') if q.strip()]
            
            new_campaign = {
                'title': title,
                'description': description,
                'questions': questions,
                'anonymous': anonymous,
                'active': True,
                'created_date': datetime.datetime.now().strftime("%Y-%m-%d"),
                'responses': []
            }
            
            project_data['feedback_campaigns'].append(new_campaign)
            st.success("Feedback campaign created successfully!")
            st.experimental_rerun()
    
    # Simulate feedback submission (this would be on a separate page in a real app)
    st.markdown("---")
    st.markdown("#### Submit Feedback (Demo)")
    
    if project_data['feedback_campaigns']:
        active_campaigns = [c for c in project_data['feedback_campaigns'] if c.get('active', False)]
        
        if active_campaigns:
            campaign_titles = [c['title'] for c in active_campaigns]
            selected_campaign = st.selectbox("Select Feedback Campaign", campaign_titles)
            
            # Find the selected campaign
            campaign = next((c for c in active_campaigns if c['title'] == selected_campaign), None)
            
            if campaign:
                with st.form("submit_feedback"):
                    st.markdown(f"**{campaign['title']}**")
                    st.markdown(campaign['description'])
                    
                    responses = {}
                    for question in campaign['questions']:
                        responses[question] = st.text_area(f"{question}", key=f"q_{question}")
                    
                    name = "" if campaign['anonymous'] else st.text_input("Your Name (Optional)")
                    
                    submit_feedback = st.form_submit_button("Submit Feedback")
                    if submit_feedback:
                        # Add response to campaign
                        feedback_entry = {
                            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                            'name': name if not campaign['anonymous'] else "Anonymous",
                            'responses': responses
                        }
                        
                        # Find campaign in the original list and add the response
                        for c in project_data['feedback_campaigns']:
                            if c['title'] == selected_campaign:
                                if 'responses' not in c:
                                    c['responses'] = []
                                c['responses'].append(feedback_entry)
                                break
                        
                        st.success("Thank you for your feedback!")
        else:
            st.info("No active feedback campaigns available.")
    else:
        st.info("No feedback campaigns have been created yet.")