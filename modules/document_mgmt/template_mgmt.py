import streamlit as st
import pandas as pd
import os
import json
import datetime
from io import StringIO

def show_template_management(project_data):
    """
    Display the Template Management module for creating and managing document templates.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.subheader("Document Template Management")
    
    # Initialize template storage in session state if it doesn't exist
    if 'document_templates' not in st.session_state:
        st.session_state.document_templates = {
            "status_report": {
                "name": "Status Report",
                "description": "Standard project status report template",
                "sections": ["Executive Summary", "Milestone Status", "Risk Summary", "Issues Log", "Budget Status", "Resource Status", "Next Steps"],
                "variables": ["project_name", "report_period", "start_date", "end_date"],
                "content": """# {project_name} - {report_period} Status Report

**Period:** {start_date} to {end_date}

## Executive Summary

[Provide a brief overview of the project status, highlighting key achievements, challenges, and overall health]

## Milestone Status

| Milestone | Due Date | Status | Comments |
|-----------|----------|--------|----------|
| [Milestone 1] | [Date] | [Status] | [Comments] |
| [Milestone 2] | [Date] | [Status] | [Comments] |

## Risk Summary

[Summarize top risks and mitigation strategies]

## Next Steps

[List upcoming activities and priorities]
"""
            },
            "meeting_minutes": {
                "name": "Meeting Minutes",
                "description": "Standard meeting minutes template",
                "sections": ["Attendees", "Agenda", "Discussion Points", "Action Items", "Next Meeting"],
                "variables": ["project_name", "meeting_type", "meeting_date", "attendees"],
                "content": """# {project_name} - {meeting_type} Minutes

**Date:** {meeting_date}

## Attendees

{attendees}

## Agenda

1. [Agenda Item 1]
2. [Agenda Item 2]
3. [Agenda Item 3]

## Discussion Points

### [Agenda Item 1]
- [Discussion point]
- [Discussion point]

### [Agenda Item 2]
- [Discussion point]
- [Discussion point]

## Action Items

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [Action 1] | [Owner] | [Date] | New |
| [Action 2] | [Owner] | [Date] | New |

## Next Meeting

- Date: [Next meeting date]
- Time: [Time]
"""
            }
        }
    
    # Create tabs for template management
    tab1, tab2 = st.tabs(["Available Templates", "Create/Edit Template"])
    
    with tab1:
        st.markdown("### Available Templates")
        
        # Display available templates in a table
        if st.session_state.document_templates:
            template_data = []
            for template_id, template in st.session_state.document_templates.items():
                template_data.append({
                    "ID": template_id,
                    "Name": template["name"],
                    "Description": template["description"],
                    "Sections": len(template["sections"]),
                    "Variables": len(template["variables"])
                })
            
            template_df = pd.DataFrame(template_data)
            st.dataframe(template_df, use_container_width=True)
            
            # Template preview
            template_to_preview = st.selectbox(
                "Select template to preview:", 
                list(st.session_state.document_templates.keys()),
                format_func=lambda x: st.session_state.document_templates[x]["name"]
            )
            
            if template_to_preview:
                with st.expander(f"Preview: {st.session_state.document_templates[template_to_preview]['name']}"):
                    st.markdown("#### Template Content")
                    st.code(st.session_state.document_templates[template_to_preview]["content"], language="markdown")
                    
                    st.markdown("#### Variables")
                    for var in st.session_state.document_templates[template_to_preview]["variables"]:
                        st.markdown(f"- `{{{var}}}`")
                    
                    # Option to delete template
                    if st.button(f"Delete Template: {st.session_state.document_templates[template_to_preview]['name']}"):
                        del st.session_state.document_templates[template_to_preview]
                        st.success(f"Template deleted!")
                        st.rerun()
        else:
            st.info("No templates available. Create a new template to get started.")
    
    with tab2:
        st.markdown("### Create or Edit Template")
        
        # Template selection or creation
        template_action = st.radio("Action:", ["Create New Template", "Edit Existing Template"])
        
        if template_action == "Create New Template":
            new_template_id = st.text_input("Template ID (unique identifier, no spaces):")
            if new_template_id in st.session_state.document_templates:
                st.warning(f"Template ID '{new_template_id}' already exists. Choose a different ID or edit the existing template.")
                return
                
            template_name = st.text_input("Template Name:")
            template_description = st.text_area("Description:")
            
            # Template sections
            sections_input = st.text_area("Sections (one per line):")
            sections = [section.strip() for section in sections_input.split("\n") if section.strip()]
            
            # Template variables
            variables_input = st.text_area("Variables (one per line, without curly braces):")
            variables = [var.strip() for var in variables_input.split("\n") if var.strip()]
            
            # Template content
            st.markdown("#### Template Content (Markdown format, use {variable_name} for variables)")
            template_content = st.text_area("Content:", height=300)
            
            if st.button("Create Template"):
                if not new_template_id or not template_name or not template_content:
                    st.error("Template ID, name, and content are required!")
                else:
                    # Create new template
                    st.session_state.document_templates[new_template_id] = {
                        "name": template_name,
                        "description": template_description,
                        "sections": sections,
                        "variables": variables,
                        "content": template_content
                    }
                    st.success(f"Template '{template_name}' created successfully!")
        
        elif template_action == "Edit Existing Template":
            if not st.session_state.document_templates:
                st.warning("No templates available to edit. Create a new template first.")
                return
                
            template_to_edit = st.selectbox(
                "Select template to edit:", 
                list(st.session_state.document_templates.keys()),
                format_func=lambda x: st.session_state.document_templates[x]["name"]
            )
            
            if template_to_edit:
                template = st.session_state.document_templates[template_to_edit]
                
                template_name = st.text_input("Template Name:", value=template["name"])
                template_description = st.text_area("Description:", value=template["description"])
                
                # Template sections
                sections_input = st.text_area(
                    "Sections (one per line):", 
                    value="\n".join(template["sections"])
                )
                sections = [section.strip() for section in sections_input.split("\n") if section.strip()]
                
                # Template variables
                variables_input = st.text_area(
                    "Variables (one per line, without curly braces):", 
                    value="\n".join(template["variables"])
                )
                variables = [var.strip() for var in variables_input.split("\n") if var.strip()]
                
                # Template content
                st.markdown("#### Template Content (Markdown format, use {variable_name} for variables)")
                template_content = st.text_area("Content:", value=template["content"], height=300)
                
                if st.button("Update Template"):
                    if not template_name or not template_content:
                        st.error("Template name and content are required!")
                    else:
                        # Update template
                        st.session_state.document_templates[template_to_edit] = {
                            "name": template_name,
                            "description": template_description,
                            "sections": sections,
                            "variables": variables,
                            "content": template_content
                        }
                        st.success(f"Template '{template_name}' updated successfully!")
    
    # Template export/import options
    st.markdown("---")
    st.subheader("Template Library Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Export Templates")
        if st.button("Export All Templates"):
            # Convert templates to JSON
            templates_json = json.dumps(st.session_state.document_templates, indent=2)
            
            # Create download button
            st.download_button(
                label="Download Templates",
                data=templates_json,
                file_name=f"document_templates_{datetime.datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
    
    with col2:
        st.markdown("### Import Templates")
        uploaded_file = st.file_uploader("Upload Templates JSON", type=["json"])
        
        if uploaded_file:
            try:
                import_action = st.radio(
                    "Import Action:", 
                    ["Merge with existing templates", "Replace all templates"]
                )
                
                if st.button("Import Templates"):
                    # Load uploaded JSON
                    templates_data = json.loads(uploaded_file.getvalue().decode())
                    
                    if import_action == "Replace all templates":
                        st.session_state.document_templates = templates_data
                        st.success(f"All templates replaced with {len(templates_data)} imported templates!")
                    else:
                        # Merge with existing templates
                        before_count = len(st.session_state.document_templates)
                        st.session_state.document_templates.update(templates_data)
                        after_count = len(st.session_state.document_templates)
                        st.success(f"Imported {after_count - before_count} new templates!")
            except Exception as e:
                st.error(f"Error importing templates: {str(e)}")