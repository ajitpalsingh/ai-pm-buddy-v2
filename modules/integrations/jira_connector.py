import streamlit as st
import pandas as pd
import datetime
import json
import requests
from io import StringIO

def show_jira_connector(project_data):
    """
    Display the JIRA Connector module.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.markdown("<h2 class='module-header'>JIRA Integration</h2>", unsafe_allow_html=True)
    
    # Initialize JIRA configuration if not present
    if 'jira_config' not in project_data:
        project_data['jira_config'] = {
            'configured': False,
            'url': '',
            'username': '',
            'api_token': '',
            'project_key': '',
            'last_sync': None
        }
    
    # Create tabs for JIRA functionality
    tab1, tab2, tab3, tab4 = st.tabs(["⚙️ Configuration", "🔄 Sync Tasks", "📊 Dashboard", "📋 Issue Tracker"])
    
    with tab1:
        show_jira_configuration(project_data)
    
    with tab2:
        show_jira_sync(project_data)
    
    with tab3:
        show_jira_dashboard(project_data)
    
    with tab4:
        show_jira_issue_tracker(project_data)

def show_jira_configuration(project_data):
    """
    Display and manage JIRA configuration.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.markdown("### JIRA Configuration")
    
    jira_config = project_data['jira_config']
    
    # Configuration status
    if jira_config['configured']:
        st.success("JIRA integration is configured")
        st.markdown(f"**JIRA URL:** {jira_config['url']}")
        st.markdown(f"**Username:** {jira_config['username']}")
        st.markdown(f"**Project Key:** {jira_config['project_key']}")
        
        if jira_config['last_sync']:
            st.markdown(f"**Last Synchronized:** {jira_config['last_sync']}")
        else:
            st.warning("No synchronization has been performed yet")
        
        # Option to reconfigure
        if st.button("Reconfigure JIRA Connection"):
            jira_config['configured'] = False
            st.experimental_rerun()
    else:
        st.warning("JIRA integration is not configured")
        
        # Configuration form
        with st.form("jira_config_form"):
            jira_url = st.text_input("JIRA URL (e.g., https://your-domain.atlassian.net)")
            username = st.text_input("JIRA Email/Username")
            api_token = st.text_input("JIRA API Token", type="password")
            project_key = st.text_input("JIRA Project Key")
            
            submitted = st.form_submit_button("Save JIRA Configuration")
            if submitted and jira_url and username and api_token and project_key:
                # Test connection before saving
                st.info("Testing JIRA connection...")
                
                # In a real implementation, we would test the connection here
                # This is a placeholder for demonstration purposes
                connection_successful = True
                
                if connection_successful:
                    jira_config['configured'] = True
                    jira_config['url'] = jira_url
                    jira_config['username'] = username
                    jira_config['api_token'] = api_token
                    jira_config['project_key'] = project_key
                    
                    st.success("JIRA configuration saved successfully!")
                    st.experimental_rerun()
                else:
                    st.error("Failed to connect to JIRA. Please check your credentials and try again.")
    
    # Advanced settings
    if jira_config['configured']:
        with st.expander("Advanced Settings"):
            sync_frequency = st.selectbox(
                "Synchronization Frequency",
                ["Manual", "Hourly", "Daily", "Weekly"],
                index=0
            )
            
            sync_direction = st.radio(
                "Synchronization Direction",
                ["Two-way", "JIRA to PM Buddy", "PM Buddy to JIRA"],
                horizontal=True
            )
            
            field_mappings = st.checkbox("Customize Field Mappings", value=False)
            if field_mappings:
                st.markdown("#### Field Mappings")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**PM Buddy Field**")
                    st.markdown("Task Name")
                    st.markdown("Start Date")
                    st.markdown("End Date")
                    st.markdown("Status")
                    st.markdown("Assignee")
                    st.markdown("Priority")
                
                with col2:
                    st.markdown("**JIRA Field**")
                    st.selectbox("Task Name", ["Summary", "Title", "Name"], index=0, key="map_name")
                    st.selectbox("Start Date", ["Start Date", "Custom Field", "None"], index=0, key="map_start")
                    st.selectbox("End Date", ["Due Date", "Custom Field", "None"], index=0, key="map_end")
                    st.selectbox("Status", ["Status", "Custom Field"], index=0, key="map_status")
                    st.selectbox("Assignee", ["Assignee", "Custom Field"], index=0, key="map_assignee")
                    st.selectbox("Priority", ["Priority", "Custom Field", "None"], index=0, key="map_priority")
            
            if st.button("Save Advanced Settings"):
                # In a real implementation, we would save these settings
                st.success("Advanced settings saved successfully!")

def show_jira_sync(project_data):
    """
    Display and manage JIRA task synchronization.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.markdown("### Synchronize with JIRA")
    
    jira_config = project_data['jira_config']
    
    if not jira_config['configured']:
        st.warning("Please configure JIRA integration before synchronizing tasks.")
        st.markdown("Go to the **Configuration** tab to set up your JIRA connection.")
        return
    
    # Initialize JIRA data if not present
    if 'jira_data' not in project_data:
        project_data['jira_data'] = {
            'issues': [],
            'sync_log': []
        }
    
    # Sync options
    st.markdown("#### Synchronization Options")
    
    sync_direction = st.radio(
        "Synchronization Direction",
        ["Two-way Sync", "Import from JIRA", "Export to JIRA"],
        horizontal=True
    )
    
    # What to sync
    st.markdown("#### What to Synchronize")
    
    sync_tasks = st.checkbox("Tasks/Issues", value=True)
    sync_users = st.checkbox("Users/Assignees", value=True)
    sync_statuses = st.checkbox("Statuses", value=True)
    sync_comments = st.checkbox("Comments", value=False)
    sync_attachments = st.checkbox("Attachments", value=False)
    
    # JQL filter for advanced users
    use_jql = st.checkbox("Use JQL Filter", value=False)
    jql_query = ""
    if use_jql:
        jql_query = st.text_area(
            "JQL Query",
            'project = "' + jira_config['project_key'] + '" AND status != Closed ORDER BY priority DESC'
        )
    
    # Sync button
    if st.button("Start Synchronization"):
        with st.spinner("Synchronizing with JIRA..."):
            # In a real implementation, this would actually sync with JIRA
            # This is a placeholder for demonstration purposes
            
            # Simulate importing tasks from JIRA
            mock_jira_import(project_data)
            
            # Update last sync time
            jira_config['last_sync'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # Add to sync log
            project_data['jira_data']['sync_log'].append({
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                'direction': sync_direction,
                'tasks_synced': len(project_data['jira_data']['issues']),
                'status': 'Success'
            })
            
            st.success("Synchronization completed successfully!")
    
    # Sync history
    if project_data['jira_data']['sync_log']:
        st.markdown("#### Synchronization History")
        
        sync_log_df = pd.DataFrame(project_data['jira_data']['sync_log'])
        st.dataframe(sync_log_df)
        
        if st.button("Clear Sync History"):
            project_data['jira_data']['sync_log'] = []
            st.success("Synchronization history cleared")
            st.experimental_rerun()

def show_jira_dashboard(project_data):
    """
    Display JIRA dashboard with project metrics.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.markdown("### JIRA Dashboard")
    
    jira_config = project_data['jira_config']
    
    if not jira_config['configured']:
        st.warning("Please configure JIRA integration to view the dashboard.")
        st.markdown("Go to the **Configuration** tab to set up your JIRA connection.")
        return
    
    # Check if we have JIRA data
    if 'jira_data' not in project_data or not project_data['jira_data']['issues']:
        st.info("No JIRA data available. Please synchronize with JIRA first.")
        st.markdown("Go to the **Sync Tasks** tab to synchronize with JIRA.")
        return
    
    # Create a dashboard with metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Issues", len(project_data['jira_data']['issues']))
    
    with col2:
        open_issues = len([i for i in project_data['jira_data']['issues'] if i['status'] != 'Done'])
        st.metric("Open Issues", open_issues)
    
    with col3:
        if project_data['jira_data']['issues']:
            high_priority = len([i for i in project_data['jira_data']['issues'] if i['priority'] in ['High', 'Highest']])
            st.metric("High Priority", high_priority)
    
    # Status distribution
    st.markdown("#### Issue Status Distribution")
    if project_data['jira_data']['issues']:
        status_counts = {}
        for issue in project_data['jira_data']['issues']:
            status = issue['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        status_df = pd.DataFrame({'Status': status_counts.keys(), 'Count': status_counts.values()})
        
        # In a real implementation, this would be a chart
        st.dataframe(status_df)
    
    # Priority distribution
    st.markdown("#### Issue Priority Distribution")
    if project_data['jira_data']['issues']:
        priority_counts = {}
        for issue in project_data['jira_data']['issues']:
            priority = issue['priority']
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        priority_df = pd.DataFrame({'Priority': priority_counts.keys(), 'Count': priority_counts.values()})
        
        # In a real implementation, this would be a chart
        st.dataframe(priority_df)
    
    # Recent activity
    st.markdown("#### Recent Activity")
    if project_data['jira_data']['issues']:
        recent_issues = sorted(project_data['jira_data']['issues'], key=lambda x: x['updated'], reverse=True)[:5]
        for issue in recent_issues:
            st.markdown(f"**{issue['key']}:** {issue['summary']} ({issue['status']})")
            st.caption(f"Updated: {issue['updated']} | Assignee: {issue['assignee']}")

def show_jira_issue_tracker(project_data):
    """
    Display and manage JIRA issues.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.markdown("### JIRA Issue Tracker")
    
    jira_config = project_data['jira_config']
    
    if not jira_config['configured']:
        st.warning("Please configure JIRA integration to manage issues.")
        st.markdown("Go to the **Configuration** tab to set up your JIRA connection.")
        return
    
    # Check if we have JIRA data
    if 'jira_data' not in project_data or not project_data['jira_data']['issues']:
        st.info("No JIRA data available. Please synchronize with JIRA first.")
        st.markdown("Go to the **Sync Tasks** tab to synchronize with JIRA.")
        return
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.multiselect(
            "Filter by Status",
            list(set(i['status'] for i in project_data['jira_data']['issues'])),
            default=list(set(i['status'] for i in project_data['jira_data']['issues']))
        )
    
    with col2:
        priority_filter = st.multiselect(
            "Filter by Priority",
            list(set(i['priority'] for i in project_data['jira_data']['issues'])),
            default=list(set(i['priority'] for i in project_data['jira_data']['issues']))
        )
    
    with col3:
        assignee_filter = st.multiselect(
            "Filter by Assignee",
            list(set(i['assignee'] for i in project_data['jira_data']['issues'])),
            default=list(set(i['assignee'] for i in project_data['jira_data']['issues']))
        )
    
    # Text search
    search_query = st.text_input("Search Issues", "")
    
    # Apply filters
    filtered_issues = project_data['jira_data']['issues']
    
    if status_filter:
        filtered_issues = [i for i in filtered_issues if i['status'] in status_filter]
    
    if priority_filter:
        filtered_issues = [i for i in filtered_issues if i['priority'] in priority_filter]
    
    if assignee_filter:
        filtered_issues = [i for i in filtered_issues if i['assignee'] in assignee_filter]
    
    if search_query:
        filtered_issues = [i for i in filtered_issues if search_query.lower() in i['summary'].lower() or search_query.lower() in i['key'].lower()]
    
    # Display issues
    st.markdown(f"#### Issues ({len(filtered_issues)})")
    
    if filtered_issues:
        issue_df = pd.DataFrame([{
            'Key': i['key'],
            'Summary': i['summary'],
            'Status': i['status'],
            'Priority': i['priority'],
            'Assignee': i['assignee'],
            'Updated': i['updated']
        } for i in filtered_issues])
        
        st.dataframe(issue_df)
        
        # Issue details
        st.markdown("#### Issue Details")
        
        selected_issue_key = st.selectbox("Select Issue", [i['key'] for i in filtered_issues])
        selected_issue = next((i for i in filtered_issues if i['key'] == selected_issue_key), None)
        
        if selected_issue:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Key:** {selected_issue['key']}")
                st.markdown(f"**Summary:** {selected_issue['summary']}")
                st.markdown(f"**Description:** {selected_issue.get('description', 'No description')}")
            
            with col2:
                st.markdown(f"**Status:** {selected_issue['status']}")
                st.markdown(f"**Priority:** {selected_issue['priority']}")
                st.markdown(f"**Assignee:** {selected_issue['assignee']}")
                st.markdown(f"**Created:** {selected_issue['created']}")
                st.markdown(f"**Updated:** {selected_issue['updated']}")
            
            # Actions
            st.markdown("#### Actions")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Open in JIRA", key=f"open_{selected_issue['key']}"):
                    issue_url = f"{jira_config['url']}/browse/{selected_issue['key']}"
                    st.markdown(f"<a href='{issue_url}' target='_blank'>Open {selected_issue['key']} in JIRA</a>", unsafe_allow_html=True)
            
            with col2:
                new_status = st.selectbox(
                    "Change Status",
                    ["To Do", "In Progress", "Review", "Done"],
                    index=["To Do", "In Progress", "Review", "Done"].index(selected_issue['status']) if selected_issue['status'] in ["To Do", "In Progress", "Review", "Done"] else 0
                )
                
                if st.button("Update Status"):
                    # In a real implementation, this would update the status in JIRA
                    for i in project_data['jira_data']['issues']:
                        if i['key'] == selected_issue['key']:
                            i['status'] = new_status
                            i['updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    
                    st.success(f"Status updated to {new_status}")
                    st.experimental_rerun()
            
            with col3:
                new_assignee = st.selectbox(
                    "Reassign To",
                    list(set(i['assignee'] for i in project_data['jira_data']['issues']))
                )
                
                if st.button("Reassign"):
                    # In a real implementation, this would reassign the issue in JIRA
                    for i in project_data['jira_data']['issues']:
                        if i['key'] == selected_issue['key']:
                            i['assignee'] = new_assignee
                            i['updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    
                    st.success(f"Issue reassigned to {new_assignee}")
                    st.experimental_rerun()
    else:
        st.info("No issues match your filters")

def mock_jira_import(project_data):
    """
    Create mock JIRA data for demonstration purposes.
    In a real implementation, this would fetch data from JIRA API.
    
    Args:
        project_data: Dictionary containing project information
    """
    jira_config = project_data['jira_config']
    
    # Create mock JIRA issues
    mock_issues = [
        {
            'key': f"{jira_config['project_key']}-1",
            'summary': "Implement user authentication",
            'description': "Implement user authentication system using OAuth 2.0",
            'status': "In Progress",
            'priority': "High",
            'assignee': "John Smith",
            'created': (datetime.datetime.now() - datetime.timedelta(days=14)).strftime("%Y-%m-%d"),
            'updated': (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
        },
        {
            'key': f"{jira_config['project_key']}-2",
            'summary': "Design database schema",
            'description': "Create ERD and finalize database schema for the application",
            'status': "Done",
            'priority': "Highest",
            'assignee': "Jane Doe",
            'created': (datetime.datetime.now() - datetime.timedelta(days=20)).strftime("%Y-%m-%d"),
            'updated': (datetime.datetime.now() - datetime.timedelta(days=10)).strftime("%Y-%m-%d")
        },
        {
            'key': f"{jira_config['project_key']}-3",
            'summary': "Set up CI/CD pipeline",
            'description': "Configure Jenkins for continuous integration and deployment",
            'status': "To Do",
            'priority': "Medium",
            'assignee': "Unassigned",
            'created': (datetime.datetime.now() - datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
            'updated': (datetime.datetime.now() - datetime.timedelta(days=5)).strftime("%Y-%m-%d")
        },
        {
            'key': f"{jira_config['project_key']}-4",
            'summary': "Implement API endpoints",
            'description': "Create RESTful API endpoints for the application",
            'status': "In Progress",
            'priority': "High",
            'assignee': "John Smith",
            'created': (datetime.datetime.now() - datetime.timedelta(days=10)).strftime("%Y-%m-%d"),
            'updated': (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        },
        {
            'key': f"{jira_config['project_key']}-5",
            'summary': "Bug: User login failing on Firefox",
            'description': "Users are unable to log in when using Firefox browser",
            'status': "To Do",
            'priority': "Highest",
            'assignee': "Jane Doe",
            'created': (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d"),
            'updated': (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        },
        {
            'key': f"{jira_config['project_key']}-6",
            'summary': "Add unit tests for backend code",
            'description': "Implement unit tests for all backend services using Jest",
            'status': "To Do",
            'priority': "Medium",
            'assignee': "John Smith",
            'created': (datetime.datetime.now() - datetime.timedelta(days=3)).strftime("%Y-%m-%d"),
            'updated': (datetime.datetime.now() - datetime.timedelta(days=3)).strftime("%Y-%m-%d")
        },
        {
            'key': f"{jira_config['project_key']}-7",
            'summary': "Create user dashboard UI",
            'description': "Design and implement the user dashboard UI using React",
            'status': "Review",
            'priority': "Medium",
            'assignee': "Alice Johnson",
            'created': (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d"),
            'updated': (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        },
        {
            'key': f"{jira_config['project_key']}-8",
            'summary': "Optimize database queries",
            'description': "Improve performance of slow database queries",
            'status': "In Progress",
            'priority': "Low",
            'assignee': "Bob Wilson",
            'created': (datetime.datetime.now() - datetime.timedelta(days=4)).strftime("%Y-%m-%d"),
            'updated': (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        },
        {
            'key': f"{jira_config['project_key']}-9",
            'summary': "Update documentation",
            'description': "Update API documentation with new endpoints",
            'status': "Done",
            'priority': "Low",
            'assignee': "Carol Martinez",
            'created': (datetime.datetime.now() - datetime.timedelta(days=15)).strftime("%Y-%m-%d"),
            'updated': (datetime.datetime.now() - datetime.timedelta(days=12)).strftime("%Y-%m-%d")
        },
        {
            'key': f"{jira_config['project_key']}-10",
            'summary': "Security review",
            'description': "Conduct security review of the authentication system",
            'status': "To Do",
            'priority': "High",
            'assignee': "Unassigned",
            'created': (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            'updated': (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        }
    ]
    
    # Add mock issues to project data
    project_data['jira_data']['issues'] = mock_issues