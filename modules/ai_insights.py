import streamlit as st
import pandas as pd
import time
from utils.openai_utils import analyze_project_risks
from utils.visualization import create_gantt_chart, create_resource_allocation_chart, create_raid_compliance_chart

def show_ai_insights(project_data):
    """
    Display AI-powered insights about the project.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.subheader("AI Project Management Insights")
    
    # Check for OpenAI API key
    if not st.session_state.openai_api_key:
        st.warning("⚠️ Please provide your OpenAI API key in the sidebar settings to enable AI insights.")
        return
    
    # Create tabs for different insights
    tab1, tab2, tab3 = st.tabs(["Risk Analysis", "Schedule Health", "Resource Optimization"])
    
    with tab1:
        st.markdown("### AI Risk Analysis")
        st.write("Using AI to analyze project data and identify potential risks and issues.")
        
        # Add refresh button for risk analysis
        if st.button("Generate Risk Analysis", key="risk_analysis"):
            with st.spinner("AI is analyzing your project data..."):
                risks = analyze_project_risks(project_data)
                
                if risks:
                    # Display risks in a table
                    risk_data = pd.DataFrame(risks)
                    
                    # Apply color coding based on severity
                    def color_severity(val):
                        colors = {
                            'high': 'background-color: rgba(255, 0, 0, 0.2)',
                            'medium': 'background-color: rgba(255, 165, 0, 0.2)',
                            'low': 'background-color: rgba(0, 128, 0, 0.2)'
                        }
                        return colors.get(val.lower(), '')
                    
                    # Style the dataframe
                    styled_risks = risk_data.style.applymap(color_severity, subset=['severity'])
                    
                    # Display the styled dataframe
                    st.dataframe(styled_risks, use_container_width=True)
                    
                    # Display actionable insights
                    st.markdown("### Key Insights")
                    high_risks = [r for r in risks if r.get('severity', '').lower() == 'high']
                    
                    if high_risks:
                        st.warning(f"⚠️ {len(high_risks)} high severity risks identified that require immediate attention.")
                    
                    # Show recommendations for top risks
                    for i, risk in enumerate(risks[:3]):
                        with st.expander(f"Recommendation for {risk.get('risk_type', 'Risk')} - {risk.get('description', '')}"):
                            st.write(risk.get('recommendation', 'No recommendation available'))
                else:
                    st.info("No significant risks identified in the current project data.")
    
    with tab2:
        st.markdown("### Schedule Health Analysis")
        st.write("Analysis of project schedule, timeline, and critical path.")
        
        # Create Gantt chart for schedule visualization
        gantt_fig = create_gantt_chart(project_data.get('wbs', []))
        st.plotly_chart(gantt_fig, use_container_width=True)
        
        # Calculate overall project progress
        tasks = project_data.get('wbs', [])
        if tasks:
            total_duration = sum(task.get('duration', 0) for task in tasks)
            weighted_progress = sum((task.get('duration', 0) * task.get('progress', 0) / 100) for task in tasks)
            overall_progress = (weighted_progress / total_duration) * 100 if total_duration > 0 else 0
            
            # Create progress metric
            st.metric("Overall Project Progress", f"{overall_progress:.1f}%")
            
            # Check for tasks on critical path with low progress
            critical_tasks = [t for t in tasks if t.get('critical', False)]
            at_risk_tasks = [t for t in critical_tasks if t.get('progress', 0) < 50]
            
            if at_risk_tasks:
                st.warning(f"⚠️ {len(at_risk_tasks)} critical path tasks are less than 50% complete.")
                
                # Show at-risk tasks
                at_risk_df = pd.DataFrame([{
                    'Task': t.get('task', ''),
                    'Progress': f"{t.get('progress', 0)}%",
                    'Deadline': t.get('end_date', '')
                } for t in at_risk_tasks])
                
                st.dataframe(at_risk_df, use_container_width=True)
    
    with tab3:
        st.markdown("### Resource Optimization")
        st.write("Analysis of resource allocation and utilization.")
        
        # Create resource allocation chart
        resource_fig = create_resource_allocation_chart(project_data.get('resources', []))
        st.plotly_chart(resource_fig, use_container_width=True)
        
        # Identify overallocated resources
        resources = project_data.get('resources', [])
        overallocated = [r for r in resources if r.get('allocated', 0) > r.get('availability', 0)]
        underutilized = [r for r in resources if r.get('allocated', 0) < 0.7 * r.get('availability', 0)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            if overallocated:
                st.error(f"⚠️ {len(overallocated)} overallocated resources")
                
                # Show overallocated resources
                over_df = pd.DataFrame([{
                    'Resource': r.get('name', ''),
                    'Allocation': f"{(r.get('allocated', 0) / r.get('availability', 1) * 100):.0f}%",
                    'Over by': f"{r.get('allocated', 0) - r.get('availability', 0)} hours"
                } for r in overallocated])
                
                st.dataframe(over_df, use_container_width=True)
        
        with col2:
            if underutilized:
                st.info(f"ℹ️ {len(underutilized)} underutilized resources (<70%)")
                
                # Show underutilized resources
                under_df = pd.DataFrame([{
                    'Resource': r.get('name', ''),
                    'Allocation': f"{(r.get('allocated', 0) / r.get('availability', 1) * 100):.0f}%",
                    'Available': f"{r.get('availability', 0) - r.get('allocated', 0)} hours"
                } for r in underutilized])
                
                st.dataframe(under_df, use_container_width=True)
