import streamlit as st
import pandas as pd
import datetime
import json
import requests

def show_ms_teams_integration(project_data):
    """
    Display the Microsoft Teams Integration module.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.markdown("<h2 class='module-header'>Microsoft Teams Integration</h2>", unsafe_allow_html=True)
    
    # Initialize Teams configuration if not present
    if 'teams_config' not in project_data:
        project_data['teams_config'] = {
            'configured': False,
            'webhook_url': '',
            'channel_name': '',
            'last_message': None
        }
    
    # Create tabs for Teams functionality
    tab1, tab2, tab3 = st.tabs(["⚙️ Configuration", "📱 Message Center", "🔄 Notification Rules"])
    
    with tab1:
        show_teams_configuration(project_data)
    
    with tab2:
        show_teams_message_center(project_data)
    
    with tab3:
        show_teams_notification_rules(project_data)

def show_teams_configuration(project_data):
    """
    Display and manage Microsoft Teams configuration.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.markdown("### Microsoft Teams Configuration")
    
    teams_config = project_data['teams_config']
    
    # Configuration status
    if teams_config['configured']:
        st.success("Microsoft Teams integration is configured")
        st.markdown(f"**Channel Name:** {teams_config['channel_name']}")
        
        if teams_config['last_message']:
            st.markdown(f"**Last Message Sent:** {teams_config['last_message']}")
        else:
            st.info("No messages have been sent yet")
        
        # Option to reconfigure
        if st.button("Reconfigure Teams Connection"):
            teams_config['configured'] = False
            st.experimental_rerun()
    else:
        st.warning("Microsoft Teams integration is not configured")
        
        # Configuration form
        with st.form("teams_config_form"):
            st.markdown("""
            #### How to Get Teams Webhook URL:
            1. Go to the Teams channel where you want to receive notifications
            2. Click on the "..." menu next to the channel name
            3. Select "Connectors"
            4. Search for "Incoming Webhook" and click "Configure"
            5. Enter a name for the webhook (e.g., "AI PM Buddy")
            6. Optionally upload an icon
            7. Click "Create"
            8. Copy the webhook URL provided
            """)
            
            webhook_url = st.text_input("Teams Webhook URL")
            channel_name = st.text_input("Teams Channel Name")
            
            submitted = st.form_submit_button("Save Teams Configuration")
            if submitted and webhook_url and channel_name:
                # Test connection before saving
                st.info("Testing Teams connection...")
                
                # In a real implementation, we would test the connection here
                # This is a placeholder for demonstration purposes
                connection_successful = True
                
                if connection_successful:
                    teams_config['configured'] = True
                    teams_config['webhook_url'] = webhook_url
                    teams_config['channel_name'] = channel_name
                    
                    st.success("Microsoft Teams configuration saved successfully!")
                    st.experimental_rerun()
                else:
                    st.error("Failed to connect to Microsoft Teams. Please check your webhook URL and try again.")

def show_teams_message_center(project_data):
    """
    Display Microsoft Teams message center for sending updates.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.markdown("### Teams Message Center")
    
    teams_config = project_data['teams_config']
    
    if not teams_config['configured']:
        st.warning("Please configure Microsoft Teams integration before sending messages.")
        st.markdown("Go to the **Configuration** tab to set up your Teams connection.")
        return
    
    # Message composition
    st.markdown("#### Compose Message")
    
    message_type = st.selectbox(
        "Message Type",
        ["Project Update", "Status Report", "Risk Alert", "Milestone Notification", "Custom Message"]
    )
    
    # Different form fields based on message type
    if message_type == "Project Update":
        with st.form("teams_project_update_form"):
            update_title = st.text_input("Update Title")
            update_message = st.text_area("Update Details")
            include_progress = st.checkbox("Include Progress Chart", value=True)
            
            submitted = st.form_submit_button("Send Project Update")
            if submitted and update_title and update_message:
                # In a real implementation, this would send a message to Teams
                send_teams_message(
                    teams_config,
                    title=f"Project Update: {update_title}",
                    message=update_message,
                    include_chart=include_progress,
                    project_data=project_data
                )
                
                st.success("Project update sent to Microsoft Teams!")
                teams_config['last_message'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    elif message_type == "Status Report":
        with st.form("teams_status_report_form"):
            report_date = st.date_input("Report Date", datetime.datetime.now())
            status_summary = st.text_area("Status Summary")
            
            # Status details
            st.markdown("**Status Details**")
            col1, col2 = st.columns(2)
            
            with col1:
                schedule_status = st.selectbox("Schedule Status", ["On Track", "At Risk", "Delayed"])
                budget_status = st.selectbox("Budget Status", ["On Track", "At Risk", "Over Budget"])
            
            with col2:
                scope_status = st.selectbox("Scope Status", ["On Track", "At Risk", "Changed"])
                resource_status = st.selectbox("Resource Status", ["Sufficient", "At Risk", "Insufficient"])
            
            key_achievements = st.text_area("Key Achievements")
            key_challenges = st.text_area("Key Challenges")
            next_steps = st.text_area("Next Steps")
            
            submitted = st.form_submit_button("Send Status Report")
            if submitted and status_summary:
                # In a real implementation, this would send a message to Teams
                status_message = f"""
                **Status Summary:**
                {status_summary}
                
                **Schedule:** {schedule_status}
                **Budget:** {budget_status}
                **Scope:** {scope_status}
                **Resources:** {resource_status}
                
                **Key Achievements:**
                {key_achievements}
                
                **Key Challenges:**
                {key_challenges}
                
                **Next Steps:**
                {next_steps}
                """
                
                send_teams_message(
                    teams_config,
                    title=f"Status Report: {report_date.strftime('%Y-%m-%d')}",
                    message=status_message,
                    project_data=project_data
                )
                
                st.success("Status report sent to Microsoft Teams!")
                teams_config['last_message'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    elif message_type == "Risk Alert":
        with st.form("teams_risk_alert_form"):
            risk_title = st.text_input("Risk Title")
            risk_description = st.text_area("Risk Description")
            risk_impact = st.selectbox("Risk Impact", ["Low", "Medium", "High", "Critical"])
            risk_probability = st.selectbox("Risk Probability", ["Low", "Medium", "High", "Very High"])
            
            mitigation_plan = st.text_area("Mitigation Plan")
            
            submitted = st.form_submit_button("Send Risk Alert")
            if submitted and risk_title and risk_description:
                # In a real implementation, this would send a message to Teams
                risk_message = f"""
                **Risk Description:**
                {risk_description}
                
                **Impact:** {risk_impact}
                **Probability:** {risk_probability}
                
                **Mitigation Plan:**
                {mitigation_plan}
                """
                
                # Determine color based on impact
                color = "#1e81b0"  # Default blue
                if risk_impact == "Critical":
                    color = "#e63946"  # Red
                elif risk_impact == "High":
                    color = "#f28c28"  # Orange
                elif risk_impact == "Medium":
                    color = "#ffd166"  # Yellow
                
                send_teams_message(
                    teams_config,
                    title=f"Risk Alert: {risk_title}",
                    message=risk_message,
                    color=color,
                    project_data=project_data
                )
                
                st.success("Risk alert sent to Microsoft Teams!")
                teams_config['last_message'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    elif message_type == "Milestone Notification":
        with st.form("teams_milestone_form"):
            milestone_name = st.text_input("Milestone Name")
            milestone_date = st.date_input("Milestone Date")
            milestone_status = st.selectbox("Status", ["Completed", "On Track", "At Risk", "Delayed"])
            milestone_description = st.text_area("Description")
            
            submitted = st.form_submit_button("Send Milestone Notification")
            if submitted and milestone_name:
                # In a real implementation, this would send a message to Teams
                milestone_message = f"""
                **Milestone:** {milestone_name}
                **Date:** {milestone_date.strftime('%Y-%m-%d')}
                **Status:** {milestone_status}
                
                **Description:**
                {milestone_description}
                """
                
                # Determine color based on status
                color = "#1e81b0"  # Default blue
                if milestone_status == "Completed":
                    color = "#06d6a0"  # Green
                elif milestone_status == "At Risk":
                    color = "#ffd166"  # Yellow
                elif milestone_status == "Delayed":
                    color = "#e63946"  # Red
                
                send_teams_message(
                    teams_config,
                    title=f"Milestone Update: {milestone_name}",
                    message=milestone_message,
                    color=color,
                    project_data=project_data
                )
                
                st.success("Milestone notification sent to Microsoft Teams!")
                teams_config['last_message'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    else:  # Custom Message
        with st.form("teams_custom_message_form"):
            message_title = st.text_input("Message Title")
            message_body = st.text_area("Message Body")
            
            # Formatting options
            st.markdown("**Formatting Options**")
            col1, col2 = st.columns(2)
            
            with col1:
                include_header = st.checkbox("Include Project Header", value=True)
                include_footer = st.checkbox("Include Footer", value=True)
            
            with col2:
                message_color = st.color_picker("Message Color", "#1e81b0")
                include_timestamp = st.checkbox("Include Timestamp", value=True)
            
            submitted = st.form_submit_button("Send Custom Message")
            if submitted and message_title and message_body:
                # In a real implementation, this would send a message to Teams
                custom_message = message_body
                
                if include_timestamp:
                    custom_message += f"\n\n*Sent: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}*"
                
                send_teams_message(
                    teams_config,
                    title=message_title,
                    message=custom_message,
                    color=message_color,
                    include_header=include_header,
                    include_footer=include_footer,
                    project_data=project_data
                )
                
                st.success("Custom message sent to Microsoft Teams!")
                teams_config['last_message'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Message history
    st.markdown("#### Message History")
    
    # Initialize message history if not present
    if 'teams_messages' not in project_data:
        project_data['teams_messages'] = []
    
    if project_data['teams_messages']:
        for i, msg in enumerate(reversed(project_data['teams_messages'])):
            if i < 5:  # Show only 5 most recent messages
                with st.expander(f"{msg['title']} ({msg['timestamp']})"):
                    st.markdown(msg['message'])
    else:
        st.info("No messages have been sent yet")

def show_teams_notification_rules(project_data):
    """
    Display and manage Teams notification rules.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.markdown("### Teams Notification Rules")
    
    teams_config = project_data['teams_config']
    
    if not teams_config['configured']:
        st.warning("Please configure Microsoft Teams integration before setting up notification rules.")
        st.markdown("Go to the **Configuration** tab to set up your Teams connection.")
        return
    
    # Initialize notification rules if not present
    if 'teams_rules' not in project_data:
        project_data['teams_rules'] = {
            'enabled': False,
            'rules': []
        }
    
    # Enable/disable automatic notifications
    auto_notifications = st.checkbox("Enable Automatic Notifications", value=project_data['teams_rules']['enabled'])
    project_data['teams_rules']['enabled'] = auto_notifications
    
    if auto_notifications:
        st.markdown("#### Configure Notification Rules")
        
        # Existing rules
        if project_data['teams_rules']['rules']:
            st.markdown("**Current Rules:**")
            
            for i, rule in enumerate(project_data['teams_rules']['rules']):
                with st.expander(f"Rule {i+1}: {rule['event']}"):
                    st.markdown(f"**Event:** {rule['event']}")
                    st.markdown(f"**Condition:** {rule['condition']}")
                    st.markdown(f"**Channel:** {rule['channel']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Edit", key=f"edit_rule_{i}"):
                            st.session_state.edit_rule_index = i
                            st.experimental_rerun()
                    
                    with col2:
                        if st.button("Delete", key=f"delete_rule_{i}"):
                            project_data['teams_rules']['rules'].pop(i)
                            st.success(f"Rule {i+1} deleted")
                            st.experimental_rerun()
        
        # Add or edit rule
        st.markdown("#### " + ("Edit Rule" if hasattr(st.session_state, 'edit_rule_index') else "Add New Rule"))
        
        # Get the rule being edited, if any
        edit_rule = None
        if hasattr(st.session_state, 'edit_rule_index'):
            edit_rule = project_data['teams_rules']['rules'][st.session_state.edit_rule_index]
        
        with st.form("teams_rule_form"):
            event_type = st.selectbox(
                "Event Type",
                [
                    "Task Status Change",
                    "Risk Level Change",
                    "Resource Overallocation",
                    "Milestone Approaching",
                    "Project Deadline Approaching",
                    "Budget Threshold Exceeded",
                    "New Team Member Added",
                    "Document Approved",
                    "RAID Log Updated",
                    "Decision Required"
                ],
                index=[
                    "Task Status Change",
                    "Risk Level Change",
                    "Resource Overallocation",
                    "Milestone Approaching",
                    "Project Deadline Approaching",
                    "Budget Threshold Exceeded",
                    "New Team Member Added",
                    "Document Approved",
                    "RAID Log Updated",
                    "Decision Required"
                ].index(edit_rule['event']) if edit_rule else 0
            )
            
            # Condition based on event type
            condition_label = "Condition"
            condition_options = []
            default_index = 0
            
            if event_type == "Task Status Change":
                condition_label = "Status Changes To"
                condition_options = ["Completed", "In Progress", "Delayed", "Blocked", "Any Change"]
            elif event_type == "Risk Level Change":
                condition_label = "Risk Level Becomes"
                condition_options = ["Low", "Medium", "High", "Critical", "Any Change"]
            elif event_type == "Resource Overallocation":
                condition_label = "Allocation Exceeds"
                condition_options = ["100%", "110%", "125%", "150%", "Any Overallocation"]
            elif event_type == "Milestone Approaching":
                condition_label = "Days Before Milestone"
                condition_options = ["1 Day", "3 Days", "1 Week", "2 Weeks", "Any Milestone"]
            elif event_type == "Project Deadline Approaching":
                condition_label = "Days Before Deadline"
                condition_options = ["1 Day", "3 Days", "1 Week", "2 Weeks", "1 Month"]
            elif event_type == "Budget Threshold Exceeded":
                condition_label = "Budget Exceeds"
                condition_options = ["80% of Allocation", "90% of Allocation", "100% of Allocation", "Any Overspend"]
            elif event_type == "New Team Member Added":
                condition_label = "Team Member Role"
                condition_options = ["Developer", "Designer", "QA", "Manager", "Any Role"]
            elif event_type == "Document Approved":
                condition_label = "Document Type"
                condition_options = ["Requirements", "Design", "Technical Specification", "Any Document"]
            elif event_type == "RAID Log Updated":
                condition_label = "Entry Type"
                condition_options = ["Risk", "Assumption", "Issue", "Dependency", "Any Entry"]
            elif event_type == "Decision Required":
                condition_label = "Priority"
                condition_options = ["Low", "Medium", "High", "Critical", "Any Priority"]
            
            # Set default condition index if editing
            if edit_rule and edit_rule['event'] == event_type:
                try:
                    default_index = condition_options.index(edit_rule['condition'])
                except ValueError:
                    default_index = 0
            
            condition = st.selectbox(condition_label, condition_options, index=default_index)
            
            # Message format and channel
            message_format = st.text_area(
                "Message Format Template",
                value=edit_rule['message_format'] if edit_rule else f"[{event_type}] - {{details}}",
                help="Use {{details}} as a placeholder for the event details"
            )
            
            channel = st.text_input(
                "Teams Channel",
                value=edit_rule['channel'] if edit_rule else teams_config['channel_name']
            )
            
            # Enable/disable rule
            enabled = st.checkbox(
                "Rule Enabled",
                value=edit_rule['enabled'] if edit_rule else True
            )
            
            # Submit buttons
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Save Rule")
                if submitted:
                    new_rule = {
                        'event': event_type,
                        'condition': condition,
                        'message_format': message_format,
                        'channel': channel,
                        'enabled': enabled
                    }
                    
                    if hasattr(st.session_state, 'edit_rule_index'):
                        # Update existing rule
                        project_data['teams_rules']['rules'][st.session_state.edit_rule_index] = new_rule
                        st.success("Rule updated successfully!")
                        delattr(st.session_state, 'edit_rule_index')
                    else:
                        # Add new rule
                        project_data['teams_rules']['rules'].append(new_rule)
                        st.success("Rule added successfully!")
                    
                    st.experimental_rerun()
            
            with col2:
                if hasattr(st.session_state, 'edit_rule_index'):
                    cancel = st.form_submit_button("Cancel Edit")
                    if cancel:
                        delattr(st.session_state, 'edit_rule_index')
                        st.experimental_rerun()
        
        # Test the rules
        st.markdown("#### Test Rules")
        
        with st.form("test_rules_form"):
            test_event = st.selectbox(
                "Test Event",
                [rule['event'] for rule in project_data['teams_rules']['rules']] if project_data['teams_rules']['rules'] else ["No rules to test"]
            )
            
            test_submitted = st.form_submit_button("Test Notification")
            if test_submitted and project_data['teams_rules']['rules']:
                # Find the rule for the selected event
                test_rule = next((rule for rule in project_data['teams_rules']['rules'] if rule['event'] == test_event), None)
                
                if test_rule and test_rule['enabled']:
                    # In a real implementation, this would send a message to Teams
                    test_message = test_rule['message_format'].replace("{details}", f"This is a test notification for the {test_event} event")
                    
                    send_teams_message(
                        teams_config,
                        title=f"Test: {test_event}",
                        message=test_message,
                        project_data=project_data
                    )
                    
                    st.success(f"Test notification for '{test_event}' sent to Microsoft Teams!")
                    teams_config['last_message'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                else:
                    st.error(f"Rule for '{test_event}' is disabled or not found")

def send_teams_message(teams_config, title, message, color="#1e81b0", include_chart=False, include_header=True, include_footer=True, project_data=None):
    """
    Send a message to Microsoft Teams channel.
    In a real implementation, this would use the Teams webhook API.
    
    Args:
        teams_config: Teams configuration dictionary
        title: Message title
        message: Message body
        color: Accent color for the message
        include_chart: Whether to include a chart
        include_header: Whether to include the project header
        include_footer: Whether to include a footer
        project_data: Project data dictionary
    """
    # In a real implementation, this would send a POST request to the Teams webhook URL
    # This is a placeholder for demonstration purposes
    
    # Store the message in history
    if 'teams_messages' not in project_data:
        project_data['teams_messages'] = []
    
    project_data['teams_messages'].append({
        'title': title,
        'message': message,
        'color': color,
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    
    # Limit history to 20 messages
    project_data['teams_messages'] = project_data['teams_messages'][-20:] if len(project_data['teams_messages']) > 20 else project_data['teams_messages']