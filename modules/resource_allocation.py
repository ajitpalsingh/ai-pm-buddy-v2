import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.visualization import create_resource_allocation_chart

def show_resource_allocation(project_data):
    """
    Display resource allocation monitoring page.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.subheader("Resource Allocation Monitoring")
    
    # Get resource data
    resource_data = project_data.get('resources', [])
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Overview", "Resource Details", "Edit Resources"])
    
    with tab1:
        if not resource_data:
            st.info("No resource data available. Use the 'Edit Resources' tab to add resources.")
        else:
            # Create resource allocation chart
            fig = create_resource_allocation_chart(resource_data)
            st.plotly_chart(fig, use_container_width=True)
            
            # Calculate overall statistics
            total_availability = sum(r.get('availability', 0) for r in resource_data)
            total_allocated = sum(r.get('allocated', 0) for r in resource_data)
            overall_utilization = (total_allocated / total_availability * 100) if total_availability > 0 else 0
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Resources", len(resource_data))
            
            with col2:
                st.metric("Overall Utilization", f"{overall_utilization:.1f}%")
            
            with col3:
                overallocated_count = sum(1 for r in resource_data if r.get('allocated', 0) > r.get('availability', 0))
                
                if overallocated_count > 0:
                    st.metric("Overallocated Resources", overallocated_count, delta=overallocated_count, delta_color="inverse")
                else:
                    st.metric("Overallocated Resources", overallocated_count)
            
            # Display warnings for overallocated or underutilized resources
            overallocated = [r for r in resource_data if r.get('allocated', 0) > r.get('availability', 0)]
            underutilized = [r for r in resource_data if r.get('allocated', 0) < 0.5 * r.get('availability', 0)]
            
            if overallocated:
                st.warning("⚠️ Some resources are overallocated:")
                
                # Show overallocated resources
                over_df = pd.DataFrame([{
                    'Resource': r.get('name', ''),
                    'Role': r.get('role', ''),
                    'Utilization': f"{(r.get('allocated', 0) / r.get('availability', 1) * 100):.0f}%",
                    'Over by': f"{r.get('allocated', 0) - r.get('availability', 0)} hours"
                } for r in overallocated])
                
                st.dataframe(over_df, use_container_width=True)
            
            if underutilized:
                st.info("ℹ️ Some resources are underutilized (<50%):")
                
                # Show underutilized resources
                under_df = pd.DataFrame([{
                    'Resource': r.get('name', ''),
                    'Role': r.get('role', ''),
                    'Utilization': f"{(r.get('allocated', 0) / r.get('availability', 1) * 100):.0f}%",
                    'Available': f"{r.get('availability', 0) - r.get('allocated', 0)} hours"
                } for r in underutilized])
                
                st.dataframe(under_df, use_container_width=True)
    
    with tab2:
        if not resource_data:
            st.info("No resource data available. Use the 'Edit Resources' tab to add resources.")
        else:
            # Create a DataFrame for the resources
            resource_df = pd.DataFrame([
                {
                    'Name': r.get('name', ''),
                    'Role': r.get('role', ''),
                    'Availability (hours)': r.get('availability', 0),
                    'Allocated (hours)': r.get('allocated', 0),
                    'Utilization (%)': f"{(r.get('allocated', 0) / r.get('availability', 1) * 100):.1f}%",
                    'Skills': ', '.join(r.get('skills', []))
                }
                for r in resource_data
            ])
            
            # Display the resources table
            st.dataframe(resource_df, use_container_width=True)
            
            # Resource skills analysis
            st.subheader("Skills Distribution")
            
            # Extract and count all skills
            all_skills = []
            for resource in resource_data:
                all_skills.extend(resource.get('skills', []))
            
            if all_skills:
                skill_counts = pd.Series(all_skills).value_counts().reset_index()
                skill_counts.columns = ['Skill', 'Count']
                
                # Create a horizontal bar chart for skills
                fig = px.bar(
                    skill_counts, 
                    y='Skill', 
                    x='Count', 
                    orientation='h',
                    title='Team Skills Distribution',
                    color='Count',
                    color_continuous_scale=px.colors.sequential.Viridis
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Highlight potential skill gaps
                st.subheader("Skill Coverage Analysis")
                
                low_coverage_skills = skill_counts[skill_counts['Count'] == 1]['Skill'].tolist()
                
                if low_coverage_skills:
                    st.warning(f"⚠️ The following skills have only one team member proficient:")
                    for skill in low_coverage_skills:
                        resources_with_skill = [r.get('name') for r in resource_data if skill in r.get('skills', [])]
                        st.write(f"- **{skill}**: {', '.join(resources_with_skill)}")
            else:
                st.info("No skills data available for analysis.")
    
    with tab3:
        st.write("Add, edit, or remove resources.")
        
        # Action selection
        action = st.radio("Select action:", ["Add New Resource", "Edit Existing Resource", "Update Allocation", "Remove Resource"])
        
        if action == "Add New Resource":
            with st.form("add_resource_form"):
                st.write("Add a new resource")
                
                # Resource details
                name = st.text_input("Name")
                role = st.text_input("Role")
                
                col1, col2 = st.columns(2)
                with col1:
                    availability = st.number_input("Availability (hours)", min_value=0, value=100)
                with col2:
                    allocated = st.number_input("Allocated (hours)", min_value=0, value=0)
                
                # Skills
                skills_input = st.text_input("Skills (comma separated)")
                skills = [skill.strip() for skill in skills_input.split(',')] if skills_input else []
                
                # Submit button
                submit_button = st.form_submit_button("Add Resource")
                
                if submit_button:
                    if name and role:
                        # Create new resource
                        new_resource = {
                            'name': name,
                            'role': role,
                            'availability': availability,
                            'allocated': allocated,
                            'skills': skills
                        }
                        
                        # Add to resource data
                        if 'resources' not in project_data:
                            project_data['resources'] = []
                        
                        project_data['resources'].append(new_resource)
                        st.success(f"Resource '{name}' added successfully!")
                        st.rerun()
                    else:
                        st.error("Name and Role are required!")
        
        elif action == "Edit Existing Resource":
            if not resource_data:
                st.info("No resources available to edit.")
            else:
                # Select a resource to edit
                resource_names = {r.get('name'): i for i, r in enumerate(resource_data)}
                selected_resource_name = st.selectbox("Select a resource to edit", options=list(resource_names.keys()))
                selected_resource_idx = resource_names[selected_resource_name]
                
                # Get the selected resource
                resource_to_edit = resource_data[selected_resource_idx]
                
                with st.form("edit_resource_form"):
                    st.write(f"Editing Resource: {resource_to_edit.get('name')}")
                    
                    # Resource details
                    name = st.text_input("Name", value=resource_to_edit.get('name', ''))
                    role = st.text_input("Role", value=resource_to_edit.get('role', ''))
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        availability = st.number_input("Availability (hours)", min_value=0, value=resource_to_edit.get('availability', 0))
                    with col2:
                        allocated = st.number_input("Allocated (hours)", min_value=0, value=resource_to_edit.get('allocated', 0))
                    
                    # Skills
                    skills_input = st.text_input("Skills (comma separated)", value=', '.join(resource_to_edit.get('skills', [])))
                    skills = [skill.strip() for skill in skills_input.split(',')] if skills_input else []
                    
                    # Submit button
                    submit_button = st.form_submit_button("Update Resource")
                    
                    if submit_button:
                        if name and role:
                            # Update resource
                            project_data['resources'][selected_resource_idx] = {
                                'name': name,
                                'role': role,
                                'availability': availability,
                                'allocated': allocated,
                                'skills': skills
                            }
                            
                            st.success(f"Resource '{name}' updated successfully!")
                            st.rerun()
                        else:
                            st.error("Name and Role are required!")
        
        elif action == "Update Allocation":
            if not resource_data:
                st.info("No resources available to update allocation.")
            else:
                # Create a form for bulk allocation update
                with st.form("update_allocation_form"):
                    st.write("Update resource allocation")
                    
                    # Create a DataFrame for the resources
                    allocation_df = pd.DataFrame([
                        {
                            'Name': r.get('name', ''),
                            'Role': r.get('role', ''),
                            'Availability': r.get('availability', 0),
                            'Current Allocation': r.get('allocated', 0),
                            'Utilization': f"{(r.get('allocated', 0) / r.get('availability', 1) * 100):.1f}%"
                        }
                        for r in resource_data
                    ])
                    
                    # Display the current allocation
                    st.dataframe(allocation_df, use_container_width=True)
                    
                    # Select a resource to update
                    resource_names = {r.get('name'): i for i, r in enumerate(resource_data)}
                    selected_resource_name = st.selectbox("Select a resource to update", options=list(resource_names.keys()))
                    selected_resource_idx = resource_names[selected_resource_name]
                    
                    # Get the selected resource
                    resource_to_update = resource_data[selected_resource_idx]
                    
                    # Update allocation
                    new_allocation = st.number_input(
                        "New Allocation (hours)", 
                        min_value=0, 
                        value=resource_to_update.get('allocated', 0)
                    )
                    
                    # Show warning if overallocated
                    if new_allocation > resource_to_update.get('availability', 0):
                        st.warning(f"⚠️ This allocation exceeds availability by {new_allocation - resource_to_update.get('availability', 0)} hours!")
                    
                    # Submit button
                    submit_button = st.form_submit_button("Update Allocation")
                    
                    if submit_button:
                        # Update allocation for the selected resource
                        project_data['resources'][selected_resource_idx]['allocated'] = new_allocation
                        
                        st.success(f"Allocation updated successfully!")
                        st.rerun()
        
        elif action == "Remove Resource":
            if not resource_data:
                st.info("No resources available to remove.")
            else:
                # Select a resource to remove
                resource_names = {r.get('name'): i for i, r in enumerate(resource_data)}
                selected_resource_name = st.selectbox("Select a resource to remove", options=list(resource_names.keys()))
                
                if st.button("Remove Resource"):
                    # Check if resource is assigned to any tasks
                    assigned_tasks = [task.get('task') for task in project_data.get('wbs', []) if task.get('assigned_to') == selected_resource_name]
                    
                    if assigned_tasks:
                        st.error(f"Cannot remove this resource as it is assigned to: {', '.join(assigned_tasks)}")
                    else:
                        # Remove the resource
                        project_data['resources'] = [r for r in project_data['resources'] if r.get('name') != selected_resource_name]
                        st.success(f"Resource removed successfully!")
                        st.rerun()
