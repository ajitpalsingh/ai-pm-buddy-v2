import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import copy

def show_what_if_analysis(project_data):
    """
    Display the What-If Analysis module.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.subheader("What-If Scenario Analysis")
    st.write("Simulate changes to project parameters and analyze their impact on project outcomes.")
    
    # Create tabs for different scenario types
    tab1, tab2, tab3 = st.tabs(["Schedule Scenarios", "Resource Scenarios", "Budget Scenarios"])
    
    with tab1:
        show_schedule_scenarios(project_data)
    
    with tab2:
        show_resource_scenarios(project_data)
        
    with tab3:
        show_budget_scenarios(project_data)

def show_schedule_scenarios(project_data):
    """Display schedule scenario analysis."""
    st.markdown("### Schedule Scenario Analysis")
    st.write("Analyze the impact of schedule changes on project timeline and resource allocation.")
    
    # Get project tasks
    tasks = project_data.get('wbs', [])
    
    if not tasks:
        st.warning("No tasks found in the project. Please add tasks to the WBS first.")
        return
    
    # Display current schedule summary
    st.markdown("#### Current Schedule")
    
    # Find earliest start and latest end dates
    start_dates = [datetime.strptime(task.get('start_date', '2025-01-01'), '%Y-%m-%d') for task in tasks]
    end_dates = [datetime.strptime(task.get('end_date', '2025-01-01'), '%Y-%m-%d') for task in tasks]
    
    earliest_start = min(start_dates)
    latest_end = max(end_dates)
    total_duration = (latest_end - earliest_start).days
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Start Date", earliest_start.strftime('%Y-%m-%d'))
    with col2:
        st.metric("End Date", latest_end.strftime('%Y-%m-%d'))
    with col3:
        st.metric("Duration", f"{total_duration} days")
    
    # Create scenario options
    st.markdown("#### Create Scenario")
    
    col1, col2 = st.columns(2)
    
    with col1:
        scenario_type = st.radio(
            "Scenario Type",
            ["Adjust Task Durations", "Delay Project Start", "Accelerate Critical Path"]
        )
    
    with col2:
        if scenario_type == "Adjust Task Durations":
            adjustment_factor = st.slider(
                "Duration Adjustment Factor", 
                min_value=0.5, 
                max_value=2.0, 
                value=1.0, 
                step=0.1
            )
            apply_to = st.radio(
                "Apply to",
                ["All Tasks", "Critical Path Tasks", "Specific Task"]
            )
            
            if apply_to == "Specific Task":
                task_options = [task.get('task', f"Task {i+1}") for i, task in enumerate(tasks)]
                selected_task = st.selectbox("Select Task", task_options)
                
        elif scenario_type == "Delay Project Start":
            delay_days = st.number_input(
                "Delay in Days",
                min_value=1,
                max_value=100,
                value=14
            )
            
        elif scenario_type == "Accelerate Critical Path":
            acceleration_factor = st.slider(
                "Acceleration Factor", 
                min_value=0.5, 
                max_value=1.0, 
                value=0.8, 
                step=0.05
            )
            cost_increase = st.slider(
                "Cost Increase (%)", 
                min_value=0, 
                max_value=100, 
                value=20, 
                step=5
            )
    
    # Run scenario analysis button
    if st.button("Run Scenario Analysis"):
        with st.spinner("Running scenario analysis..."):
            # Create a copy of the project data for the scenario
            scenario_data = copy.deepcopy(project_data)
            scenario_tasks = scenario_data.get('wbs', [])
            
            # Apply scenario changes
            if scenario_type == "Adjust Task Durations":
                if apply_to == "All Tasks":
                    for task in scenario_tasks:
                        task['duration'] = int(task.get('duration', 0) * adjustment_factor)
                        
                elif apply_to == "Critical Path Tasks":
                    for task in scenario_tasks:
                        if task.get('critical', False):
                            task['duration'] = int(task.get('duration', 0) * adjustment_factor)
                            
                elif apply_to == "Specific Task":
                    for task in scenario_tasks:
                        if task.get('task', '') == selected_task:
                            task['duration'] = int(task.get('duration', 0) * adjustment_factor)
                
                scenario_name = f"Duration {'Increase' if adjustment_factor > 1 else 'Decrease'} - {abs(1-adjustment_factor)*100:.0f}%"
                
            elif scenario_type == "Delay Project Start":
                # Shift all start and end dates
                for task in scenario_tasks:
                    start_date = datetime.strptime(task.get('start_date', '2025-01-01'), '%Y-%m-%d')
                    end_date = datetime.strptime(task.get('end_date', '2025-01-01'), '%Y-%m-%d')
                    
                    new_start = start_date + timedelta(days=delay_days)
                    new_end = end_date + timedelta(days=delay_days)
                    
                    task['start_date'] = new_start.strftime('%Y-%m-%d')
                    task['end_date'] = new_end.strftime('%Y-%m-%d')
                
                scenario_name = f"Project Delay - {delay_days} days"
                
            elif scenario_type == "Accelerate Critical Path":
                # Accelerate critical path tasks and adjust costs
                critical_task_count = 0
                for task in scenario_tasks:
                    if task.get('critical', False):
                        critical_task_count += 1
                        original_duration = task.get('duration', 0)
                        task['duration'] = int(original_duration * acceleration_factor)
                        
                        # Adjust resource allocation
                        resources = scenario_data.get('resources', [])
                        task_owner = task.get('owner', '')
                        
                        for resource in resources:
                            if resource.get('name', '') == task_owner:
                                # Increase allocated hours due to acceleration
                                resource['allocated'] = resource.get('allocated', 0) * (1 + cost_increase/100)
                
                scenario_name = f"Acceleration - {(1-acceleration_factor)*100:.0f}% faster"
            
            # Recalculate scenario schedule
            recalculate_scenario_schedule(scenario_tasks)
            
            # Find scenario start and end dates
            scenario_start_dates = [datetime.strptime(task.get('start_date', '2025-01-01'), '%Y-%m-%d') for task in scenario_tasks]
            scenario_end_dates = [datetime.strptime(task.get('end_date', '2025-01-01'), '%Y-%m-%d') for task in scenario_tasks]
            
            scenario_earliest_start = min(scenario_start_dates)
            scenario_latest_end = max(scenario_end_dates)
            scenario_total_duration = (scenario_latest_end - scenario_earliest_start).days
            
            # Display scenario results
            st.markdown(f"#### Scenario Results: {scenario_name}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "New Start Date", 
                    scenario_earliest_start.strftime('%Y-%m-%d'),
                    delta_color="inverse",
                    delta=(scenario_earliest_start - earliest_start).days
                )
            with col2:
                st.metric(
                    "New End Date", 
                    scenario_latest_end.strftime('%Y-%m-%d'),
                    delta_color="inverse",
                    delta=(scenario_latest_end - latest_end).days
                )
            with col3:
                duration_change = scenario_total_duration - total_duration
                st.metric(
                    "New Duration", 
                    f"{scenario_total_duration} days",
                    delta=duration_change,
                    delta_color="inverse"
                )
            
            # Create comparative Gantt chart
            st.markdown("#### Schedule Comparison")
            
            # Prepare data for Gantt chart
            gantt_data = []
            
            # Add original tasks
            for i, task in enumerate(tasks):
                task_name = task.get('task', f"Task {i+1}")
                start_date = datetime.strptime(task.get('start_date', '2025-01-01'), '%Y-%m-%d')
                end_date = datetime.strptime(task.get('end_date', '2025-01-01'), '%Y-%m-%d')
                
                gantt_data.append({
                    'Task': task_name,
                    'Start': start_date,
                    'Finish': end_date,
                    'Version': 'Original'
                })
            
            # Add scenario tasks
            for i, task in enumerate(scenario_tasks):
                task_name = task.get('task', f"Task {i+1}")
                start_date = datetime.strptime(task.get('start_date', '2025-01-01'), '%Y-%m-%d')
                end_date = datetime.strptime(task.get('end_date', '2025-01-01'), '%Y-%m-%d')
                
                gantt_data.append({
                    'Task': task_name,
                    'Start': start_date,
                    'Finish': end_date,
                    'Version': 'Scenario'
                })
            
            # Create Gantt chart
            gantt_df = pd.DataFrame(gantt_data)
            
            fig = px.timeline(
                gantt_df, 
                x_start="Start", 
                x_end="Finish", 
                y="Task",
                color="Version",
                color_discrete_map={"Original": "#B0C4DE", "Scenario": "#4CAF50"}
            )
            
            fig.update_layout(
                title='Original vs Scenario Schedule',
                xaxis_title='Date',
                yaxis_title='Task',
                legend_title='Version'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Impact analysis
            st.markdown("#### Impact Analysis")
            
            # Resource impact if applicable
            if scenario_type == "Accelerate Critical Path":
                st.markdown("##### Resource Impact")
                
                # Calculate resource changes
                resource_changes = []
                
                for resource in scenario_data.get('resources', []):
                    original_resource = next((r for r in project_data.get('resources', []) if r.get('name', '') == resource.get('name', '')), None)
                    
                    if original_resource:
                        original_allocation = original_resource.get('allocated', 0)
                        scenario_allocation = resource.get('allocated', 0)
                        
                        if original_allocation != scenario_allocation:
                            resource_changes.append({
                                'Resource': resource.get('name', ''),
                                'Original Allocation': original_allocation,
                                'Scenario Allocation': scenario_allocation,
                                'Change': scenario_allocation - original_allocation,
                                'Change %': (scenario_allocation - original_allocation) / original_allocation * 100 if original_allocation > 0 else 0
                            })
                
                if resource_changes:
                    resource_df = pd.DataFrame(resource_changes)
                    st.dataframe(resource_df, use_container_width=True)
                    
                    # Resource allocation chart
                    fig = go.Figure()
                    
                    for change in resource_changes:
                        fig.add_trace(go.Bar(
                            x=[change['Resource']],
                            y=[change['Original Allocation']],
                            name='Original',
                            marker_color='#B0C4DE'
                        ))
                        fig.add_trace(go.Bar(
                            x=[change['Resource']],
                            y=[change['Scenario Allocation']],
                            name='Scenario',
                            marker_color='#4CAF50'
                        ))
                    
                    fig.update_layout(
                        title='Resource Allocation Comparison',
                        xaxis_title='Resource',
                        yaxis_title='Allocation (hours)',
                        barmode='group'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            
            # Schedule impact
            st.markdown("##### Critical Path Impact")
            
            # Count tasks on critical path
            original_critical = len([t for t in tasks if t.get('critical', False)])
            scenario_critical = len([t for t in scenario_tasks if t.get('critical', False)])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Original Critical Tasks", original_critical)
            with col2:
                st.metric("Scenario Critical Tasks", scenario_critical, delta=scenario_critical-original_critical)
            
            # Calculate slack changes
            st.markdown("##### Task Slack Changes")
            
            slack_changes = []
            
            for i, task in enumerate(tasks):
                task_name = task.get('task', f"Task {i+1}")
                original_duration = task.get('duration', 0)
                original_slack = task.get('slack', 0)
                
                scenario_task = scenario_tasks[i]
                scenario_duration = scenario_task.get('duration', 0)
                scenario_slack = scenario_task.get('slack', 0)
                
                if original_slack != scenario_slack:
                    slack_changes.append({
                        'Task': task_name,
                        'Original Duration': original_duration,
                        'Scenario Duration': scenario_duration,
                        'Original Slack': original_slack,
                        'Scenario Slack': scenario_slack,
                        'Slack Change': scenario_slack - original_slack
                    })
            
            if slack_changes:
                slack_df = pd.DataFrame(slack_changes)
                st.dataframe(slack_df, use_container_width=True)
            else:
                st.info("No significant slack changes identified.")
            
            # Risk assessment
            st.markdown("##### Risk Assessment")
            
            if scenario_type == "Adjust Task Durations" and adjustment_factor < 1:
                st.warning("⚠️ Reducing task durations increases the risk of schedule overruns.")
                st.markdown("**Recommendations:**")
                st.markdown("- Ensure resources are available to support accelerated schedule")
                st.markdown("- Implement more rigorous monitoring of critical path tasks")
                st.markdown("- Consider adding budget contingency for potential overtime costs")
                
            elif scenario_type == "Delay Project Start":
                st.warning("⚠️ Project delay may impact resource availability and stakeholder satisfaction.")
                st.markdown("**Recommendations:**")
                st.markdown("- Communicate schedule changes to all stakeholders")
                st.markdown("- Reconfirm resource availability for new dates")
                st.markdown("- Update dependent project schedules and milestones")
                
            elif scenario_type == "Accelerate Critical Path":
                st.warning("⚠️ Accelerating the schedule may impact quality and increase costs.")
                st.markdown("**Recommendations:**")
                st.markdown("- Implement additional quality control measures")
                st.markdown("- Monitor budget carefully for cost overruns")
                st.markdown("- Ensure resources have capacity to handle increased workload")
            
            # Save scenario
            if 'schedule_scenarios' not in st.session_state:
                st.session_state.schedule_scenarios = {}
                
            # Save scenario data
            scenario_id = f"scenario_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            st.session_state.schedule_scenarios[scenario_id] = {
                'name': scenario_name,
                'type': scenario_type,
                'original_start': earliest_start.strftime('%Y-%m-%d'),
                'original_end': latest_end.strftime('%Y-%m-%d'),
                'original_duration': total_duration,
                'scenario_start': scenario_earliest_start.strftime('%Y-%m-%d'),
                'scenario_end': scenario_latest_end.strftime('%Y-%m-%d'),
                'scenario_duration': scenario_total_duration,
                'tasks': scenario_tasks
            }
            
            st.success(f"Scenario '{scenario_name}' saved!")
    
    # Previous scenarios
    st.markdown("---")
    st.markdown("#### Previous Scenarios")
    
    if 'schedule_scenarios' in st.session_state and st.session_state.schedule_scenarios:
        scenario_options = [f"{data['name']} ({data['scenario_start']} to {data['scenario_end']})" 
                           for sid, data in st.session_state.schedule_scenarios.items()]
        
        selected_scenario = st.selectbox("Select Scenario", scenario_options)
        
        if selected_scenario:
            scenario_index = scenario_options.index(selected_scenario)
            scenario_id = list(st.session_state.schedule_scenarios.keys())[scenario_index]
            scenario = st.session_state.schedule_scenarios[scenario_id]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Start Date", scenario['scenario_start'])
            with col2:
                st.metric("End Date", scenario['scenario_end'])
            with col3:
                st.metric("Duration", f"{scenario['scenario_duration']} days")
            
            # Option to delete scenario
            if st.button(f"Delete Scenario: {scenario['name']}"):
                del st.session_state.schedule_scenarios[scenario_id]
                st.success(f"Scenario deleted!")
                st.rerun()
    else:
        st.info("No saved scenarios yet. Run a scenario analysis to see results here.")

def show_resource_scenarios(project_data):
    """Display resource scenario analysis."""
    st.markdown("### Resource Scenario Analysis")
    st.write("Analyze the impact of resource changes on project schedule and budget.")
    
    # Get project resources
    resources = project_data.get('resources', [])
    
    if not resources:
        st.warning("No resources found in the project. Please add resources first.")
        return
    
    # Display current resource allocation
    st.markdown("#### Current Resource Allocation")
    
    # Create resource allocation table
    resource_df = pd.DataFrame([{
        'Resource': r.get('name', ''),
        'Role': r.get('role', ''),
        'Allocated': r.get('allocated', 0),
        'Availability': r.get('availability', 0),
        'Utilization': f"{r.get('allocated', 0) / r.get('availability', 1) * 100:.0f}%" if r.get('availability', 0) > 0 else "N/A"
    } for r in resources])
    
    st.dataframe(resource_df, use_container_width=True)
    
    # Calculate overall statistics
    total_allocated = sum(r.get('allocated', 0) for r in resources)
    total_available = sum(r.get('availability', 0) for r in resources)
    overall_utilization = total_allocated / total_available * 100 if total_available > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Allocated", f"{total_allocated} hours")
    with col2:
        st.metric("Total Availability", f"{total_available} hours")
    with col3:
        st.metric("Overall Utilization", f"{overall_utilization:.1f}%")
    
    # Create scenario options
    st.markdown("#### Create Scenario")
    
    col1, col2 = st.columns(2)
    
    with col1:
        scenario_type = st.radio(
            "Scenario Type",
            ["Add/Remove Resources", "Change Resource Availability", "Redistribute Workload"]
        )
    
    with col2:
        if scenario_type == "Add/Remove Resources":
            action = st.radio("Action", ["Add Resources", "Remove Resources"])
            
            if action == "Add Resources":
                num_resources = st.number_input(
                    "Number of Resources to Add",
                    min_value=1,
                    max_value=10,
                    value=1
                )
                resource_role = st.selectbox(
                    "Resource Role",
                    ["Developer", "Designer", "Tester", "Business Analyst", "Project Manager"]
                )
                availability = st.number_input(
                    "Availability (hours)",
                    min_value=1,
                    max_value=160,
                    value=80
                )
                
            else:  # Remove Resources
                resource_options = [r.get('name', '') for r in resources]
                resources_to_remove = st.multiselect(
                    "Select Resources to Remove",
                    resource_options
                )
                
        elif scenario_type == "Change Resource Availability":
            resource_options = [r.get('name', '') for r in resources]
            selected_resource = st.selectbox(
                "Select Resource",
                resource_options
            )
            
            selected_resource_data = next((r for r in resources if r.get('name', '') == selected_resource), None)
            if selected_resource_data:
                current_availability = selected_resource_data.get('availability', 0)
                new_availability = st.number_input(
                    "New Availability (hours)",
                    min_value=1,
                    max_value=160,
                    value=current_availability
                )
                
        elif scenario_type == "Redistribute Workload":
            redistribution_strategy = st.selectbox(
                "Redistribution Strategy",
                ["Balance Workload", "Optimize for Schedule", "Minimize Overallocation"]
            )
            
            allow_overallocation = st.checkbox("Allow Temporary Overallocation", value=False)
            max_overallocation = st.slider(
                "Maximum Overallocation (%)",
                min_value=100,
                max_value=150,
                value=120,
                step=5,
                disabled=not allow_overallocation
            )
    
    # Run scenario analysis button
    if st.button("Run Resource Scenario Analysis"):
        with st.spinner("Running resource scenario analysis..."):
            # Create a copy of the project data for the scenario
            scenario_data = copy.deepcopy(project_data)
            scenario_resources = scenario_data.get('resources', [])
            
            # Apply scenario changes
            if scenario_type == "Add/Remove Resources":
                if action == "Add Resources":
                    # Generate new resource names
                    existing_names = [r.get('name', '') for r in resources]
                    
                    for i in range(num_resources):
                        # Generate a unique name
                        new_name = f"New {resource_role} {i+1}"
                        counter = 1
                        while new_name in existing_names:
                            new_name = f"New {resource_role} {i+1} ({counter})"
                            counter += 1
                        
                        # Add new resource
                        scenario_resources.append({
                            'name': new_name,
                            'role': resource_role,
                            'allocated': 0,  # Start with no allocation
                            'availability': availability
                        })
                        existing_names.append(new_name)
                    
                    scenario_name = f"Added {num_resources} {resource_role}(s)"
                    
                else:  # Remove Resources
                    if not resources_to_remove:
                        st.error("Please select at least one resource to remove.")
                        return
                    
                    # Remove selected resources
                    scenario_resources = [r for r in scenario_resources if r.get('name', '') not in resources_to_remove]
                    
                    # Need to reassign tasks from removed resources
                    available_resources = [r.get('name', '') for r in scenario_resources]
                    
                    if not available_resources:
                        st.error("Cannot remove all resources. Keep at least one resource.")
                        return
                    
                    # Reassign tasks from removed resources
                    tasks = scenario_data.get('wbs', [])
                    for task in tasks:
                        if task.get('owner', '') in resources_to_remove:
                            # Assign to first available resource
                            task['owner'] = available_resources[0]
                    
                    scenario_name = f"Removed {len(resources_to_remove)} Resource(s)"
                
            elif scenario_type == "Change Resource Availability":
                # Update selected resource availability
                for resource in scenario_resources:
                    if resource.get('name', '') == selected_resource:
                        old_availability = resource.get('availability', 0)
                        resource['availability'] = new_availability
                        
                        # Update scenario name based on change
                        if new_availability > old_availability:
                            scenario_name = f"Increased {selected_resource} Availability (+{new_availability - old_availability}h)"
                        else:
                            scenario_name = f"Decreased {selected_resource} Availability (-{old_availability - new_availability}h)"
                
            elif scenario_type == "Redistribute Workload":
                # Implement workload redistribution based on strategy
                if redistribution_strategy == "Balance Workload":
                    # Balance workload across resources of the same role
                    roles = set(r.get('role', '') for r in scenario_resources)
                    
                    for role in roles:
                        role_resources = [r for r in scenario_resources if r.get('role', '') == role]
                        
                        if len(role_resources) <= 1:
                            continue  # Can't balance with only one resource
                        
                        # Calculate total allocation and availability for this role
                        total_role_allocation = sum(r.get('allocated', 0) for r in role_resources)
                        total_role_availability = sum(r.get('availability', 0) for r in role_resources)
                        
                        # Skip if no allocation or availability
                        if total_role_allocation == 0 or total_role_availability == 0:
                            continue
                        
                        # Calculate target utilization
                        target_utilization = total_role_allocation / total_role_availability
                        
                        # Adjust allocations to meet target utilization
                        for resource in role_resources:
                            resource['allocated'] = target_utilization * resource.get('availability', 0)
                    
                    scenario_name = "Balanced Workload"
                    
                elif redistribution_strategy == "Optimize for Schedule":
                    # Allocate more work to resources with higher availability
                    # For this simulation, we'll just redistribute based on availability
                    total_allocation = sum(r.get('allocated', 0) for r in scenario_resources)
                    total_availability = sum(r.get('availability', 0) for r in scenario_resources)
                    
                    if total_allocation == 0 or total_availability == 0:
                        st.error("Cannot redistribute with zero allocation or availability.")
                        return
                    
                    # Calculate max allowed allocation per resource
                    max_allowed = max_overallocation / 100 if allow_overallocation else 1.0
                    
                    # Redistribute based on availability proportion
                    remaining_allocation = total_allocation
                    
                    for resource in sorted(scenario_resources, key=lambda r: r.get('availability', 0), reverse=True):
                        availability = resource.get('availability', 0)
                        
                        # Calculate proportional allocation
                        if availability > 0:
                            proportion = availability / total_availability
                            allocation = min(remaining_allocation, availability * max_allowed)
                            resource['allocated'] = allocation
                            remaining_allocation -= allocation
                        
                        if remaining_allocation <= 0:
                            break
                    
                    scenario_name = "Schedule Optimized"
                    
                elif redistribution_strategy == "Minimize Overallocation":
                    # Identify overallocated resources
                    overallocated = [r for r in scenario_resources if r.get('allocated', 0) > r.get('availability', 0)]
                    underallocated = [r for r in scenario_resources if r.get('allocated', 0) < r.get('availability', 0)]
                    
                    if not overallocated:
                        st.info("No overallocated resources to fix.")
                        scenario_name = "No Changes (No Overallocation)"
                    else:
                        # For each overallocated resource, move excess work to underallocated resources
                        for resource in overallocated:
                            excess = resource.get('allocated', 0) - resource.get('availability', 0)
                            resource['allocated'] = resource.get('availability', 0)
                            
                            # Distribute excess to underallocated resources
                            if underallocated and excess > 0:
                                # Sort by available capacity
                                underallocated.sort(key=lambda r: r.get('availability', 0) - r.get('allocated', 0), reverse=True)
                                
                                for under_resource in underallocated:
                                    available_capacity = under_resource.get('availability', 0) - under_resource.get('allocated', 0)
                                    
                                    if available_capacity > 0:
                                        transfer = min(excess, available_capacity)
                                        under_resource['allocated'] += transfer
                                        excess -= transfer
                                        
                                        if excess <= 0:
                                            break
                        
                        scenario_name = "Minimized Overallocation"
            
            # Recalculate resource utilization
            for resource in scenario_resources:
                if resource.get('availability', 0) > 0:
                    resource['utilization'] = resource.get('allocated', 0) / resource.get('availability', 0) * 100
                else:
                    resource['utilization'] = 0
            
            # Calculate scenario statistics
            scenario_total_allocated = sum(r.get('allocated', 0) for r in scenario_resources)
            scenario_total_available = sum(r.get('availability', 0) for r in scenario_resources)
            scenario_overall_utilization = scenario_total_allocated / scenario_total_available * 100 if scenario_total_available > 0 else 0
            
            # Display scenario results
            st.markdown(f"#### Scenario Results: {scenario_name}")
            
            # Create resource allocation table for scenario
            scenario_resource_df = pd.DataFrame([{
                'Resource': r.get('name', ''),
                'Role': r.get('role', ''),
                'Allocated': r.get('allocated', 0),
                'Availability': r.get('availability', 0),
                'Utilization': f"{r.get('allocated', 0) / r.get('availability', 1) * 100:.0f}%" if r.get('availability', 0) > 0 else "N/A"
            } for r in scenario_resources])
            
            st.dataframe(scenario_resource_df, use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "Total Allocated", 
                    f"{scenario_total_allocated} hours",
                    delta=round(scenario_total_allocated - total_allocated, 1)
                )
            with col2:
                st.metric(
                    "Total Availability", 
                    f"{scenario_total_available} hours",
                    delta=round(scenario_total_available - total_available, 1)
                )
            with col3:
                st.metric(
                    "Overall Utilization", 
                    f"{scenario_overall_utilization:.1f}%",
                    delta=round(scenario_overall_utilization - overall_utilization, 1)
                )
            
            # Resource utilization comparison
            st.markdown("#### Resource Utilization Comparison")
            
            # Prepare data for comparison chart
            comparison_data = []
            
            for original_resource in resources:
                resource_name = original_resource.get('name', '')
                original_allocated = original_resource.get('allocated', 0)
                original_availability = original_resource.get('availability', 0)
                original_utilization = original_allocated / original_availability * 100 if original_availability > 0 else 0
                
                # Find corresponding resource in scenario
                scenario_resource = next((r for r in scenario_resources if r.get('name', '') == resource_name), None)
                
                if scenario_resource:
                    scenario_allocated = scenario_resource.get('allocated', 0)
                    scenario_availability = scenario_resource.get('availability', 0)
                    scenario_utilization = scenario_allocated / scenario_availability * 100 if scenario_availability > 0 else 0
                    
                    comparison_data.append({
                        'Resource': resource_name,
                        'Original Utilization': original_utilization,
                        'Scenario Utilization': scenario_utilization
                    })
            
            # Add new resources from scenario that weren't in original
            for scenario_resource in scenario_resources:
                resource_name = scenario_resource.get('name', '')
                
                if not any(r.get('name', '') == resource_name for r in resources):
                    scenario_allocated = scenario_resource.get('allocated', 0)
                    scenario_availability = scenario_resource.get('availability', 0)
                    scenario_utilization = scenario_allocated / scenario_availability * 100 if scenario_availability > 0 else 0
                    
                    comparison_data.append({
                        'Resource': resource_name,
                        'Original Utilization': 0,  # New resource, so 0 in original
                        'Scenario Utilization': scenario_utilization
                    })
            
            # Create comparison chart
            if comparison_data:
                comparison_df = pd.DataFrame(comparison_data)
                
                fig = go.Figure()
                
                # Add bars for original utilization
                fig.add_trace(go.Bar(
                    x=comparison_df['Resource'],
                    y=comparison_df['Original Utilization'],
                    name='Original',
                    marker_color='#B0C4DE'
                ))
                
                # Add bars for scenario utilization
                fig.add_trace(go.Bar(
                    x=comparison_df['Resource'],
                    y=comparison_df['Scenario Utilization'],
                    name='Scenario',
                    marker_color='#4CAF50'
                ))
                
                # Add 100% utilization line
                fig.add_shape(
                    type="line",
                    x0=-0.5,
                    y0=100,
                    x1=len(comparison_df) - 0.5,
                    y1=100,
                    line=dict(color="red", width=2, dash="dash")
                )
                
                fig.update_layout(
                    title='Resource Utilization Comparison',
                    xaxis_title='Resource',
                    yaxis_title='Utilization (%)',
                    barmode='group',
                    yaxis=dict(range=[0, max(max(comparison_df['Original Utilization']), max(comparison_df['Scenario Utilization'])) * 1.1])
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Impact analysis
            st.markdown("#### Impact Analysis")
            
            # Calculate overallocation
            original_overallocated = [r for r in resources if r.get('allocated', 0) > r.get('availability', 0)]
            scenario_overallocated = [r for r in scenario_resources if r.get('allocated', 0) > r.get('availability', 0)]
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "Overallocated Resources (Original)",
                    len(original_overallocated)
                )
            with col2:
                st.metric(
                    "Overallocated Resources (Scenario)",
                    len(scenario_overallocated),
                    delta=-len(original_overallocated) + len(scenario_overallocated)
                )
            
            # Risk assessment
            st.markdown("##### Risk Assessment")
            
            if scenario_type == "Add/Remove Resources" and action == "Add Resources":
                st.success("✅ Adding resources can reduce schedule pressure but may require onboarding time.")
                st.markdown("**Recommendations:**")
                st.markdown("- Allow time for new resources to ramp up (productivity may be lower initially)")
                st.markdown("- Ensure proper knowledge transfer to new team members")
                st.markdown("- Adjust team communication plans to accommodate larger team")
                
            elif scenario_type == "Add/Remove Resources" and action == "Remove Resources":
                st.warning("⚠️ Removing resources may impact schedule and increase workload on remaining team members.")
                st.markdown("**Recommendations:**")
                st.markdown("- Ensure proper knowledge transfer before resources leave")
                st.markdown("- Reassess critical path activities and timeline")
                st.markdown("- Identify tasks that may need to be reprioritized or delayed")
                
            elif scenario_type == "Change Resource Availability":
                if new_availability > selected_resource_data.get('availability', 0):
                    st.success("✅ Increased availability can help accelerate the schedule.")
                    st.markdown("**Recommendations:**")
                    st.markdown("- Prioritize critical path activities for the additional hours")
                    st.markdown("- Review resource assignments to optimize allocation")
                else:
                    st.warning("⚠️ Decreased availability may impact the schedule.")
                    st.markdown("**Recommendations:**")
                    st.markdown("- Reassess task assignments to accommodate reduced availability")
                    st.markdown("- Identify tasks that may need to be reassigned or delayed")
                    st.markdown("- Update project timeline to reflect resource constraints")
                
            elif scenario_type == "Redistribute Workload":
                if scenario_overall_utilization > 90:
                    st.warning("⚠️ Overall resource utilization is high (>90%). This may leave limited buffer for unexpected issues.")
                    st.markdown("**Recommendations:**")
                    st.markdown("- Consider adding resources or extending timeline")
                    st.markdown("- Implement more rigorous progress tracking")
                    st.markdown("- Identify non-critical tasks that could be delayed if needed")
                else:
                    st.success("✅ Resource utilization is balanced and at a sustainable level.")
                    st.markdown("**Recommendations:**")
                    st.markdown("- Continue monitoring resource allocation throughout the project")
                    st.markdown("- Reassess as new tasks or requirements are added")
            
            # Save scenario
            if 'resource_scenarios' not in st.session_state:
                st.session_state.resource_scenarios = {}
                
            # Save scenario data
            scenario_id = f"scenario_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            st.session_state.resource_scenarios[scenario_id] = {
                'name': scenario_name,
                'type': scenario_type,
                'original_allocation': total_allocated,
                'original_availability': total_available,
                'original_utilization': overall_utilization,
                'scenario_allocation': scenario_total_allocated,
                'scenario_availability': scenario_total_available,
                'scenario_utilization': scenario_overall_utilization,
                'resources': scenario_resources
            }
            
            st.success(f"Scenario '{scenario_name}' saved!")
    
    # Previous scenarios
    st.markdown("---")
    st.markdown("#### Previous Scenarios")
    
    if 'resource_scenarios' in st.session_state and st.session_state.resource_scenarios:
        scenario_options = [f"{data['name']} (Util: {data['scenario_utilization']:.1f}%)" 
                           for sid, data in st.session_state.resource_scenarios.items()]
        
        selected_scenario = st.selectbox("Select Scenario", scenario_options)
        
        if selected_scenario:
            scenario_index = scenario_options.index(selected_scenario)
            scenario_id = list(st.session_state.resource_scenarios.keys())[scenario_index]
            scenario = st.session_state.resource_scenarios[scenario_id]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Allocated", f"{scenario['scenario_allocation']} hours")
            with col2:
                st.metric("Total Availability", f"{scenario['scenario_availability']} hours")
            with col3:
                st.metric("Overall Utilization", f"{scenario['scenario_utilization']:.1f}%")
            
            # Option to delete scenario
            if st.button(f"Delete Scenario: {scenario['name']}"):
                del st.session_state.resource_scenarios[scenario_id]
                st.success(f"Scenario deleted!")
                st.rerun()
    else:
        st.info("No saved resource scenarios yet. Run a scenario analysis to see results here.")

def show_budget_scenarios(project_data):
    """Display budget scenario analysis."""
    st.markdown("### Budget Scenario Analysis")
    st.write("Analyze the impact of budget changes on project performance and constraints.")
    
    # Check if budget data is available
    if 'budget' not in project_data:
        st.warning("No budget data found in the project. Budget scenarios cannot be created.")
        
        # Create sample budget to demonstrate functionality
        st.markdown("#### Sample Budget Data")
        st.info("Using sample budget data for demonstration. In a real project, add budget data to enable this feature.")
        
        # Create sample budget
        sample_budget = {
            'total': 100000,
            'categories': {
                'Personnel': 65000,
                'Equipment': 15000,
                'Software': 10000,
                'Travel': 5000,
                'Contingency': 5000
            },
            'spent': {
                'Personnel': 32500,
                'Equipment': 12000,
                'Software': 8000,
                'Travel': 2000,
                'Contingency': 0
            }
        }
        
        project_data['budget'] = sample_budget
    
    # Get budget data
    budget = project_data.get('budget', {})
    
    # Display current budget status
    st.markdown("#### Current Budget Status")
    
    total_budget = budget.get('total', 0)
    categories = budget.get('categories', {})
    spent = budget.get('spent', {})
    
    # Calculate spent and remaining
    total_spent = sum(spent.values())
    total_remaining = total_budget - total_spent
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Budget", f"${total_budget:,.0f}")
    with col2:
        st.metric("Total Spent", f"${total_spent:,.0f}")
    with col3:
        st.metric("Remaining", f"${total_remaining:,.0f}")
    
    # Create budget breakdown
    budget_data = []
    
    for category, amount in categories.items():
        category_spent = spent.get(category, 0)
        budget_data.append({
            'Category': category,
            'Budget': amount,
            'Spent': category_spent,
            'Remaining': amount - category_spent,
            'Percent Used': category_spent / amount * 100 if amount > 0 else 0
        })
    
    # Display budget breakdown
    budget_df = pd.DataFrame(budget_data)
    
    # Apply color formatting based on percentage used
    def color_percent_used(val):
        if val > 90:
            return 'background-color: rgba(255, 0, 0, 0.2)'
        elif val > 75:
            return 'background-color: rgba(255, 165, 0, 0.2)'
        else:
            return 'background-color: rgba(0, 128, 0, 0.2)'
    
    styled_budget = budget_df.style.format({
        'Budget': '${:,.0f}',
        'Spent': '${:,.0f}',
        'Remaining': '${:,.0f}',
        'Percent Used': '{:.1f}%'
    }).applymap(color_percent_used, subset=['Percent Used'])
    
    st.dataframe(styled_budget, use_container_width=True)
    
    # Create budget chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=budget_df['Category'],
        y=budget_df['Budget'],
        name='Budget',
        marker_color='#B0C4DE'
    ))
    
    fig.add_trace(go.Bar(
        x=budget_df['Category'],
        y=budget_df['Spent'],
        name='Spent',
        marker_color='#4CAF50'
    ))
    
    fig.update_layout(
        title='Budget vs. Actual by Category',
        xaxis_title='Category',
        yaxis_title='Amount ($)',
        barmode='group'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Create scenario options
    st.markdown("#### Create Budget Scenario")
    
    col1, col2 = st.columns(2)
    
    with col1:
        scenario_type = st.radio(
            "Scenario Type",
            ["Budget Increase/Decrease", "Category Reallocation", "Cost Overrun Simulation"]
        )
    
    with col2:
        if scenario_type == "Budget Increase/Decrease":
            budget_change = st.slider(
                "Budget Change (%)", 
                min_value=-30, 
                max_value=30, 
                value=0, 
                step=5
            )
            
            apply_to = st.radio(
                "Apply to",
                ["All Categories Proportionally", "Specific Category"]
            )
            
            if apply_to == "Specific Category":
                category_options = list(categories.keys())
                selected_category = st.selectbox("Select Category", category_options)
                
        elif scenario_type == "Category Reallocation":
            # Allow reallocation of budget between categories
            st.write("Adjust budget allocations between categories:")
            
            reallocation_data = {}
            total_original = sum(categories.values())
            
            for category, amount in categories.items():
                percentage = amount / total_original * 100 if total_original > 0 else 0
                new_percentage = st.slider(
                    f"{category} Allocation (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=percentage,
                    step=1.0,
                    key=f"realloc_{category}"
                )
                reallocation_data[category] = new_percentage
            
            # Check if percentages sum to 100%
            total_percentage = sum(reallocation_data.values())
            if abs(total_percentage - 100) > 1:
                st.warning(f"Total allocation ({total_percentage:.1f}%) should equal 100%. Please adjust.")
                
        elif scenario_type == "Cost Overrun Simulation":
            # Simulate cost overruns in specific categories
            overrun_categories = st.multiselect(
                "Select Categories with Potential Overruns",
                list(categories.keys())
            )
            
            overrun_percentage = st.slider(
                "Overrun Percentage",
                min_value=5,
                max_value=50,
                value=20,
                step=5
            )
            
            contingency_usage = st.checkbox("Use Contingency Budget if Available", value=True)
    
    # Run scenario analysis button
    if st.button("Run Budget Scenario Analysis"):
        with st.spinner("Running budget scenario analysis..."):
            # Create a copy of the project data for the scenario
            scenario_data = copy.deepcopy(project_data)
            scenario_budget = scenario_data.get('budget', {})
            scenario_categories = scenario_budget.get('categories', {})
            scenario_spent = scenario_budget.get('spent', {})
            
            # Apply scenario changes
            if scenario_type == "Budget Increase/Decrease":
                if apply_to == "All Categories Proportionally":
                    # Apply change to total budget and all categories proportionally
                    change_factor = 1 + (budget_change / 100)
                    
                    # Update total budget
                    scenario_budget['total'] = total_budget * change_factor
                    
                    # Update each category proportionally
                    for category in scenario_categories:
                        scenario_categories[category] = categories[category] * change_factor
                    
                    scenario_name = f"Budget {'Increase' if budget_change > 0 else 'Decrease'} of {abs(budget_change)}%"
                    
                else:  # Specific Category
                    # Apply change only to selected category
                    change_factor = 1 + (budget_change / 100)
                    
                    # Update the specific category
                    original_amount = scenario_categories[selected_category]
                    new_amount = original_amount * change_factor
                    delta = new_amount - original_amount
                    
                    scenario_categories[selected_category] = new_amount
                    
                    # Update total budget
                    scenario_budget['total'] = total_budget + delta
                    
                    scenario_name = f"{selected_category} Budget {'Increase' if budget_change > 0 else 'Decrease'} of {abs(budget_change)}%"
                
            elif scenario_type == "Category Reallocation":
                if abs(total_percentage - 100) > 1:
                    st.error("Total allocation must equal 100%. Please adjust and try again.")
                    return
                
                # Keep total budget the same, but reallocate between categories
                for category, percentage in reallocation_data.items():
                    scenario_categories[category] = total_budget * (percentage / 100)
                
                scenario_name = "Budget Reallocation"
                
            elif scenario_type == "Cost Overrun Simulation":
                if not overrun_categories:
                    st.error("Please select at least one category for cost overrun simulation.")
                    return
                
                # Calculate overrun amounts
                overrun_amounts = {}
                total_overrun = 0
                
                for category in overrun_categories:
                    budget_amount = scenario_categories.get(category, 0)
                    spent_amount = scenario_spent.get(category, 0)
                    remaining = budget_amount - spent_amount
                    
                    # Calculate overrun as percentage of remaining budget
                    overrun = remaining * (overrun_percentage / 100)
                    overrun_amounts[category] = overrun
                    total_overrun += overrun
                
                # Use contingency if available and requested
                contingency_used = 0
                if contingency_usage and 'Contingency' in scenario_categories:
                    contingency_budget = scenario_categories.get('Contingency', 0)
                    contingency_spent = scenario_spent.get('Contingency', 0)
                    available_contingency = contingency_budget - contingency_spent
                    
                    if available_contingency > 0:
                        contingency_used = min(available_contingency, total_overrun)
                        scenario_spent['Contingency'] = contingency_spent + contingency_used
                        total_overrun -= contingency_used
                
                # Apply overruns to spent amounts
                for category, overrun in overrun_amounts.items():
                    # Apply full overrun if no contingency, or proportionally reduced if contingency was used
                    if total_overrun > 0:
                        applied_overrun = overrun * (1 - contingency_used / sum(overrun_amounts.values()))
                    else:
                        applied_overrun = 0
                    
                    scenario_spent[category] = scenario_spent.get(category, 0) + applied_overrun
                
                scenario_name = f"Cost Overrun of {overrun_percentage}% in {len(overrun_categories)} Categories"
            
            # Calculate scenario totals
            scenario_total_budget = scenario_budget.get('total', 0)
            scenario_total_spent = sum(scenario_spent.values())
            scenario_total_remaining = scenario_total_budget - scenario_total_spent
            
            # Display scenario results
            st.markdown(f"#### Scenario Results: {scenario_name}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "Total Budget", 
                    f"${scenario_total_budget:,.0f}",
                    delta=int(scenario_total_budget - total_budget)
                )
            with col2:
                st.metric(
                    "Total Spent", 
                    f"${scenario_total_spent:,.0f}",
                    delta=int(scenario_total_spent - total_spent)
                )
            with col3:
                st.metric(
                    "Remaining", 
                    f"${scenario_total_remaining:,.0f}",
                    delta=int(scenario_total_remaining - total_remaining)
                )
            
            # Create scenario budget breakdown
            scenario_budget_data = []
            
            for category, amount in scenario_categories.items():
                category_spent = scenario_spent.get(category, 0)
                scenario_budget_data.append({
                    'Category': category,
                    'Budget': amount,
                    'Spent': category_spent,
                    'Remaining': amount - category_spent,
                    'Percent Used': category_spent / amount * 100 if amount > 0 else 0
                })
            
            # Display scenario budget breakdown
            scenario_budget_df = pd.DataFrame(scenario_budget_data)
            
            # Apply color formatting
            styled_scenario = scenario_budget_df.style.format({
                'Budget': '${:,.0f}',
                'Spent': '${:,.0f}',
                'Remaining': '${:,.0f}',
                'Percent Used': '{:.1f}%'
            }).applymap(color_percent_used, subset=['Percent Used'])
            
            st.dataframe(styled_scenario, use_container_width=True)
            
            # Create comparison chart - Budget vs. Spent for original and scenario
            st.markdown("#### Budget Comparison")
            
            # Prepare data for side-by-side chart
            chart_data = []
            
            for category in set(list(categories.keys()) + list(scenario_categories.keys())):
                original_budget = categories.get(category, 0)
                original_spent = spent.get(category, 0)
                scenario_budget = scenario_categories.get(category, 0)
                scenario_spent = scenario_spent.get(category, 0)
                
                chart_data.append({
                    'Category': category,
                    'Original Budget': original_budget,
                    'Original Spent': original_spent,
                    'Scenario Budget': scenario_budget,
                    'Scenario Spent': scenario_spent,
                    'Original Remaining': original_budget - original_spent,
                    'Scenario Remaining': scenario_budget - scenario_spent,
                    'Budget Change': scenario_budget - original_budget,
                    'Spent Change': scenario_spent - original_spent
                })
            
            chart_df = pd.DataFrame(chart_data)
            
            # Create comparison chart
            fig = go.Figure()
            
            # Add original budget bars
            fig.add_trace(go.Bar(
                x=chart_df['Category'],
                y=chart_df['Original Budget'],
                name='Original Budget',
                marker_color='#B0C4DE'
            ))
            
            # Add scenario budget bars
            fig.add_trace(go.Bar(
                x=chart_df['Category'],
                y=chart_df['Scenario Budget'],
                name='Scenario Budget',
                marker_color='#4CAF50'
            ))
            
            # Add original spent bars
            fig.add_trace(go.Bar(
                x=chart_df['Category'],
                y=chart_df['Original Spent'],
                name='Original Spent',
                marker_color='#FF9800'
            ))
            
            # Add scenario spent bars
            fig.add_trace(go.Bar(
                x=chart_df['Category'],
                y=chart_df['Scenario Spent'],
                name='Scenario Spent',
                marker_color='#F44336'
            ))
            
            fig.update_layout(
                title='Budget Comparison by Category',
                xaxis_title='Category',
                yaxis_title='Amount ($)',
                barmode='group'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Impact analysis
            st.markdown("#### Impact Analysis")
            
            # Check for budget overruns
            original_overruns = [c for c in budget_data if c['Remaining'] < 0]
            scenario_overruns = [c for c in scenario_budget_data if c['Remaining'] < 0]
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "Categories with Overruns (Original)",
                    len(original_overruns)
                )
            with col2:
                st.metric(
                    "Categories with Overruns (Scenario)",
                    len(scenario_overruns),
                    delta=len(scenario_overruns) - len(original_overruns),
                    delta_color="inverse"
                )
            
            # Calculate budget health
            original_health = total_remaining / total_budget * 100 if total_budget > 0 else 0
            scenario_health = scenario_total_remaining / scenario_total_budget * 100 if scenario_total_budget > 0 else 0
            
            st.markdown("##### Budget Health")
            
            # Add gauge charts for budget health
            col1, col2 = st.columns(2)
            
            with col1:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=original_health,
                    title={'text': "Original Budget Health"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': get_health_color(original_health)},
                        'steps': [
                            {'range': [0, 25], 'color': "rgba(255, 0, 0, 0.2)"},
                            {'range': [25, 50], 'color': "rgba(255, 165, 0, 0.2)"},
                            {'range': [50, 75], 'color': "rgba(255, 255, 0, 0.2)"},
                            {'range': [75, 100], 'color': "rgba(0, 128, 0, 0.2)"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 25
                        }
                    }
                ))
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=scenario_health,
                    title={'text': "Scenario Budget Health"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': get_health_color(scenario_health)},
                        'steps': [
                            {'range': [0, 25], 'color': "rgba(255, 0, 0, 0.2)"},
                            {'range': [25, 50], 'color': "rgba(255, 165, 0, 0.2)"},
                            {'range': [50, 75], 'color': "rgba(255, 255, 0, 0.2)"},
                            {'range': [75, 100], 'color': "rgba(0, 128, 0, 0.2)"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 25
                        }
                    }
                ))
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Recommendations based on scenario
            st.markdown("##### Recommendations")
            
            if scenario_type == "Budget Increase/Decrease":
                if budget_change > 0:
                    st.success("✅ Budget increase provides more flexibility and reduces risk.")
                    st.markdown("**Recommendations:**")
                    st.markdown("- Prioritize critical activities that were previously constrained")
                    st.markdown("- Consider increasing contingency reserves")
                    st.markdown("- Reevaluate quality/scope options that were previously descoped")
                else:
                    st.warning("⚠️ Budget decrease requires careful reallocation and may impact scope/quality.")
                    st.markdown("**Recommendations:**")
                    st.markdown("- Identify potential scope reductions to accommodate budget constraints")
                    st.markdown("- Implement stricter cost control measures")
                    st.markdown("- Consider alternative lower-cost approaches")
                    st.markdown("- Review critical vs. nice-to-have features")
                
            elif scenario_type == "Category Reallocation":
                categories_increased = [c for c in chart_data if c['Budget Change'] > 0]
                categories_decreased = [c for c in chart_data if c['Budget Change'] < 0]
                
                st.info("ℹ️ Budget reallocation shifts focus between different aspects of the project.")
                st.markdown("**Recommendations:**")
                
                if categories_increased:
                    st.markdown("Increased categories should receive additional focus:")
                    for category in categories_increased:
                        st.markdown(f"- {category['Category']}: Review plans to utilize additional ${category['Budget Change']:,.0f}")
                
                if categories_decreased:
                    st.markdown("Decreased categories will require adjustments:")
                    for category in categories_decreased:
                        st.markdown(f"- {category['Category']}: Identify options to reduce costs by ${abs(category['Budget Change']):,.0f}")
                
            elif scenario_type == "Cost Overrun Simulation":
                if scenario_health < 25:
                    st.error("🚨 Severe budget risk! Cost overruns will likely require additional funding.")
                    st.markdown("**Recommendations:**")
                    st.markdown("- Prepare budget increase request with detailed justification")
                    st.markdown("- Implement immediate cost containment measures")
                    st.markdown("- Consider reducing scope to meet budget constraints")
                    st.markdown("- Communicate budget risk to stakeholders immediately")
                elif scenario_health < 50:
                    st.warning("⚠️ Moderate budget risk. Cost overruns will significantly reduce buffer.")
                    st.markdown("**Recommendations:**")
                    st.markdown("- Implement enhanced cost monitoring")
                    st.markdown("- Identify potential cost-saving opportunities")
                    st.markdown("- Review and prioritize remaining project activities")
                else:
                    st.success("✅ Budget appears resilient to the simulated cost overruns.")
                    st.markdown("**Recommendations:**")
                    st.markdown("- Continue regular cost monitoring")
                    st.markdown("- Document lessons learned for future budget planning")
            
            # Save scenario
            if 'budget_scenarios' not in st.session_state:
                st.session_state.budget_scenarios = {}
                
            # Save scenario data
            scenario_id = f"scenario_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            st.session_state.budget_scenarios[scenario_id] = {
                'name': scenario_name,
                'type': scenario_type,
                'original_budget': total_budget,
                'original_spent': total_spent,
                'original_remaining': total_remaining,
                'scenario_budget': scenario_total_budget,
                'scenario_spent': scenario_total_spent,
                'scenario_remaining': scenario_total_remaining,
                'categories': scenario_categories,
                'spent': scenario_spent
            }
            
            st.success(f"Scenario '{scenario_name}' saved!")
    
    # Previous scenarios
    st.markdown("---")
    st.markdown("#### Previous Scenarios")
    
    if 'budget_scenarios' in st.session_state and st.session_state.budget_scenarios:
        scenario_options = [f"{data['name']} (Budget: ${data['scenario_budget']:,.0f})" 
                           for sid, data in st.session_state.budget_scenarios.items()]
        
        selected_scenario = st.selectbox("Select Scenario", scenario_options)
        
        if selected_scenario:
            scenario_index = scenario_options.index(selected_scenario)
            scenario_id = list(st.session_state.budget_scenarios.keys())[scenario_index]
            scenario = st.session_state.budget_scenarios[scenario_id]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Budget", f"${scenario['scenario_budget']:,.0f}")
            with col2:
                st.metric("Total Spent", f"${scenario['scenario_spent']:,.0f}")
            with col3:
                st.metric("Remaining", f"${scenario['scenario_remaining']:,.0f}")
            
            # Option to delete scenario
            if st.button(f"Delete Scenario: {scenario['name']}"):
                del st.session_state.budget_scenarios[scenario_id]
                st.success(f"Scenario deleted!")
                st.rerun()
    else:
        st.info("No saved budget scenarios yet. Run a scenario analysis to see results here.")

def recalculate_scenario_schedule(tasks):
    """
    Recalculate the schedule for a scenario after changes to task durations.
    Simple implementation that assumes sequential tasks without dependencies.
    
    Args:
        tasks: List of tasks to recalculate
    """
    # Sort tasks by start date
    sorted_tasks = sorted(tasks, key=lambda t: t.get('start_date', '2025-01-01'))
    
    # Get the first task start date
    if not sorted_tasks:
        return
    
    current_date = datetime.strptime(sorted_tasks[0].get('start_date', '2025-01-01'), '%Y-%m-%d')
    
    # Recalculate dates for each task based on duration
    for task in sorted_tasks:
        # Update start date
        task['start_date'] = current_date.strftime('%Y-%m-%d')
        
        # Calculate end date based on duration
        duration = task.get('duration', 0)
        end_date = current_date + timedelta(days=duration)
        task['end_date'] = end_date.strftime('%Y-%m-%d')
        
        # Move to next task start date
        current_date = end_date

def get_health_color(health_value):
    """Return color for budget health indicator based on value."""
    if health_value < 25:
        return "red"
    elif health_value < 50:
        return "orange"
    elif health_value < 75:
        return "yellow"
    else:
        return "green"