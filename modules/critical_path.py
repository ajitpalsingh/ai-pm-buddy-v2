import streamlit as st
import pandas as pd
import numpy as np
import datetime
from utils.visualization import create_critical_path_network

def show_critical_path(project_data):
    """
    Display the Critical Path Slippage Warning module.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.subheader("Critical Path Slippage Warning")
    
    # Get WBS data
    wbs_data = project_data.get('wbs', [])
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Critical Path Analysis", "Task Progress Tracking"])
    
    with tab1:
        st.write("""
        The Critical Path Slippage Warning module monitors tasks on the critical path
        and provides early warning if key project tasks are delayed or at risk.
        """)
        
        if not wbs_data:
            st.info("No WBS data available. Please add tasks in the WBS Overview module.")
        else:
            # Create critical path network visualization
            critical_path_fig = create_critical_path_network(wbs_data)
            st.pyplot(critical_path_fig)
            
            # Calculate critical path metrics
            critical_tasks = [task for task in wbs_data if task.get('critical', False)]
            
            total_critical_tasks = len(critical_tasks)
            completed_critical_tasks = len([task for task in critical_tasks if task.get('progress', 0) >= 100])
            at_risk_critical_tasks = [task for task in critical_tasks if task.get('progress', 0) < 50 and 
                                     datetime.datetime.strptime(task.get('end_date', '2099-12-31'), "%Y-%m-%d") > datetime.datetime.now()]
            delayed_critical_tasks = [task for task in critical_tasks if 
                                     datetime.datetime.strptime(task.get('end_date', '2099-12-31'), "%Y-%m-%d") < datetime.datetime.now() and 
                                     task.get('progress', 0) < 100]
            
            # Display metrics in columns
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Critical Tasks", total_critical_tasks)
            
            with col2:
                st.metric("Completed", completed_critical_tasks, delta=f"{completed_critical_tasks}/{total_critical_tasks}")
            
            with col3:
                st.metric("At Risk (<50%)", len(at_risk_critical_tasks), delta=len(at_risk_critical_tasks), delta_color="inverse")
            
            with col4:
                st.metric("Delayed", len(delayed_critical_tasks), delta=len(delayed_critical_tasks), delta_color="inverse")
            
            # Show warnings for critical path issues
            if delayed_critical_tasks:
                st.error("⚠️ **Critical Path Alert**: Some critical tasks are delayed!")
                
                delayed_df = pd.DataFrame([
                    {
                        'Task': task.get('task', ''),
                        'End Date': task.get('end_date', ''),
                        'Progress': f"{task.get('progress', 0)}%",
                        'Assigned To': task.get('assigned_to', ''),
                        'Days Overdue': (datetime.datetime.now() - datetime.datetime.strptime(task.get('end_date', '2099-12-31'), "%Y-%m-%d")).days
                    }
                    for task in delayed_critical_tasks
                ])
                
                st.dataframe(delayed_df, use_container_width=True)
            
            if at_risk_critical_tasks:
                st.warning("⚠️ **Critical Path Warning**: Some critical tasks are at risk!")
                
                at_risk_df = pd.DataFrame([
                    {
                        'Task': task.get('task', ''),
                        'End Date': task.get('end_date', ''),
                        'Progress': f"{task.get('progress', 0)}%",
                        'Assigned To': task.get('assigned_to', ''),
                        'Days Remaining': (datetime.datetime.strptime(task.get('end_date', '2099-12-31'), "%Y-%m-%d") - datetime.datetime.now()).days
                    }
                    for task in at_risk_critical_tasks
                ])
                
                st.dataframe(at_risk_df, use_container_width=True)
            
            if not delayed_critical_tasks and not at_risk_critical_tasks and total_critical_tasks > 0:
                st.success("✅ Critical path is on track.")
    
    with tab2:
        st.write("Track the progress of all tasks on the critical path.")
        
        if not wbs_data:
            st.info("No WBS data available. Please add tasks in the WBS Overview module.")
        else:
            # Filter only critical path tasks
            critical_tasks = [task for task in wbs_data if task.get('critical', False)]
            
            if not critical_tasks:
                st.info("No tasks are marked as being on the critical path. Please update your WBS.")
            else:
                # Create a DataFrame for the critical tasks
                critical_df = pd.DataFrame([
                    {
                        'ID': task.get('id', ''),
                        'Task': task.get('task', ''),
                        'Start Date': task.get('start_date', ''),
                        'End Date': task.get('end_date', ''),
                        'Duration': task.get('duration', 0),
                        'Progress': task.get('progress', 0),
                        'Assigned To': task.get('assigned_to', ''),
                        'Status': get_task_status(task)
                    }
                    for task in critical_tasks
                ])
                
                # Sort by start date
                critical_df = critical_df.sort_values('Start Date')
                
                # Display the table
                st.dataframe(critical_df, use_container_width=True)
                
                # Allow quick progress updates
                st.subheader("Quick Progress Update")
                st.write("Update the progress of critical path tasks:")
                
                # Select a task to update
                task_ids = {f"{task.get('id')} - {task.get('task')}": task.get('id') for task in critical_tasks}
                selected_task_label = st.selectbox("Select a task", options=list(task_ids.keys()))
                selected_task_id = task_ids[selected_task_label]
                
                # Find the selected task
                task_to_update = next((task for task in wbs_data if task.get('id') == selected_task_id), None)
                
                if task_to_update:
                    # Show current progress
                    current_progress = task_to_update.get('progress', 0)
                    st.write(f"Current Progress: {current_progress}%")
                    
                    # Update progress
                    new_progress = st.slider("New Progress", 0, 100, int(current_progress))
                    
                    if st.button("Update Progress"):
                        # Update the task progress
                        for i, task in enumerate(project_data['wbs']):
                            if task.get('id') == selected_task_id:
                                project_data['wbs'][i]['progress'] = new_progress
                                break
                        
                        st.success(f"Progress updated to {new_progress}%")
                        st.rerun()

def get_task_status(task):
    """
    Determine the status of a task based on its dates and progress.
    
    Args:
        task: Task dictionary
        
    Returns:
        String representing the task status
    """
    progress = task.get('progress', 0)
    
    if progress >= 100:
        return "Completed"
    
    try:
        end_date = datetime.datetime.strptime(task.get('end_date', '2099-12-31'), "%Y-%m-%d")
        start_date = datetime.datetime.strptime(task.get('start_date', '2000-01-01'), "%Y-%m-%d")
        today = datetime.datetime.now()
        
        if today > end_date:
            return "Delayed"
        elif today < start_date:
            return "Not Started"
        else:
            # Calculate expected progress based on dates
            total_days = (end_date - start_date).days
            if total_days <= 0:
                return "In Progress"
            
            days_passed = (today - start_date).days
            expected_progress = (days_passed / total_days) * 100
            
            if progress < expected_progress - 10:  # 10% buffer
                return "Behind Schedule"
            elif progress > expected_progress + 10:  # 10% buffer
                return "Ahead of Schedule"
            else:
                return "On Track"
    except Exception as e:
        return "In Progress"
