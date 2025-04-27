import streamlit as st
import pandas as pd
import datetime
from utils.visualization import create_raid_compliance_chart

def show_raid_checker(project_data):
    """
    Display the RAID (Risks, Assumptions, Issues, Dependencies) compliance checker.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.subheader("RAID Compliance Checker")
    
    # Get RAID data
    raid_data = project_data.get('raid', {})
    
    # Create tabs for different RAID elements
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Risks", "Assumptions", "Issues", "Dependencies"])
    
    with tab1:
        st.write("""
        The RAID Compliance Checker helps ensure that all Risks, Assumptions, Issues, and Dependencies 
        are properly documented with all required fields. This helps maintain project governance standards.
        """)
        
        # Create RAID compliance chart
        fig = create_raid_compliance_chart(raid_data)
        st.plotly_chart(fig, use_container_width=True)
        
        # Display summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            risk_count = len(raid_data.get('risks', []))
            st.metric("Risks", risk_count)
        
        with col2:
            assumption_count = len(raid_data.get('assumptions', []))
            st.metric("Assumptions", assumption_count)
        
        with col3:
            issue_count = len(raid_data.get('issues', []))
            st.metric("Issues", issue_count)
        
        with col4:
            dependency_count = len(raid_data.get('dependencies', []))
            st.metric("Dependencies", dependency_count)
        
        # Required fields for each category
        required_fields = {
            'risks': ['description', 'impact', 'probability', 'mitigation', 'owner'],
            'assumptions': ['description', 'impact', 'owner', 'validation'],
            'issues': ['description', 'impact', 'owner', 'resolution', 'status'],
            'dependencies': ['description', 'depends_on', 'impact', 'due_date', 'status']
        }
        
        # Check for missing fields
        missing_fields = {}
        
        for category, fields in required_fields.items():
            items = raid_data.get(category, [])
            
            for i, item in enumerate(items):
                missing = [field for field in fields if field not in item or not item[field]]
                
                if missing:
                    if category not in missing_fields:
                        missing_fields[category] = []
                    
                    missing_fields[category].append({
                        'id': item.get('id', i + 1),
                        'description': item.get('description', 'Unknown'),
                        'missing': missing
                    })
        
        # Display missing fields
        if any(missing_fields.values()):
            st.warning("⚠️ Some RAID items are missing required fields")
            
            for category, items in missing_fields.items():
                if items:
                    with st.expander(f"{category.capitalize()} - {len(items)} items with missing fields"):
                        for item in items:
                            st.write(f"ID: {item['id']} - {item['description']}")
                            st.write(f"Missing fields: {', '.join(item['missing'])}")
                            st.write("---")
        else:
            st.success("✅ All RAID items have the required fields")
    
    with tab2:
        st.write("Risk log showing all identified project risks.")
        
        # Edit risks
        risks = raid_data.get('risks', [])
        
        # Display risks table
        if risks:
            risk_df = pd.DataFrame([
                {
                    'ID': risk.get('id', ''),
                    'Description': risk.get('description', ''),
                    'Impact': risk.get('impact', ''),
                    'Probability': risk.get('probability', ''),
                    'Mitigation': risk.get('mitigation', ''),
                    'Owner': risk.get('owner', ''),
                    'Status': risk.get('status', '')
                }
                for risk in risks
            ])
            
            st.dataframe(risk_df, use_container_width=True)
        else:
            st.info("No risks have been recorded yet.")
        
        # Risk actions
        risk_action = st.radio("Risk Actions:", ["Add New Risk", "Edit Existing Risk", "Remove Risk"], key="risk_action")
        
        if risk_action == "Add New Risk":
            with st.form("add_risk_form"):
                st.write("Add a new risk")
                
                # Generate a new risk ID
                new_id = max([risk.get('id', 0) for risk in risks], default=0) + 1
                
                # Risk details
                description = st.text_area("Risk Description")
                
                col1, col2 = st.columns(2)
                with col1:
                    impact = st.selectbox("Impact", ["Low", "Medium", "High"])
                with col2:
                    probability = st.selectbox("Probability", ["Low", "Medium", "High"])
                
                mitigation = st.text_area("Mitigation Plan")
                owner = st.text_input("Risk Owner")
                status = st.selectbox("Status", ["Open", "Mitigated", "Closed", "Accepted"])
                
                # Submit button
                submit_button = st.form_submit_button("Add Risk")
                
                if submit_button:
                    if description and impact and probability and mitigation and owner:
                        # Create new risk
                        new_risk = {
                            'id': new_id,
                            'description': description,
                            'impact': impact,
                            'probability': probability,
                            'mitigation': mitigation,
                            'owner': owner,
                            'status': status
                        }
                        
                        # Add to risks
                        if 'raid' not in project_data:
                            project_data['raid'] = {}
                        
                        if 'risks' not in project_data['raid']:
                            project_data['raid']['risks'] = []
                        
                        project_data['raid']['risks'].append(new_risk)
                        st.success("Risk added successfully!")
                        st.rerun()
                    else:
                        st.error("All fields are required!")
        
        elif risk_action == "Edit Existing Risk":
            if not risks:
                st.info("No risks available to edit.")
            else:
                # Select a risk to edit
                risk_ids = {f"{risk.get('id')} - {risk.get('description')[:30]}...": risk.get('id') for risk in risks}
                selected_risk_label = st.selectbox("Select a risk to edit", options=list(risk_ids.keys()))
                selected_risk_id = risk_ids[selected_risk_label]
                
                # Find the selected risk
                risk_to_edit = next((risk for risk in risks if risk.get('id') == selected_risk_id), None)
                
                if risk_to_edit:
                    with st.form("edit_risk_form"):
                        st.write(f"Editing Risk: {risk_to_edit.get('description')[:50]}...")
                        
                        # Risk details
                        description = st.text_area("Risk Description", value=risk_to_edit.get('description', ''))
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            impact = st.selectbox("Impact", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(risk_to_edit.get('impact', 'Low')))
                        with col2:
                            probability = st.selectbox("Probability", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(risk_to_edit.get('probability', 'Low')))
                        
                        mitigation = st.text_area("Mitigation Plan", value=risk_to_edit.get('mitigation', ''))
                        owner = st.text_input("Risk Owner", value=risk_to_edit.get('owner', ''))
                        status = st.selectbox("Status", ["Open", "Mitigated", "Closed", "Accepted"], index=["Open", "Mitigated", "Closed", "Accepted"].index(risk_to_edit.get('status', 'Open')))
                        
                        # Submit button
                        submit_button = st.form_submit_button("Update Risk")
                        
                        if submit_button:
                            if description and impact and probability and mitigation and owner:
                                # Update risk
                                for i, risk in enumerate(project_data['raid']['risks']):
                                    if risk.get('id') == selected_risk_id:
                                        project_data['raid']['risks'][i] = {
                                            'id': selected_risk_id,
                                            'description': description,
                                            'impact': impact,
                                            'probability': probability,
                                            'mitigation': mitigation,
                                            'owner': owner,
                                            'status': status
                                        }
                                        break
                                
                                st.success("Risk updated successfully!")
                                st.rerun()
                            else:
                                st.error("All fields are required!")
        
        elif risk_action == "Remove Risk":
            if not risks:
                st.info("No risks available to remove.")
            else:
                # Select a risk to remove
                risk_ids = {f"{risk.get('id')} - {risk.get('description')[:30]}...": risk.get('id') for risk in risks}
                selected_risk_label = st.selectbox("Select a risk to remove", options=list(risk_ids.keys()))
                selected_risk_id = risk_ids[selected_risk_label]
                
                if st.button("Remove Risk"):
                    # Remove the risk
                    project_data['raid']['risks'] = [risk for risk in project_data['raid']['risks'] if risk.get('id') != selected_risk_id]
                    st.success("Risk removed successfully!")
                    st.rerun()
    
    with tab3:
        st.write("Assumptions log showing all project assumptions.")
        
        # Edit assumptions
        assumptions = raid_data.get('assumptions', [])
        
        # Display assumptions table
        if assumptions:
            assumption_df = pd.DataFrame([
                {
                    'ID': assumption.get('id', ''),
                    'Description': assumption.get('description', ''),
                    'Impact': assumption.get('impact', ''),
                    'Owner': assumption.get('owner', ''),
                    'Validation': assumption.get('validation', '')
                }
                for assumption in assumptions
            ])
            
            st.dataframe(assumption_df, use_container_width=True)
        else:
            st.info("No assumptions have been recorded yet.")
        
        # Assumption actions
        assumption_action = st.radio("Assumption Actions:", ["Add New Assumption", "Edit Existing Assumption", "Remove Assumption"], key="assumption_action")
        
        if assumption_action == "Add New Assumption":
            with st.form("add_assumption_form"):
                st.write("Add a new assumption")
                
                # Generate a new assumption ID
                new_id = max([assumption.get('id', 0) for assumption in assumptions], default=0) + 1
                
                # Assumption details
                description = st.text_area("Assumption Description")
                impact = st.selectbox("Impact if Invalid", ["Low", "Medium", "High"])
                owner = st.text_input("Assumption Owner")
                validation = st.selectbox("Validation Status", ["Pending", "Validated", "Invalid"])
                
                # Submit button
                submit_button = st.form_submit_button("Add Assumption")
                
                if submit_button:
                    if description and impact and owner:
                        # Create new assumption
                        new_assumption = {
                            'id': new_id,
                            'description': description,
                            'impact': impact,
                            'owner': owner,
                            'validation': validation
                        }
                        
                        # Add to assumptions
                        if 'raid' not in project_data:
                            project_data['raid'] = {}
                        
                        if 'assumptions' not in project_data['raid']:
                            project_data['raid']['assumptions'] = []
                        
                        project_data['raid']['assumptions'].append(new_assumption)
                        st.success("Assumption added successfully!")
                        st.rerun()
                    else:
                        st.error("Description, Impact, and Owner are required!")
        
        elif assumption_action == "Edit Existing Assumption":
            if not assumptions:
                st.info("No assumptions available to edit.")
            else:
                # Select an assumption to edit
                assumption_ids = {f"{assumption.get('id')} - {assumption.get('description')[:30]}...": assumption.get('id') for assumption in assumptions}
                selected_assumption_label = st.selectbox("Select an assumption to edit", options=list(assumption_ids.keys()))
                selected_assumption_id = assumption_ids[selected_assumption_label]
                
                # Find the selected assumption
                assumption_to_edit = next((assumption for assumption in assumptions if assumption.get('id') == selected_assumption_id), None)
                
                if assumption_to_edit:
                    with st.form("edit_assumption_form"):
                        st.write(f"Editing Assumption: {assumption_to_edit.get('description')[:50]}...")
                        
                        # Assumption details
                        description = st.text_area("Assumption Description", value=assumption_to_edit.get('description', ''))
                        impact = st.selectbox("Impact if Invalid", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(assumption_to_edit.get('impact', 'Low')))
                        owner = st.text_input("Assumption Owner", value=assumption_to_edit.get('owner', ''))
                        validation = st.selectbox("Validation Status", ["Pending", "Validated", "Invalid"], index=["Pending", "Validated", "Invalid"].index(assumption_to_edit.get('validation', 'Pending')))
                        
                        # Submit button
                        submit_button = st.form_submit_button("Update Assumption")
                        
                        if submit_button:
                            if description and impact and owner:
                                # Update assumption
                                for i, assumption in enumerate(project_data['raid']['assumptions']):
                                    if assumption.get('id') == selected_assumption_id:
                                        project_data['raid']['assumptions'][i] = {
                                            'id': selected_assumption_id,
                                            'description': description,
                                            'impact': impact,
                                            'owner': owner,
                                            'validation': validation
                                        }
                                        break
                                
                                st.success("Assumption updated successfully!")
                                st.rerun()
                            else:
                                st.error("Description, Impact, and Owner are required!")
        
        elif assumption_action == "Remove Assumption":
            if not assumptions:
                st.info("No assumptions available to remove.")
            else:
                # Select an assumption to remove
                assumption_ids = {f"{assumption.get('id')} - {assumption.get('description')[:30]}...": assumption.get('id') for assumption in assumptions}
                selected_assumption_label = st.selectbox("Select an assumption to remove", options=list(assumption_ids.keys()))
                selected_assumption_id = assumption_ids[selected_assumption_label]
                
                if st.button("Remove Assumption"):
                    # Remove the assumption
                    project_data['raid']['assumptions'] = [assumption for assumption in project_data['raid']['assumptions'] if assumption.get('id') != selected_assumption_id]
                    st.success("Assumption removed successfully!")
                    st.rerun()
    
    with tab4:
        st.write("Issues log showing all project issues.")
        
        # Edit issues
        issues = raid_data.get('issues', [])
        
        # Display issues table
        if issues:
            issue_df = pd.DataFrame([
                {
                    'ID': issue.get('id', ''),
                    'Description': issue.get('description', ''),
                    'Impact': issue.get('impact', ''),
                    'Raised Date': issue.get('raised_date', ''),
                    'Owner': issue.get('owner', ''),
                    'Resolution': issue.get('resolution', ''),
                    'Status': issue.get('status', '')
                }
                for issue in issues
            ])
            
            st.dataframe(issue_df, use_container_width=True)
        else:
            st.info("No issues have been recorded yet.")
        
        # Issue actions
        issue_action = st.radio("Issue Actions:", ["Add New Issue", "Edit Existing Issue", "Remove Issue"], key="issue_action")
        
        if issue_action == "Add New Issue":
            with st.form("add_issue_form"):
                st.write("Add a new issue")
                
                # Generate a new issue ID
                new_id = max([issue.get('id', 0) for issue in issues], default=0) + 1
                
                # Issue details
                description = st.text_area("Issue Description")
                impact = st.selectbox("Impact", ["Low", "Medium", "High"])
                raised_date = st.date_input("Date Raised", value=datetime.datetime.now()).strftime("%Y-%m-%d")
                owner = st.text_input("Issue Owner")
                resolution = st.text_area("Resolution Plan")
                status = st.selectbox("Status", ["Open", "In Progress", "Closed"])
                
                # Submit button
                submit_button = st.form_submit_button("Add Issue")
                
                if submit_button:
                    if description and impact and owner and resolution:
                        # Create new issue
                        new_issue = {
                            'id': new_id,
                            'description': description,
                            'impact': impact,
                            'raised_date': raised_date,
                            'owner': owner,
                            'resolution': resolution,
                            'status': status
                        }
                        
                        # Add to issues
                        if 'raid' not in project_data:
                            project_data['raid'] = {}
                        
                        if 'issues' not in project_data['raid']:
                            project_data['raid']['issues'] = []
                        
                        project_data['raid']['issues'].append(new_issue)
                        st.success("Issue added successfully!")
                        st.rerun()
                    else:
                        st.error("Description, Impact, Owner, and Resolution are required!")
        
        elif issue_action == "Edit Existing Issue":
            if not issues:
                st.info("No issues available to edit.")
            else:
                # Select an issue to edit
                issue_ids = {f"{issue.get('id')} - {issue.get('description')[:30]}...": issue.get('id') for issue in issues}
                selected_issue_label = st.selectbox("Select an issue to edit", options=list(issue_ids.keys()))
                selected_issue_id = issue_ids[selected_issue_label]
                
                # Find the selected issue
                issue_to_edit = next((issue for issue in issues if issue.get('id') == selected_issue_id), None)
                
                if issue_to_edit:
                    with st.form("edit_issue_form"):
                        st.write(f"Editing Issue: {issue_to_edit.get('description')[:50]}...")
                        
                        # Issue details
                        description = st.text_area("Issue Description", value=issue_to_edit.get('description', ''))
                        impact = st.selectbox("Impact", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(issue_to_edit.get('impact', 'Low')))
                        
                        raised_date = st.date_input(
                            "Date Raised", 
                            value=datetime.datetime.strptime(issue_to_edit.get('raised_date', datetime.datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d")
                        ).strftime("%Y-%m-%d")
                        
                        owner = st.text_input("Issue Owner", value=issue_to_edit.get('owner', ''))
                        resolution = st.text_area("Resolution Plan", value=issue_to_edit.get('resolution', ''))
                        status = st.selectbox("Status", ["Open", "In Progress", "Closed"], index=["Open", "In Progress", "Closed"].index(issue_to_edit.get('status', 'Open')))
                        
                        # Submit button
                        submit_button = st.form_submit_button("Update Issue")
                        
                        if submit_button:
                            if description and impact and owner and resolution:
                                # Update issue
                                for i, issue in enumerate(project_data['raid']['issues']):
                                    if issue.get('id') == selected_issue_id:
                                        project_data['raid']['issues'][i] = {
                                            'id': selected_issue_id,
                                            'description': description,
                                            'impact': impact,
                                            'raised_date': raised_date,
                                            'owner': owner,
                                            'resolution': resolution,
                                            'status': status
                                        }
                                        break
                                
                                st.success("Issue updated successfully!")
                                st.rerun()
                            else:
                                st.error("Description, Impact, Owner, and Resolution are required!")
        
        elif issue_action == "Remove Issue":
            if not issues:
                st.info("No issues available to remove.")
            else:
                # Select an issue to remove
                issue_ids = {f"{issue.get('id')} - {issue.get('description')[:30]}...": issue.get('id') for issue in issues}
                selected_issue_label = st.selectbox("Select an issue to remove", options=list(issue_ids.keys()))
                selected_issue_id = issue_ids[selected_issue_label]
                
                if st.button("Remove Issue"):
                    # Remove the issue
                    project_data['raid']['issues'] = [issue for issue in project_data['raid']['issues'] if issue.get('id') != selected_issue_id]
                    st.success("Issue removed successfully!")
                    st.rerun()
    
    with tab5:
        st.write("Dependencies log showing all project dependencies.")
        
        # Edit dependencies
        dependencies = raid_data.get('dependencies', [])
        
        # Display dependencies table
        if dependencies:
            dependency_df = pd.DataFrame([
                {
                    'ID': dependency.get('id', ''),
                    'Description': dependency.get('description', ''),
                    'Depends On': dependency.get('depends_on', ''),
                    'Impact': dependency.get('impact', ''),
                    'Due Date': dependency.get('due_date', ''),
                    'Status': dependency.get('status', '')
                }
                for dependency in dependencies
            ])
            
            st.dataframe(dependency_df, use_container_width=True)
        else:
            st.info("No dependencies have been recorded yet.")
        
        # Dependency actions
        dependency_action = st.radio("Dependency Actions:", ["Add New Dependency", "Edit Existing Dependency", "Remove Dependency"], key="dependency_action")
        
        if dependency_action == "Add New Dependency":
            with st.form("add_dependency_form"):
                st.write("Add a new dependency")
                
                # Generate a new dependency ID
                new_id = max([dependency.get('id', 0) for dependency in dependencies], default=0) + 1
                
                # Dependency details
                description = st.text_area("Dependency Description")
                depends_on = st.text_input("Depends On (team, system, or external party)")
                impact = st.selectbox("Impact", ["Low", "Medium", "High"])
                due_date = st.date_input("Due Date", value=datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
                status = st.selectbox("Status", ["Not Started", "In Progress", "Completed", "Blocked"])
                
                # Submit button
                submit_button = st.form_submit_button("Add Dependency")
                
                if submit_button:
                    if description and depends_on and impact:
                        # Create new dependency
                        new_dependency = {
                            'id': new_id,
                            'description': description,
                            'depends_on': depends_on,
                            'impact': impact,
                            'due_date': due_date,
                            'status': status
                        }
                        
                        # Add to dependencies
                        if 'raid' not in project_data:
                            project_data['raid'] = {}
                        
                        if 'dependencies' not in project_data['raid']:
                            project_data['raid']['dependencies'] = []
                        
                        project_data['raid']['dependencies'].append(new_dependency)
                        st.success("Dependency added successfully!")
                        st.rerun()
                    else:
                        st.error("Description, Depends On, and Impact are required!")
        
        elif dependency_action == "Edit Existing Dependency":
            if not dependencies:
                st.info("No dependencies available to edit.")
            else:
                # Select a dependency to edit
                dependency_ids = {f"{dependency.get('id')} - {dependency.get('description')[:30]}...": dependency.get('id') for dependency in dependencies}
                selected_dependency_label = st.selectbox("Select a dependency to edit", options=list(dependency_ids.keys()))
                selected_dependency_id = dependency_ids[selected_dependency_label]
                
                # Find the selected dependency
                dependency_to_edit = next((dependency for dependency in dependencies if dependency.get('id') == selected_dependency_id), None)
                
                if dependency_to_edit:
                    with st.form("edit_dependency_form"):
                        st.write(f"Editing Dependency: {dependency_to_edit.get('description')[:50]}...")
                        
                        # Dependency details
                        description = st.text_area("Dependency Description", value=dependency_to_edit.get('description', ''))
                        depends_on = st.text_input("Depends On (team, system, or external party)", value=dependency_to_edit.get('depends_on', ''))
                        impact = st.selectbox("Impact", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(dependency_to_edit.get('impact', 'Low')))
                        
                        due_date = st.date_input(
                            "Due Date", 
                            value=datetime.datetime.strptime(dependency_to_edit.get('due_date', (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")), "%Y-%m-%d")
                        ).strftime("%Y-%m-%d")
                        
                        status = st.selectbox("Status", ["Not Started", "In Progress", "Completed", "Blocked"], index=["Not Started", "In Progress", "Completed", "Blocked"].index(dependency_to_edit.get('status', 'Not Started')))
                        
                        # Submit button
                        submit_button = st.form_submit_button("Update Dependency")
                        
                        if submit_button:
                            if description and depends_on and impact:
                                # Update dependency
                                for i, dependency in enumerate(project_data['raid']['dependencies']):
                                    if dependency.get('id') == selected_dependency_id:
                                        project_data['raid']['dependencies'][i] = {
                                            'id': selected_dependency_id,
                                            'description': description,
                                            'depends_on': depends_on,
                                            'impact': impact,
                                            'due_date': due_date,
                                            'status': status
                                        }
                                        break
                                
                                st.success("Dependency updated successfully!")
                                st.rerun()
                            else:
                                st.error("Description, Depends On, and Impact are required!")
        
        elif dependency_action == "Remove Dependency":
            if not dependencies:
                st.info("No dependencies available to remove.")
            else:
                # Select a dependency to remove
                dependency_ids = {f"{dependency.get('id')} - {dependency.get('description')[:30]}...": dependency.get('id') for dependency in dependencies}
                selected_dependency_label = st.selectbox("Select a dependency to remove", options=list(dependency_ids.keys()))
                selected_dependency_id = dependency_ids[selected_dependency_label]
                
                if st.button("Remove Dependency"):
                    # Remove the dependency
                    project_data['raid']['dependencies'] = [dependency for dependency in project_data['raid']['dependencies'] if dependency.get('id') != selected_dependency_id]
                    st.success("Dependency removed successfully!")
                    st.rerun()
