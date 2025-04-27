import streamlit as st
import pandas as pd
import datetime
from utils.visualization import create_gantt_chart

def show_wbs_overview(project_data):
    """
    Display the Work Breakdown Structure (WBS) overview.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.subheader("Work Breakdown Structure (WBS) Overview")
    
    # Get WBS data
    wbs_data = project_data.get('wbs', [])
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Task List", "Gantt Chart", "Edit WBS"])
    
    with tab1:
        if not wbs_data:
            st.info("No WBS data available. Use the 'Edit WBS' tab to add tasks.")
        else:
            # Calculate overall progress
            total_duration = sum(task.get('duration', 0) for task in wbs_data)
            weighted_progress = sum((task.get('duration', 0) * task.get('progress', 0) / 100) for task in wbs_data)
            overall_progress = (weighted_progress / total_duration) * 100 if total_duration > 0 else 0
            
            # Display overall progress
            st.progress(overall_progress / 100)
            st.write(f"Overall Progress: {overall_progress:.1f}%")
            
            # Create a DataFrame for the tasks
            wbs_df = pd.DataFrame([
                {
                    'ID': task.get('id', ''),
                    'Task': task.get('task', ''),
                    'Description': task.get('description', ''),
                    'Start Date': task.get('start_date', ''),
                    'End Date': task.get('end_date', ''),
                    'Duration (days)': task.get('duration', 0),
                    'Progress (%)': task.get('progress', 0),
                    'Assigned To': task.get('assigned_to', ''),
                    'Dependencies': ', '.join(map(str, task.get('dependencies', []))),
                    'Critical': task.get('critical', False)
                }
                for task in wbs_data
            ])
            
            # Display the tasks table
            st.dataframe(wbs_df, use_container_width=True)
            
            # Display some stats and filters
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Tasks", len(wbs_data))
            
            with col2:
                critical_tasks = len([t for t in wbs_data if t.get('critical', False)])
                st.metric("Critical Path Tasks", critical_tasks)
            
            with col3:
                completed_tasks = len([t for t in wbs_data if t.get('progress', 0) >= 100])
                st.metric("Completed Tasks", f"{completed_tasks} / {len(wbs_data)}")
    
    with tab2:
        if not wbs_data:
            st.info("No WBS data available. Use the 'Edit WBS' tab to add tasks.")
        else:
            # Create Gantt chart
            gantt_fig = create_gantt_chart(wbs_data)
            st.plotly_chart(gantt_fig, use_container_width=True)
    
    with tab3:
        st.write("Add, edit, or remove tasks in the Work Breakdown Structure.")
        
        # Action selection
        action = st.radio("Select action:", ["Add New Task", "Edit Existing Task", "Update Progress", "Remove Task"])
        
        if action == "Add New Task":
            with st.form("add_task_form"):
                st.write("Add a new task to the WBS")
                
                # Generate a new task ID (max existing ID + 1)
                new_id = max([task.get('id', 0) for task in wbs_data], default=0) + 1
                
                # Task details
                task_name = st.text_input("Task Name")
                task_description = st.text_area("Description")
                
                col1, col2 = st.columns(2)
                with col1:
                    start_date = st.date_input("Start Date", value=datetime.datetime.now())
                with col2:
                    duration = st.number_input("Duration (days)", min_value=1, value=5)
                
                # Calculate end date
                end_date = start_date + datetime.timedelta(days=duration)
                st.write(f"End Date: {end_date.strftime('%Y-%m-%d')}")
                
                # Additional details
                assigned_to = st.text_input("Assigned To")
                
                # Get existing task IDs for dependencies selection
                existing_ids = [task.get('id') for task in wbs_data]
                dependencies = st.multiselect("Dependencies", options=existing_ids)
                
                critical = st.checkbox("On Critical Path")
                
                # Submit button
                submit_button = st.form_submit_button("Add Task")
                
                if submit_button:
                    if task_name:
                        # Create new task
                        new_task = {
                            'id': new_id,
                            'task': task_name,
                            'description': task_description,
                            'start_date': start_date.strftime("%Y-%m-%d"),
                            'end_date': end_date.strftime("%Y-%m-%d"),
                            'duration': duration,
                            'progress': 0,
                            'assigned_to': assigned_to,
                            'dependencies': dependencies,
                            'critical': critical
                        }
                        
                        # Add to WBS data
                        project_data['wbs'].append(new_task)
                        st.success(f"Task '{task_name}' added successfully!")
                        st.rerun()
                    else:
                        st.error("Task name is required!")
        
        elif action == "Edit Existing Task":
            if not wbs_data:
                st.info("No tasks available to edit.")
            else:
                # Select a task to edit
                task_ids = {f"{task.get('id')} - {task.get('task')}": task.get('id') for task in wbs_data}
                selected_task_label = st.selectbox("Select a task to edit", options=list(task_ids.keys()))
                selected_task_id = task_ids[selected_task_label]
                
                # Find the selected task
                task_to_edit = next((task for task in wbs_data if task.get('id') == selected_task_id), None)
                
                if task_to_edit:
                    with st.form("edit_task_form"):
                        st.write(f"Editing Task: {task_to_edit.get('task')}")
                        
                        # Task details
                        task_name = st.text_input("Task Name", value=task_to_edit.get('task', ''))
                        task_description = st.text_area("Description", value=task_to_edit.get('description', ''))
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            start_date = st.date_input("Start Date", value=datetime.datetime.strptime(task_to_edit.get('start_date', datetime.datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d"))
                        with col2:
                            duration = st.number_input("Duration (days)", min_value=1, value=task_to_edit.get('duration', 5))
                        
                        # Calculate end date
                        end_date = start_date + datetime.timedelta(days=duration)
                        st.write(f"End Date: {end_date.strftime('%Y-%m-%d')}")
                        
                        # Additional details
                        assigned_to = st.text_input("Assigned To", value=task_to_edit.get('assigned_to', ''))
                        
                        # Get existing task IDs for dependencies selection
                        existing_ids = [task.get('id') for task in wbs_data if task.get('id') != selected_task_id]
                        dependencies = st.multiselect("Dependencies", options=existing_ids, default=task_to_edit.get('dependencies', []))
                        
                        critical = st.checkbox("On Critical Path", value=task_to_edit.get('critical', False))
                        progress = st.slider("Progress (%)", min_value=0, max_value=100, value=task_to_edit.get('progress', 0))
                        
                        # Submit button
                        submit_button = st.form_submit_button("Update Task")
                        
                        if submit_button:
                            if task_name:
                                # Update task
                                for i, task in enumerate(project_data['wbs']):
                                    if task.get('id') == selected_task_id:
                                        project_data['wbs'][i] = {
                                            'id': selected_task_id,
                                            'task': task_name,
                                            'description': task_description,
                                            'start_date': start_date.strftime("%Y-%m-%d"),
                                            'end_date': end_date.strftime("%Y-%m-%d"),
                                            'duration': duration,
                                            'progress': progress,
                                            'assigned_to': assigned_to,
                                            'dependencies': dependencies,
                                            'critical': critical
                                        }
                                        break
                                
                                st.success(f"Task '{task_name}' updated successfully!")
                                st.rerun()
                            else:
                                st.error("Task name is required!")
        
        elif action == "Update Progress":
            if not wbs_data:
                st.info("No tasks available to update progress.")
            else:
                # Create a form for bulk progress update
                with st.form("update_progress_form"):
                    st.write("Update progress for multiple tasks")
                    
                    # Create a DataFrame for the tasks
                    progress_df = pd.DataFrame([
                        {
                            'ID': task.get('id', ''),
                            'Task': task.get('task', ''),
                            'Current Progress (%)': task.get('progress', 0)
                        }
                        for task in wbs_data
                    ])
                    
                    # Display the current progress
                    st.dataframe(progress_df, use_container_width=True)
                    
                    # Select a task to update
                    task_ids = {f"{task.get('id')} - {task.get('task')}": task.get('id') for task in wbs_data}
                    selected_task_label = st.selectbox("Select a task to update", options=list(task_ids.keys()))
                    selected_task_id = task_ids[selected_task_label]
                    
                    # Update progress
                    new_progress = st.slider("New Progress (%)", min_value=0, max_value=100, value=next((task.get('progress', 0) for task in wbs_data if task.get('id') == selected_task_id), 0))
                    
                    # Submit button
                    submit_button = st.form_submit_button("Update Progress")
                    
                    if submit_button:
                        # Update progress for the selected task
                        for i, task in enumerate(project_data['wbs']):
                            if task.get('id') == selected_task_id:
                                project_data['wbs'][i]['progress'] = new_progress
                                break
                        
                        st.success(f"Progress updated successfully!")
                        st.rerun()
        
        elif action == "Remove Task":
            if not wbs_data:
                st.info("No tasks available to remove.")
            else:
                # Select a task to remove
                task_ids = {f"{task.get('id')} - {task.get('task')}": task.get('id') for task in wbs_data}
                selected_task_label = st.selectbox("Select a task to remove", options=list(task_ids.keys()))
                selected_task_id = task_ids[selected_task_label]
                
                if st.button("Remove Task"):
                    # Check if task is dependency for other tasks
                    dependent_tasks = [task.get('task') for task in wbs_data if selected_task_id in task.get('dependencies', [])]
                    
                    if dependent_tasks:
                        st.error(f"Cannot remove this task as it is a dependency for: {', '.join(dependent_tasks)}")
                    else:
                        # Remove the task
                        project_data['wbs'] = [task for task in project_data['wbs'] if task.get('id') != selected_task_id]
                        st.success(f"Task removed successfully!")
                        st.rerun()
