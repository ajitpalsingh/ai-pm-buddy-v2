import streamlit as st
import pandas as pd
import numpy as np
import datetime
from utils.visualization import create_scope_creep_chart

def show_scope_detection(project_data):
    """
    Display the Scope Creep Early Detection module.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.subheader("Scope Creep Early Detection")
    
    # Get WBS data and baseline WBS data
    wbs_data = project_data.get('wbs', [])
    baseline_wbs = project_data.get('baseline_wbs', [])
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Scope Analysis", "Baseline Management"])
    
    with tab1:
        st.write("""
        The Scope Creep Early Detection module monitors changes in project scope
        by comparing the current Work Breakdown Structure (WBS) with the baseline WBS.
        It helps identify unauthorized growth in project scope.
        """)
        
        if not wbs_data or not baseline_wbs:
            st.info("No WBS data or baseline available. Please add tasks in the WBS Overview module and set a baseline.")
        else:
            # Create scope creep visualization
            scope_fig = create_scope_creep_chart(baseline_wbs, wbs_data)
            st.plotly_chart(scope_fig, use_container_width=True)
            
            # Calculate scope metrics
            baseline_task_count = len(baseline_wbs)
            current_task_count = len(wbs_data)
            
            baseline_effort = sum(task.get('duration', 0) for task in baseline_wbs)
            current_effort = sum(task.get('duration', 0) for task in wbs_data)
            
            task_change = current_task_count - baseline_task_count
            effort_change = current_effort - baseline_effort
            
            task_change_pct = (task_change / baseline_task_count) * 100 if baseline_task_count > 0 else 0
            effort_change_pct = (effort_change / baseline_effort) * 100 if baseline_effort > 0 else 0
            
            # Display metrics in columns
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Baseline Tasks", baseline_task_count)
            
            with col2:
                st.metric("Current Tasks", current_task_count, delta=task_change)
            
            with col3:
                st.metric("Baseline Effort (days)", baseline_effort)
            
            with col4:
                st.metric("Current Effort (days)", current_effort, delta=effort_change)
            
            # Identify new tasks
            new_task_ids = set(task.get('id') for task in wbs_data) - set(task.get('id') for task in baseline_wbs)
            new_tasks = [task for task in wbs_data if task.get('id') in new_task_ids]
            
            # Identify modified tasks
            modified_tasks = []
            for baseline_task in baseline_wbs:
                baseline_id = baseline_task.get('id')
                current_task = next((task for task in wbs_data if task.get('id') == baseline_id), None)
                
                if current_task and (
                    baseline_task.get('duration', 0) != current_task.get('duration', 0) or
                    baseline_task.get('description', '') != current_task.get('description', '') or
                    baseline_task.get('task', '') != current_task.get('task', '')
                ):
                    modified_tasks.append({
                        'id': baseline_id,
                        'task': current_task.get('task', ''),
                        'original_duration': baseline_task.get('duration', 0),
                        'current_duration': current_task.get('duration', 0),
                        'duration_change': current_task.get('duration', 0) - baseline_task.get('duration', 0)
                    })
            
            # Show scope creep analysis
            if task_change_pct > 10 or effort_change_pct > 20:  # Thresholds for significant scope creep
                st.error(f"⚠️ **Scope Creep Alert**: Project scope has increased significantly by {task_change_pct:.1f}% in tasks and {effort_change_pct:.1f}% in effort!")
            elif task_change_pct > 5 or effort_change_pct > 10:  # Thresholds for moderate scope creep
                st.warning(f"⚠️ **Scope Creep Warning**: Project scope has increased by {task_change_pct:.1f}% in tasks and {effort_change_pct:.1f}% in effort.")
            elif task_change_pct > 0 or effort_change_pct > 0:  # Any increase
                st.info(f"ℹ️ Project scope has changed by {task_change_pct:.1f}% in tasks and {effort_change_pct:.1f}% in effort.")
            else:
                st.success("✅ Project scope is on track with the baseline.")
            
            # Display new tasks
            if new_tasks:
                st.subheader(f"New Tasks Added ({len(new_tasks)})")
                
                new_tasks_df = pd.DataFrame([
                    {
                        'ID': task.get('id', ''),
                        'Task': task.get('task', ''),
                        'Description': task.get('description', ''),
                        'Duration': task.get('duration', 0),
                        'Assigned To': task.get('assigned_to', '')
                    }
                    for task in new_tasks
                ])
                
                st.dataframe(new_tasks_df, use_container_width=True)
            
            # Display modified tasks
            if modified_tasks:
                st.subheader(f"Modified Tasks ({len(modified_tasks)})")
                
                modified_tasks_df = pd.DataFrame([
                    {
                        'ID': task.get('id', ''),
                        'Task': task.get('task', ''),
                        'Original Duration': task.get('original_duration', 0),
                        'Current Duration': task.get('current_duration', 0),
                        'Change (days)': task.get('duration_change', 0)
                    }
                    for task in modified_tasks
                ])
                
                st.dataframe(modified_tasks_df, use_container_width=True)
    
    with tab2:
        st.write("Manage the baseline WBS for scope comparison.")
        
        # Display current baseline status
        if baseline_wbs:
            st.success(f"✅ Baseline established with {len(baseline_wbs)} tasks.")
            baseline_date = project_data.get('baseline_date', 'Unknown')
            st.write(f"Baseline Date: {baseline_date}")
        else:
            st.warning("⚠️ No baseline has been established. Set a baseline to enable scope creep detection.")
        
        # Baseline management options
        action = st.radio("Baseline Options:", ["Set New Baseline", "View Baseline", "Reset Baseline"])
        
        if action == "Set New Baseline":
            if not wbs_data:
                st.error("Cannot set baseline: No WBS tasks available. Please add tasks first.")
            else:
                st.write("Setting a new baseline will save the current WBS as the reference point for scope change detection.")
                
                if st.button("Set Baseline"):
                    # Create a deep copy of the current WBS
                    project_data['baseline_wbs'] = wbs_data.copy()
                    project_data['baseline_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
                    
                    st.success("Baseline set successfully!")
                    st.rerun()
        
        elif action == "View Baseline":
            if not baseline_wbs:
                st.info("No baseline available to view.")
            else:
                st.write("Current baseline WBS:")
                
                baseline_df = pd.DataFrame([
                    {
                        'ID': task.get('id', ''),
                        'Task': task.get('task', ''),
                        'Description': task.get('description', ''),
                        'Duration': task.get('duration', 0),
                        'Assigned To': task.get('assigned_to', '')
                    }
                    for task in baseline_wbs
                ])
                
                st.dataframe(baseline_df, use_container_width=True)
        
        elif action == "Reset Baseline":
            if not baseline_wbs:
                st.info("No baseline available to reset.")
            else:
                st.write("⚠️ Warning: Resetting the baseline will remove the current baseline and scope change detection will not be possible until a new baseline is set.")
                
                if st.button("Reset Baseline"):
                    # Clear the baseline
                    project_data['baseline_wbs'] = []
                    project_data['baseline_date'] = ""
                    
                    st.success("Baseline reset successfully!")
                    st.rerun()
