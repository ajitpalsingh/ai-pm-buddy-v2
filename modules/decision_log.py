import streamlit as st
import pandas as pd
import datetime
from utils.visualization import create_decision_status_chart

def show_decision_log(project_data):
    """
    Display the decision log assistant module.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.subheader("Decision Log Assistant")
    
    # Get decision log data
    decisions = project_data.get('decisions', [])
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Decision Log", "Add/Edit Decisions"])
    
    with tab1:
        st.write("""
        The Decision Log tracks important project decisions, their rationale, and approval status.
        This helps maintain a clear record of decisions made throughout the project lifecycle.
        """)
        
        if not decisions:
            st.info("No decisions have been recorded yet. Use the 'Add/Edit Decisions' tab to add decisions.")
        else:
            # Create decision status chart
            fig = create_decision_status_chart(decisions)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            # Create decision table
            decision_df = pd.DataFrame([
                {
                    'ID': decision.get('id', ''),
                    'Description': decision.get('description', ''),
                    'Rationale': decision.get('rationale', ''),
                    'Date': decision.get('decision_date', ''),
                    'Decided By': decision.get('decided_by', ''),
                    'Impact': decision.get('impact', ''),
                    'Status': decision.get('status', '')
                }
                for decision in decisions
            ])
            
            # Add filter for status
            status_filter = st.multiselect(
                "Filter by Status",
                options=sorted(list(set(d.get('status', '') for d in decisions))),
                default=sorted(list(set(d.get('status', '') for d in decisions)))
            )
            
            # Filter the dataframe
            if status_filter:
                filtered_df = decision_df[decision_df['Status'].isin(status_filter)]
            else:
                filtered_df = decision_df
            
            # Display the filtered table
            st.dataframe(filtered_df, use_container_width=True)
            
            # Display counts by status
            st.subheader("Decision Status Summary")
            
            status_counts = decision_df['Status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                pending_count = status_counts[status_counts['Status'] == 'Pending Approval']['Count'].sum() if 'Pending Approval' in status_counts['Status'].values else 0
                st.metric("Pending Approval", pending_count)
            
            with col2:
                approved_count = status_counts[status_counts['Status'] == 'Approved']['Count'].sum() if 'Approved' in status_counts['Status'].values else 0
                st.metric("Approved", approved_count)
            
            with col3:
                rejected_count = status_counts[status_counts['Status'] == 'Rejected']['Count'].sum() if 'Rejected' in status_counts['Status'].values else 0
                st.metric("Rejected", rejected_count)
    
    with tab2:
        st.write("Add, edit, or remove decisions in the decision log.")
        
        # Action selection
        action = st.radio("Select action:", ["Add New Decision", "Edit Existing Decision", "Remove Decision"])
        
        if action == "Add New Decision":
            with st.form("add_decision_form"):
                st.write("Add a new decision")
                
                # Generate a new decision ID
                new_id = max([decision.get('id', 0) for decision in decisions], default=0) + 1
                
                # Decision details
                description = st.text_area("Decision Description")
                rationale = st.text_area("Rationale")
                
                col1, col2 = st.columns(2)
                with col1:
                    decision_date = st.date_input("Decision Date", value=datetime.datetime.now()).strftime("%Y-%m-%d")
                with col2:
                    decided_by = st.text_input("Decided By")
                
                impact = st.selectbox("Impact", ["Low", "Medium", "High"])
                status = st.selectbox("Status", ["Pending Approval", "Approved", "Rejected", "Deferred"])
                
                # Submit button
                submit_button = st.form_submit_button("Add Decision")
                
                if submit_button:
                    if description and rationale and decided_by:
                        # Create new decision
                        new_decision = {
                            'id': new_id,
                            'description': description,
                            'rationale': rationale,
                            'decision_date': decision_date,
                            'decided_by': decided_by,
                            'impact': impact,
                            'status': status
                        }
                        
                        # Add to decisions
                        if 'decisions' not in project_data:
                            project_data['decisions'] = []
                        
                        project_data['decisions'].append(new_decision)
                        st.success("Decision added successfully!")
                        st.rerun()
                    else:
                        st.error("Decision description, rationale, and decided by are required!")
        
        elif action == "Edit Existing Decision":
            if not decisions:
                st.info("No decisions available to edit.")
            else:
                # Select a decision to edit
                decision_ids = {f"{decision.get('id')} - {decision.get('description')[:30]}...": decision.get('id') for decision in decisions}
                selected_decision_label = st.selectbox("Select a decision to edit", options=list(decision_ids.keys()))
                selected_decision_id = decision_ids[selected_decision_label]
                
                # Find the selected decision
                decision_to_edit = next((decision for decision in decisions if decision.get('id') == selected_decision_id), None)
                
                if decision_to_edit:
                    with st.form("edit_decision_form"):
                        st.write(f"Editing Decision: {decision_to_edit.get('description')[:50]}...")
                        
                        # Decision details
                        description = st.text_area("Decision Description", value=decision_to_edit.get('description', ''))
                        rationale = st.text_area("Rationale", value=decision_to_edit.get('rationale', ''))
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            decision_date = st.date_input(
                                "Decision Date", 
                                value=datetime.datetime.strptime(decision_to_edit.get('decision_date', datetime.datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d")
                            ).strftime("%Y-%m-%d")
                        with col2:
                            decided_by = st.text_input("Decided By", value=decision_to_edit.get('decided_by', ''))
                        
                        impact = st.selectbox("Impact", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(decision_to_edit.get('impact', 'Low')))
                        status = st.selectbox("Status", ["Pending Approval", "Approved", "Rejected", "Deferred"], index=["Pending Approval", "Approved", "Rejected", "Deferred"].index(decision_to_edit.get('status', 'Pending Approval')))
                        
                        # Submit button
                        submit_button = st.form_submit_button("Update Decision")
                        
                        if submit_button:
                            if description and rationale and decided_by:
                                # Update decision
                                for i, decision in enumerate(project_data['decisions']):
                                    if decision.get('id') == selected_decision_id:
                                        project_data['decisions'][i] = {
                                            'id': selected_decision_id,
                                            'description': description,
                                            'rationale': rationale,
                                            'decision_date': decision_date,
                                            'decided_by': decided_by,
                                            'impact': impact,
                                            'status': status
                                        }
                                        break
                                
                                st.success("Decision updated successfully!")
                                st.rerun()
                            else:
                                st.error("Decision description, rationale, and decided by are required!")
        
        elif action == "Remove Decision":
            if not decisions:
                st.info("No decisions available to remove.")
            else:
                # Select a decision to remove
                decision_ids = {f"{decision.get('id')} - {decision.get('description')[:30]}...": decision.get('id') for decision in decisions}
                selected_decision_label = st.selectbox("Select a decision to remove", options=list(decision_ids.keys()))
                selected_decision_id = decision_ids[selected_decision_label]
                
                if st.button("Remove Decision"):
                    # Remove the decision
                    project_data['decisions'] = [decision for decision in project_data['decisions'] if decision.get('id') != selected_decision_id]
                    st.success("Decision removed successfully!")
                    st.rerun()
