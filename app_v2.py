import streamlit as st
import os
import pandas as pd
from datetime import datetime
import json
from pathlib import Path

# Import original modules
from modules.ai_insights import show_ai_insights
from modules.wbs_overview import show_wbs_overview
from modules.resource_allocation import show_resource_allocation
from modules.raid_checker import show_raid_checker
from modules.decision_log import show_decision_log
from modules.sentiment_analyzer import show_sentiment_analyzer
from modules.agile_coach import show_agile_coach
from modules.pm_knowledge import show_pm_knowledge
from modules.critical_path import show_critical_path
from modules.scope_detection import show_scope_detection

# Import new v2.0 modules
# Document Management
from modules.document_mgmt.generator import show_document_generator
from modules.document_mgmt.template_mgmt import show_template_management

# Scenario Simulation
from modules.simulation.risk_simulator import show_risk_simulator
from modules.simulation.what_if_analysis import show_what_if_analysis

# Communication Management
from modules.communication.team_communication import show_team_communication
from modules.communication.notification import show_notification_center

# Integrations
from modules.integrations.jira_connector import show_jira_connector
from modules.integrations.ms_teams import show_ms_teams_integration
# from modules.communication.notifications import show_notifications
# from modules.communication.meeting_summaries import show_meeting_summaries

# Onboarding - To be implemented
# from modules.onboarding.project_history import show_project_history
# from modules.onboarding.knowledge_extraction import show_knowledge_extraction

# Import utilities
from utils.data_utils import load_sample_data, save_data

# Constants
APP_TITLE = "AI PM Buddy v2.0"
APP_ICON = "📊"

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for improved UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4CAF50;
        margin-bottom: 1rem;
    }
    .module-header {
        font-size: 1.8rem;
        color: #4CAF50;
        margin-bottom: 0.8rem;
        border-bottom: 2px solid #4CAF50;
        padding-bottom: 0.3rem;
    }
    .project-title {
        font-size: 1.2rem;
        color: #333;
        font-weight: bold;
    }
    .dashboard-card {
        background-color: #f9f9f9;
        border-radius: 5px;
        padding: 1rem;
        border-left: 4px solid #4CAF50;
        margin-bottom: 1rem;
    }
    .sidebar-section {
        background-color: #f5f5f5;
        border-radius: 5px;
        padding: 0.8rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #e8f5e9;
        border-radius: 5px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .warning-box {
        background-color: #ffecb3;
        border-radius: 5px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .streamlit-expanderHeader {
        font-weight: bold;
        color: #333;
    }
    div.stButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 4px;
    }
    div.stButton > button:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'project_data' not in st.session_state:
    st.session_state.project_data = {}
    # Automatically create a sample project for testing
    st.session_state.project_data["Sample Project"] = load_sample_data()
    
if 'current_project' not in st.session_state:
    if "Sample Project" in st.session_state.project_data:
        st.session_state.current_project = "Sample Project"
    else:
        st.session_state.current_project = None
    
if 'current_view' not in st.session_state:
    st.session_state.current_view = "dashboard"
    
if 'notifications' not in st.session_state:
    st.session_state.notifications = []
    # Add sample notifications
    st.session_state.notifications.append({
        "id": 1,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "title": "Welcome to AI PM Buddy v2.0",
        "message": "Explore the new features in this upgraded version!",
        "type": "info",
        "read": False
    })

# For development in Replit - Remove this when running locally
if os.environ.get("REPL_ID"):
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

# Initialize OpenAI API key from environment or session
api_key = os.environ.get("OPENAI_API_KEY", "")
if 'openai_api_key' not in st.session_state:
    st.session_state.openai_api_key = api_key

def show_dashboard():
    """Display the main dashboard with project overview."""
    st.markdown('<h1 class="main-header">Project Dashboard</h1>', unsafe_allow_html=True)
    
    # Get current project data
    project_data = st.session_state.project_data.get(st.session_state.current_project, {})
    
    # Project overview cards in a 3-column layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("Project Progress")
        
        # Calculate overall project progress
        tasks = project_data.get('wbs', [])
        if tasks:
            total_duration = sum(task.get('duration', 0) for task in tasks)
            weighted_progress = sum((task.get('duration', 0) * task.get('progress', 0) / 100) for task in tasks)
            overall_progress = (weighted_progress / total_duration) * 100 if total_duration > 0 else 0
            
            # Create progress metric and bar
            st.metric("Overall Completion", f"{overall_progress:.1f}%")
            st.progress(overall_progress/100)
            
            # Status summary
            completed = len([t for t in tasks if t.get('progress', 0) >= 100])
            in_progress = len([t for t in tasks if t.get('progress', 0) > 0 and t.get('progress', 0) < 100])
            not_started = len([t for t in tasks if t.get('progress', 0) == 0])
            
            status_data = pd.DataFrame({
                'Status': ['Completed', 'In Progress', 'Not Started'],
                'Count': [completed, in_progress, not_started]
            })
            
            st.bar_chart(status_data.set_index('Status'), use_container_width=True)
        else:
            st.info("No tasks found in project.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("Resource Allocation")
        
        # Show resource allocation
        resources = project_data.get('resources', [])
        if resources:
            # Find overallocated and underutilized resources
            overallocated = [r for r in resources if r.get('allocated', 0) > r.get('availability', 0)]
            underutilized = [r for r in resources if r.get('allocated', 0) < 0.7 * r.get('availability', 0)]
            
            if overallocated:
                st.warning(f"{len(overallocated)} overallocated resources")
            else:
                st.success("No overallocated resources")
                
            if underutilized:
                st.info(f"{len(underutilized)} underutilized resources")
            
            # Show resource allocation chart
            resource_data = pd.DataFrame([{
                'Resource': r.get('name', ''),
                'Allocation %': (r.get('allocated', 0) / r.get('availability', 1) * 100)
            } for r in resources])
            
            st.bar_chart(resource_data.set_index('Resource'), use_container_width=True)
        else:
            st.info("No resources found in project.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("Risk Overview")
        
        # Show risk overview
        risks = project_data.get('risks', [])
        if risks:
            # Count risks by severity
            high_risks = len([r for r in risks if r.get('severity', '').lower() == 'high'])
            medium_risks = len([r for r in risks if r.get('severity', '').lower() == 'medium'])
            low_risks = len([r for r in risks if r.get('severity', '').lower() == 'low'])
            
            # Display risk metrics
            if high_risks > 0:
                st.error(f"{high_risks} high severity risks")
            else:
                st.success("No high severity risks")
            
            if medium_risks > 0:
                st.warning(f"{medium_risks} medium severity risks")
                
            if low_risks > 0:
                st.info(f"{low_risks} low severity risks")
            
            # Show risk chart
            risk_data = pd.DataFrame({
                'Severity': ['High', 'Medium', 'Low'],
                'Count': [high_risks, medium_risks, low_risks]
            })
            
            st.bar_chart(risk_data.set_index('Severity'), use_container_width=True)
        else:
            st.info("No risks found in project.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent activities
    st.markdown('<h2 class="module-header">Recent Activities</h2>', unsafe_allow_html=True)
    
    # Placeholder for actual recent activities
    activities = [
        {"timestamp": "2025-04-26 14:30", "user": "System", "action": "Project created", "details": "Initial project setup completed"},
        {"timestamp": "2025-04-26 15:45", "user": "AI Assistant", "action": "Risk analysis", "details": "Performed initial risk assessment"},
        {"timestamp": "2025-04-27 09:15", "user": "System", "action": "Resource update", "details": "Added 3 new team members to the project"}
    ]
    
    activities_df = pd.DataFrame(activities)
    st.dataframe(activities_df, use_container_width=True)
    
    # Upcoming deadlines
    st.markdown('<h2 class="module-header">Upcoming Deadlines</h2>', unsafe_allow_html=True)
    
    tasks = project_data.get('wbs', [])
    if tasks:
        # Sort tasks by end date and filter for upcoming deadlines
        upcoming_tasks = sorted(
            [t for t in tasks if t.get('progress', 0) < 100],
            key=lambda x: x.get('end_date', '9999-12-31')
        )[:5]  # Get top 5 upcoming tasks
        
        if upcoming_tasks:
            upcoming_df = pd.DataFrame([{
                'Task': t.get('task', ''),
                'Deadline': t.get('end_date', ''),
                'Progress': f"{t.get('progress', 0)}%",
                'Owner': t.get('owner', '')
            } for t in upcoming_tasks])
            
            st.dataframe(upcoming_df, use_container_width=True)
        else:
            st.info("No upcoming deadlines found.")
    else:
        st.info("No tasks found in project.")

def show_ai_assistant():
    """Display the AI Personal Assistant module."""
    st.markdown('<h1 class="main-header">AI Personal Assistant</h1>', unsafe_allow_html=True)
    
    # Check for OpenAI API key
    if not st.session_state.openai_api_key:
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.warning("⚠️ Please provide your OpenAI API key in the sidebar settings to enable AI assistant features.")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Daily briefing section
    st.markdown('<h2 class="module-header">Daily Project Briefing</h2>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.write("Your AI assistant can provide a daily summary of the most important aspects of your project.")
    
    if st.button("Generate Daily Briefing"):
        with st.spinner("Generating your daily briefing..."):
            # Placeholder for actual AI-generated content
            st.success("Daily briefing generated!")
            
            st.markdown("""
            ### Project Daily Briefing - Sample Project
            
            **Date:** April 27, 2025
            
            **High Priority Items:**
            1. 2 critical path tasks are behind schedule
            2. Resource "Developer 2" is overallocated at 125%
            3. New high severity risk identified related to vendor delays
            
            **Progress Update:**
            - Overall project is 47.5% complete (on track)
            - Sprint 3 ends this Friday with 4 incomplete tasks
            - UAT environment is now ready for testing
            
            **Recommendations:**
            1. Consider redistributing tasks from Developer 2
            2. Schedule risk mitigation meeting for vendor delays
            3. Prepare for Sprint 3 review and retrospective
            
            **Upcoming Deadlines:**
            - API Integration (Tom) - April 29
            - Database Migration (Sarah) - May 1
            - Security Review (External) - May 3
            """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Project assistant section
    st.markdown('<h2 class="module-header">Project Assistant</h2>', unsafe_allow_html=True)
    
    # User input for questions/tasks
    user_input = st.text_input("Ask a question or request an action:")
    
    if user_input:
        if st.button("Submit"):
            with st.spinner("Processing your request..."):
                # Placeholder for actual AI-generated responses
                if "risk" in user_input.lower() or "risks" in user_input.lower():
                    st.markdown("### Risk Analysis")
                    st.markdown("""
                    Based on current project data, there are 8 identified risks:
                    - 2 high severity risks
                    - 4 medium severity risks
                    - 2 low severity risks
                    
                    The most critical risk is related to vendor delays, which could impact the project timeline by up to 2 weeks.
                    """)
                    
                elif "schedule" in user_input.lower() or "timeline" in user_input.lower():
                    st.markdown("### Schedule Analysis")
                    st.markdown("""
                    The project is currently on track overall, with a 47.5% completion rate.
                    
                    However, there are 2 critical path tasks that are behind schedule:
                    1. API Integration (25% complete, should be at 50%)
                    2. Database Migration (10% complete, should be at 30%)
                    
                    If these delays continue, the project end date could slip by approximately 7 days.
                    """)
                    
                elif "resource" in user_input.lower() or "team" in user_input.lower():
                    st.markdown("### Resource Analysis")
                    st.markdown("""
                    Current resource allocation shows:
                    - 1 overallocated team member (Developer 2 at 125%)
                    - 2 optimally allocated team members
                    - 3 underutilized team members (below 70% allocation)
                    
                    Recommendation: Redistribute 2-3 tasks from Developer 2 to the underutilized resources.
                    """)
                    
                else:
                    st.markdown("I'll help you with that request. Based on the current project data, here are some insights that might be useful:")
                    st.markdown("""
                    - The project is 47.5% complete overall
                    - There are 2 critical path tasks that need attention
                    - 1 team member is currently overallocated
                    - 3 important deadlines are coming up this week
                    
                    Would you like more specific information about any of these areas?
                    """)
    
    # Sample additional features (placeholders)
    st.markdown('<h2 class="module-header">Assistant Capabilities</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("Task Management")
        st.write("The AI assistant can help you manage tasks:")
        st.markdown("- Create tasks based on natural language input")
        st.markdown("- Assign tasks to team members")
        st.markdown("- Set reminders for important deadlines")
        st.markdown("- Prioritize tasks based on project impact")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("Decision Support")
        st.write("The AI assistant can help with decision making:")
        st.markdown("- Analyze trade-offs between options")
        st.markdown("- Provide data-driven recommendations")
        st.markdown("- Document decision rationale")
        st.markdown("- Track decision outcomes")
        st.markdown('</div>', unsafe_allow_html=True)

def render_sidebar():
    """Render the enhanced sidebar with improved navigation."""
    st.sidebar.markdown('<h1 style="color:#4CAF50;">AI PM Buddy v2.0</h1>', unsafe_allow_html=True)
    
    # Add a professional project management icon
    st.sidebar.image("https://img.icons8.com/fluency/96/000000/project-management.png")
    
    # Notifications icon with counter
    unread_count = len([n for n in st.session_state.notifications if not n.get('read', False)])
    if unread_count > 0:
        st.sidebar.markdown(f'<div style="text-align:right;margin-bottom:10px;"><span style="background-color:#4CAF50;color:white;padding:2px 8px;border-radius:10px;">🔔 {unread_count}</span></div>', unsafe_allow_html=True)
    
    # OpenAI API Key Input
    with st.sidebar.expander("API Key Settings", expanded=False):
        api_key = st.text_input("OpenAI API Key", value=st.session_state.openai_api_key, type="password")
        if api_key != st.session_state.openai_api_key:
            st.session_state.openai_api_key = api_key
            st.success("API Key updated!")
    
    # Project selection or creation in a cleaner UI
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.sidebar.subheader("Project Management")
    
    project_option = st.sidebar.radio("Choose option:", ["Select Existing Project", "Create New Project"])
    
    if project_option == "Select Existing Project":
        if not st.session_state.project_data:
            st.sidebar.warning("No projects available. Please create a new project.")
            project_option = "Create New Project"
        else:
            projects = list(st.session_state.project_data.keys())
            selected_project = st.sidebar.selectbox("Select Project", projects)
            st.session_state.current_project = selected_project
    
    if project_option == "Create New Project":
        new_project_name = st.sidebar.text_input("New Project Name")
        if st.sidebar.button("Create Project"):
            if new_project_name:
                if new_project_name in st.session_state.project_data:
                    st.sidebar.error("Project already exists!")
                else:
                    # Initialize with sample data structure
                    st.session_state.project_data[new_project_name] = load_sample_data()
                    st.session_state.current_project = new_project_name
                    st.sidebar.success(f"Project '{new_project_name}' created!")
                    save_data(st.session_state.project_data)
                    st.rerun()
            else:
                st.sidebar.error("Please enter a project name")
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Modern navigation with sections
    if st.session_state.current_project:
        st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.sidebar.subheader("Navigation")
        
        # Main views
        main_views = {
            "dashboard": "📊 Dashboard",
            "ai_assistant": "🤖 AI Assistant"
        }
        
        selected_main_view = st.sidebar.radio("Main Views", list(main_views.keys()), 
                                            format_func=lambda x: main_views[x])
        
        if selected_main_view != st.session_state.current_view:
            st.session_state.current_view = selected_main_view
            st.rerun()
        st.sidebar.markdown('</div>', unsafe_allow_html=True)
        
        # Module Categories
        st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.sidebar.subheader("Modules")
        
        # Group modules into categories for better organization
        module_categories = {
            "Planning & Tracking": [
                "AI PM Insights", 
                "WBS Overview", 
                "Critical Path Slippage Warning",
                "Scope Creep Early Detection"
            ],
            "Resource Management": [
                "Resource Allocation Monitoring"
            ],
            "Risk & Compliance": [
                "RAID Compliance Checker"
            ],
            "Communication & Collaboration": [
                "Decision Log Assistant",
                "Team Sentiment Analyzer"
            ],
            "Knowledge Management": [
                "Agile Coach Bot",
                "PM Knowledge Assistant"
            ],
            # New v2.0 module categories
            "Documents & Reports": [
                "Document Generator",
                "Template Management"
            ],
            "Simulation & Analysis": [
                "Risk Simulator",
                "What-If Analysis"
            ],
            "Communication": [
                "Team Communication",
                "Notification Center"
            ],
            "Integrations": [
                "JIRA Connector",
                "MS Teams Integration"
                # "Outlook Calendar"
            ]
        }
        
        # Create expandable sections for each category
        selected_category = st.sidebar.selectbox("Module Categories", list(module_categories.keys()))
        
        modules_in_category = module_categories[selected_category]
        if modules_in_category:
            selected_module = st.sidebar.selectbox("Select Module", modules_in_category)
            
            if st.sidebar.button("Load Module"):
                st.session_state.current_view = "module"
                st.session_state.current_module = selected_module
                st.rerun()
        else:
            st.sidebar.info("Modules coming soon in this category!")
        
        st.sidebar.markdown('</div>', unsafe_allow_html=True)
        
        # Version information
        st.sidebar.markdown('<div style="text-align:center;margin-top:20px;font-size:0.8em;">AI PM Buddy v2.0<br/>©2025 PM Technologies Inc.</div>', unsafe_allow_html=True)

def main():
    """Main application function."""
    # Render the enhanced sidebar
    render_sidebar()
    
    if st.session_state.current_project:
        # Display the appropriate view
        if st.session_state.current_view == "dashboard":
            show_dashboard()
        elif st.session_state.current_view == "ai_assistant":
            show_ai_assistant()
        elif st.session_state.current_view == "module":
            # Display the selected module
            st.markdown(f'<h1 class="main-header">{st.session_state.current_module}</h1>', unsafe_allow_html=True)
            
            # Load the appropriate module
            if st.session_state.current_module == "AI PM Insights":
                show_ai_insights(st.session_state.project_data[st.session_state.current_project])
            elif st.session_state.current_module == "WBS Overview":
                show_wbs_overview(st.session_state.project_data[st.session_state.current_project])
            elif st.session_state.current_module == "Resource Allocation Monitoring":
                show_resource_allocation(st.session_state.project_data[st.session_state.current_project])
            elif st.session_state.current_module == "RAID Compliance Checker":
                show_raid_checker(st.session_state.project_data[st.session_state.current_project])
            elif st.session_state.current_module == "Decision Log Assistant":
                show_decision_log(st.session_state.project_data[st.session_state.current_project])
            elif st.session_state.current_module == "Team Sentiment Analyzer":
                show_sentiment_analyzer(st.session_state.project_data[st.session_state.current_project])
            elif st.session_state.current_module == "Agile Coach Bot":
                show_agile_coach()
            elif st.session_state.current_module == "PM Knowledge Assistant":
                show_pm_knowledge()
            elif st.session_state.current_module == "Critical Path Slippage Warning":
                show_critical_path(st.session_state.project_data[st.session_state.current_project])
            elif st.session_state.current_module == "Scope Creep Early Detection":
                show_scope_detection(st.session_state.project_data[st.session_state.current_project])
            # New v2.0 modules
            elif st.session_state.current_module == "Document Generator":
                show_document_generator(st.session_state.project_data[st.session_state.current_project])
            elif st.session_state.current_module == "Template Management":
                show_template_management(st.session_state.project_data[st.session_state.current_project])
            elif st.session_state.current_module == "Risk Simulator":
                show_risk_simulator(st.session_state.project_data[st.session_state.current_project])
            elif st.session_state.current_module == "What-If Analysis":
                show_what_if_analysis(st.session_state.project_data[st.session_state.current_project])
            # Communication modules
            elif st.session_state.current_module == "Team Communication":
                show_team_communication(st.session_state.project_data[st.session_state.current_project])
            elif st.session_state.current_module == "Notification Center":
                show_notification_center(st.session_state.project_data[st.session_state.current_project])
            # Integration modules
            elif st.session_state.current_module == "JIRA Connector":
                show_jira_connector(st.session_state.project_data[st.session_state.current_project])
            elif st.session_state.current_module == "MS Teams Integration":
                show_ms_teams_integration(st.session_state.project_data[st.session_state.current_project])
            # Future modules will be added here
            else:
                st.info(f"The module '{st.session_state.current_module}' is coming soon in AI PM Buddy v2.0!")
    else:
        # Welcome page
        st.markdown('<h1 class="main-header">Welcome to AI PM Buddy v2.0</h1>', unsafe_allow_html=True)
        
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.write("""
        AI PM Buddy is a comprehensive project management assistant powered by artificial intelligence. 
        It provides real-time insights, monitoring, and guidance to help project managers succeed.
        
        Please select or create a project from the sidebar to get started.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Features section with improved layout
        st.markdown('<h2 class="module-header">Key Features</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Core Features")
            st.markdown("""
            - ✅ AI-powered risk detection and monitoring
            - ✅ Visual WBS tracking and progress monitoring
            - ✅ Resource allocation optimization
            - ✅ Compliance checking for RAID logs
            - ✅ Decision tracking and management
            - ✅ Team sentiment analysis
            - ✅ AI-assisted knowledge base for Agile and PM practices
            - ✅ Critical path monitoring
            - ✅ Automatic scope creep detection
            """)
        
        with col2:
            st.markdown("### New in v2.0")
            st.markdown("""
            - 🆕 Personalized project dashboard
            - 🆕 AI Personal Assistant with daily briefings
            - 🆕 Document generation and management
            - 🆕 Risk simulation and what-if analysis
            - 🆕 Enhanced team communication features
            - 🆕 Project history for new team members
            - 🆕 Integration with JIRA, MS Teams, and Outlook
            - 🆕 Customizable notifications
            - 🆕 Improved UI with better visualization
            """)
        
        # Display a sample dashboard preview
        st.markdown('<h2 class="module-header">Preview</h2>', unsafe_allow_html=True)
        st.image("https://img.icons8.com/color/452/dashboard-layout.png", width=600)

if __name__ == "__main__":
    main()