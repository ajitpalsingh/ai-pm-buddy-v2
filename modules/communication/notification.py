import streamlit as st
import pandas as pd
import datetime
import json

def show_notification_center(project_data):
    """
    Display the Notification Center module.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.markdown("<h2 class='module-header'>Notification Center</h2>", unsafe_allow_html=True)
    
    # Initialize notifications if not present
    if 'notifications' not in project_data:
        project_data['notifications'] = []
        
        # Add some sample notifications for demo purposes
        sample_notifications = [
            {
                'id': 1,
                'title': 'Critical Path Delay',
                'message': 'Task "Database Implementation" is delayed by 3 days and is on the critical path.',
                'severity': 'Critical',
                'timestamp': (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M"),
                'read': False,
                'type': 'task',
                'related_id': 'task-5'
            },
            {
                'id': 2,
                'title': 'New Team Member Added',
                'message': 'John Doe has been added to the project team as Database Developer.',
                'severity': 'Info',
                'timestamp': (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d %H:%M"),
                'read': True,
                'type': 'resource',
                'related_id': 'resource-7'
            },
            {
                'id': 3,
                'title': 'Milestone Approaching',
                'message': 'Milestone "Phase 1 Completion" is scheduled for next week.',
                'severity': 'Warning',
                'timestamp': (datetime.datetime.now() - datetime.timedelta(days=3)).strftime("%Y-%m-%d %H:%M"),
                'read': False,
                'type': 'milestone',
                'related_id': 'milestone-2'
            }
        ]
        project_data['notifications'].extend(sample_notifications)
    
    # Layout with tabs for different notification views
    tab1, tab2, tab3 = st.tabs(["📬 All Notifications", "⚙️ Notification Settings", "🔄 Integration Status"])
    
    with tab1:
        show_all_notifications(project_data)
    
    with tab2:
        show_notification_settings(project_data)
        
    with tab3:
        show_integration_status(project_data)

def show_all_notifications(project_data):
    """
    Display all notifications with filtering and sorting options.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.markdown("### All Notifications")
    
    # Controls for filtering and sorting
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_severity = st.multiselect(
            "Filter by Severity",
            ["Critical", "Warning", "Info"],
            default=["Critical", "Warning", "Info"]
        )
    
    with col2:
        filter_read = st.radio(
            "Show",
            ["All", "Unread Only", "Read Only"],
            horizontal=True
        )
    
    with col3:
        sort_by = st.selectbox(
            "Sort by",
            ["Newest First", "Oldest First", "Severity (High to Low)", "Severity (Low to High)"]
        )
    
    # Filter notifications based on selections
    filtered_notifications = project_data['notifications']
    
    # Filter by severity
    if filter_severity:
        filtered_notifications = [n for n in filtered_notifications if n['severity'] in filter_severity]
    
    # Filter by read status
    if filter_read == "Unread Only":
        filtered_notifications = [n for n in filtered_notifications if not n['read']]
    elif filter_read == "Read Only":
        filtered_notifications = [n for n in filtered_notifications if n['read']]
    
    # Sort notifications
    if sort_by == "Newest First":
        filtered_notifications = sorted(filtered_notifications, key=lambda x: x['timestamp'], reverse=True)
    elif sort_by == "Oldest First":
        filtered_notifications = sorted(filtered_notifications, key=lambda x: x['timestamp'])
    elif sort_by == "Severity (High to Low)":
        severity_order = {"Critical": 3, "Warning": 2, "Info": 1}
        filtered_notifications = sorted(filtered_notifications, key=lambda x: severity_order.get(x['severity'], 0), reverse=True)
    elif sort_by == "Severity (Low to High)":
        severity_order = {"Critical": 3, "Warning": 2, "Info": 1}
        filtered_notifications = sorted(filtered_notifications, key=lambda x: severity_order.get(x['severity'], 0))
    
    # Display notification count
    st.markdown(f"**{len(filtered_notifications)}** notifications")
    
    # Mark all as read button
    if st.button("Mark All as Read"):
        for notification in project_data['notifications']:
            notification['read'] = True
        st.success("All notifications marked as read")
        st.experimental_rerun()
    
    # Display notifications
    if filtered_notifications:
        for notification in filtered_notifications:
            # Determine color based on severity
            if notification['severity'] == 'Critical':
                container_style = "border-left: 4px solid #ff4b4b; padding-left: 10px;"
            elif notification['severity'] == 'Warning':
                container_style = "border-left: 4px solid #ffa62b; padding-left: 10px;"
            else:  # Info
                container_style = "border-left: 4px solid #36a2eb; padding-left: 10px;"
            
            # Notification container
            st.markdown(f"<div style='{container_style}'>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([5, 1])
            
            with col1:
                # Title with read/unread indicator
                read_indicator = "🔵" if not notification['read'] else ""
                st.markdown(f"**{notification['title']}** {read_indicator}")
                st.markdown(f"*{notification['message']}*")
                st.caption(f"{notification['timestamp']} | {notification['severity']}")
            
            with col2:
                # Action buttons
                if st.button("View", key=f"view_{notification['id']}"):
                    # Set as read
                    for n in project_data['notifications']:
                        if n['id'] == notification['id']:
                            n['read'] = True
                    
                    # In a real implementation, link to the related item
                    st.info(f"Redirecting to {notification['type']} with ID {notification['related_id']}")
                
                if st.button("Dismiss", key=f"dismiss_{notification['id']}"):
                    # Remove from list
                    project_data['notifications'] = [n for n in project_data['notifications'] if n['id'] != notification['id']]
                    st.success("Notification dismissed")
                    st.experimental_rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("---")
    else:
        st.info("No notifications match your filters")

def show_notification_settings(project_data):
    """
    Display and manage notification settings.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.markdown("### Notification Settings")
    
    # Initialize notification settings if not present
    if 'notification_settings' not in project_data:
        project_data['notification_settings'] = {
            'email_notifications': False,
            'desktop_notifications': True,
            'push_notifications': False,
            'email_address': '',
            'notification_types': [
                'Critical Path Changes',
                'Risk Score Updates',
                'Resource Conflicts',
                'Milestone Updates'
            ],
            'daily_digest': False,
            'weekly_summary': True
        }
    
    settings = project_data['notification_settings']
    
    # Notification channels
    st.markdown("#### Notification Channels")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        settings['desktop_notifications'] = st.checkbox("In-App Notifications", value=settings['desktop_notifications'])
    
    with col2:
        settings['email_notifications'] = st.checkbox("Email Notifications", value=settings['email_notifications'])
        if settings['email_notifications']:
            settings['email_address'] = st.text_input("Email Address", value=settings.get('email_address', ''))
    
    with col3:
        settings['push_notifications'] = st.checkbox("Push Notifications", value=settings['push_notifications'])
        if settings['push_notifications']:
            st.info("Push notifications require mobile app installation")
    
    # Notification types
    st.markdown("#### Notification Types")
    notification_types = [
        'Critical Path Changes',
        'Risk Score Updates',
        'Resource Conflicts',
        'Milestone Updates',
        'Task Status Changes',
        'Team Member Updates',
        'Budget Alerts',
        'Scope Change Requests',
        'Meeting Reminders',
        'Decision Log Updates'
    ]
    
    settings['notification_types'] = st.multiselect(
        "Select which events should trigger notifications:",
        notification_types,
        default=settings.get('notification_types', [])
    )
    
    # Digest settings
    st.markdown("#### Summary & Digest Settings")
    col1, col2 = st.columns(2)
    
    with col1:
        settings['daily_digest'] = st.checkbox("Daily Digest Email", value=settings.get('daily_digest', False))
        if settings['daily_digest']:
            settings['daily_digest_time'] = st.time_input("Send at", datetime.time(17, 0))
    
    with col2:
        settings['weekly_summary'] = st.checkbox("Weekly Project Summary", value=settings.get('weekly_summary', True))
        if settings['weekly_summary']:
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            settings['weekly_summary_day'] = st.selectbox("Send on", days, index=days.index(settings.get('weekly_summary_day', 'Friday')) if 'weekly_summary_day' in settings else 4)
    
    # Save settings
    if st.button("Save Notification Settings"):
        project_data['notification_settings'] = settings
        st.success("Notification settings saved successfully!")
        
    # Test notification
    st.markdown("#### Test Notifications")
    with st.form("test_notification_form"):
        notification_title = st.text_input("Test Notification Title", "Test Notification")
        notification_message = st.text_area("Test Notification Message", "This is a test notification from AI PM Buddy.")
        notification_severity = st.selectbox("Severity", ["Info", "Warning", "Critical"])
        
        submit_test = st.form_submit_button("Send Test Notification")
        if submit_test:
            new_notification = {
                'id': max([n['id'] for n in project_data['notifications']], default=0) + 1,
                'title': notification_title,
                'message': notification_message,
                'severity': notification_severity,
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                'read': False,
                'type': 'test',
                'related_id': None
            }
            project_data['notifications'].append(new_notification)
            
            # Show success message with different notification methods
            channels = []
            if settings['desktop_notifications']:
                channels.append("in-app")
            if settings['email_notifications'] and settings.get('email_address'):
                channels.append(f"email ({settings['email_address']})")
            if settings['push_notifications']:
                channels.append("push notification")
            
            if channels:
                st.success(f"Test notification sent via {', '.join(channels)}")
            else:
                st.warning("Test notification added, but no notification channels are enabled")
            
            st.experimental_rerun()

def show_integration_status(project_data):
    """
    Display status of notification integrations.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.markdown("### Integration Status")
    
    # Initialize integrations if not present
    if 'notification_integrations' not in project_data:
        project_data['notification_integrations'] = {
            'email': {
                'status': 'Not Configured',
                'provider': 'None',
                'last_checked': None
            },
            'sms': {
                'status': 'Not Configured',
                'provider': 'None',
                'last_checked': None
            },
            'ms_teams': {
                'status': 'Not Configured',
                'webhook_url': '',
                'last_checked': None
            },
            'slack': {
                'status': 'Not Configured',
                'webhook_url': '',
                'last_checked': None
            }
        }
    
    integrations = project_data['notification_integrations']
    
    # Display integration status
    integration_data = []
    for integration, details in integrations.items():
        integration_data.append({
            'Integration': integration.upper(),
            'Status': details['status'],
            'Provider/URL': details.get('provider', '') or details.get('webhook_url', ''),
            'Last Checked': details['last_checked'] or 'Never'
        })
    
    integration_df = pd.DataFrame(integration_data)
    st.dataframe(integration_df, width=800)
    
    # Configure integrations
    st.markdown("#### Configure Integrations")
    
    integration_to_configure = st.selectbox(
        "Select Integration to Configure",
        ["Email", "SMS", "Microsoft Teams", "Slack"]
    )
    
    if integration_to_configure == "Email":
        with st.form("email_integration_form"):
            email_provider = st.selectbox("Email Provider", ["SMTP", "SendGrid", "Mailchimp", "Amazon SES"])
            if email_provider == "SMTP":
                smtp_server = st.text_input("SMTP Server")
                smtp_port = st.number_input("SMTP Port", min_value=1, max_value=65535, value=587)
                smtp_username = st.text_input("Username")
                smtp_password = st.text_input("Password", type="password")
                use_tls = st.checkbox("Use TLS", value=True)
            else:
                api_key = st.text_input("API Key", type="password")
            
            sender_email = st.text_input("Sender Email Address")
            
            test_recipient = st.text_input("Test Recipient Email")
            
            submit_email = st.form_submit_button("Save Email Configuration")
            if submit_email:
                # In a real implementation, we would validate and test the connection
                integrations['email'] = {
                    'status': 'Configured',
                    'provider': email_provider,
                    'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                
                if test_recipient:
                    st.info(f"Test email would be sent to {test_recipient}")
                
                st.success("Email integration configured successfully!")
                st.experimental_rerun()
    
    elif integration_to_configure == "SMS":
        with st.form("sms_integration_form"):
            sms_provider = st.selectbox("SMS Provider", ["Twilio", "Nexmo", "AWS SNS"])
            
            if sms_provider == "Twilio":
                account_sid = st.text_input("Account SID")
                auth_token = st.text_input("Auth Token", type="password")
                phone_number = st.text_input("Twilio Phone Number")
            else:
                api_key = st.text_input("API Key", type="password")
                api_secret = st.text_input("API Secret", type="password")
            
            test_phone = st.text_input("Test Phone Number (with country code)")
            
            submit_sms = st.form_submit_button("Save SMS Configuration")
            if submit_sms:
                # In a real implementation, we would validate and test the connection
                integrations['sms'] = {
                    'status': 'Configured',
                    'provider': sms_provider,
                    'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                
                if test_phone:
                    st.info(f"Test SMS would be sent to {test_phone}")
                
                st.success("SMS integration configured successfully!")
                st.experimental_rerun()
    
    elif integration_to_configure == "Microsoft Teams":
        with st.form("teams_integration_form"):
            webhook_url = st.text_input("Teams Webhook URL")
            channel_name = st.text_input("Channel Name")
            
            submit_teams = st.form_submit_button("Save Teams Configuration")
            if submit_teams and webhook_url:
                # In a real implementation, we would validate and test the connection
                integrations['ms_teams'] = {
                    'status': 'Configured',
                    'webhook_url': webhook_url,
                    'channel_name': channel_name,
                    'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                
                st.success("Microsoft Teams integration configured successfully!")
                st.experimental_rerun()
    
    elif integration_to_configure == "Slack":
        with st.form("slack_integration_form"):
            webhook_url = st.text_input("Slack Webhook URL")
            channel_name = st.text_input("Channel Name")
            
            submit_slack = st.form_submit_button("Save Slack Configuration")
            if submit_slack and webhook_url:
                # In a real implementation, we would validate and test the connection
                integrations['slack'] = {
                    'status': 'Configured',
                    'webhook_url': webhook_url,
                    'channel_name': channel_name,
                    'last_checked': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                
                st.success("Slack integration configured successfully!")
                st.experimental_rerun()
    
    # Test integrations
    st.markdown("#### Test Integrations")
    col1, col2 = st.columns(2)
    
    with col1:
        integration_to_test = st.selectbox(
            "Select Integration to Test",
            ["Email", "SMS", "Microsoft Teams", "Slack"]
        )
    
    with col2:
        if st.button("Send Test Message"):
            integration_key = integration_to_test.lower().replace(" ", "_").replace("-", "_")
            if integration_key in integrations and integrations[integration_key]['status'] == 'Configured':
                st.success(f"Test message sent via {integration_to_test}")
                
                # Update last checked timestamp
                integrations[integration_key]['last_checked'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            else:
                st.error(f"{integration_to_test} is not configured yet")