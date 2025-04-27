import streamlit as st
import pandas as pd
import os
import json
import datetime
from io import StringIO

def show_document_generator(project_data):
    """
    Display the Document Generator module.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.subheader("Project Document Generator")
    
    # Check for OpenAI API key
    if not st.session_state.openai_api_key:
        st.warning("⚠️ Please provide your OpenAI API key in the sidebar settings to enable document generation.")
        return
    
    # Document types
    document_types = {
        "status_report": "Project Status Report",
        "risk_register": "Risk Register",
        "meeting_minutes": "Meeting Minutes Template",
        "project_charter": "Project Charter",
        "communication_plan": "Communication Plan",
        "lessons_learned": "Lessons Learned Document",
        "stakeholder_register": "Stakeholder Register",
        "business_case": "Business Case",
        "project_schedule": "Project Schedule Summary",
        "resource_plan": "Resource Management Plan"
    }
    
    # Create columns for better layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Document type selection
        selected_doc_type = st.selectbox(
            "Select Document Type", 
            list(document_types.keys()),
            format_func=lambda x: document_types[x]
        )
        
        # Document customization options
        st.subheader("Document Options")
        
        if selected_doc_type == "status_report":
            report_period = st.selectbox("Reporting Period", ["Weekly", "Bi-weekly", "Monthly"])
            include_sections = st.multiselect(
                "Include Sections", 
                ["Executive Summary", "Milestone Status", "Risk Summary", "Issues Log", "Budget Status", "Resource Status", "Next Steps"],
                default=["Executive Summary", "Milestone Status", "Risk Summary", "Next Steps"]
            )
            
            custom_options = {
                "report_period": report_period,
                "include_sections": include_sections
            }
            
        elif selected_doc_type == "risk_register":
            risk_categories = st.multiselect(
                "Risk Categories", 
                ["Technical", "Schedule", "Cost", "Resource", "Scope", "Quality", "Communication", "External"],
                default=["Technical", "Schedule", "Cost", "Resource"]
            )
            
            risk_data = project_data.get('risks', [])
            include_existing = st.checkbox("Include existing risks", value=True)
            
            custom_options = {
                "risk_categories": risk_categories,
                "include_existing": include_existing,
                "existing_risks": risk_data if include_existing else []
            }
            
        elif selected_doc_type == "meeting_minutes":
            meeting_type = st.selectbox("Meeting Type", 
                                       ["Status Meeting", "Sprint Planning", "Sprint Review", 
                                        "Sprint Retrospective", "Stakeholder Meeting", "Technical Discussion"])
            
            attendees = st.text_area("Attendees (one per line)")
            meeting_date = st.date_input("Meeting Date", datetime.datetime.now())
            
            custom_options = {
                "meeting_type": meeting_type,
                "attendees": [name.strip() for name in attendees.split("\n") if name.strip()],
                "meeting_date": meeting_date.strftime("%Y-%m-%d")
            }
            
        elif selected_doc_type == "project_charter":
            objectives = st.text_area("Project Objectives (one per line)")
            scope = st.text_area("Project Scope")
            constraints = st.text_area("Constraints (one per line)")
            
            custom_options = {
                "objectives": [obj.strip() for obj in objectives.split("\n") if obj.strip()],
                "scope": scope,
                "constraints": [c.strip() for c in constraints.split("\n") if c.strip()]
            }
            
        else:
            # Generic options for other document types
            custom_options = {}
            st.info(f"Standard template will be used for {document_types[selected_doc_type]}")
        
        # Output format selection
        output_format = st.radio("Output Format", ["Markdown", "HTML", "Plain Text"])
        
        # Generate document button
        if st.button("Generate Document"):
            with st.spinner("Generating document..."):
                # Combine project data with custom options
                generation_data = {
                    "project_name": st.session_state.current_project,
                    "document_type": document_types[selected_doc_type],
                    "custom_options": custom_options,
                    "project_data": {
                        "wbs": project_data.get("wbs", []),
                        "resources": project_data.get("resources", []),
                        "risks": project_data.get("risks", []),
                        "assumptions": project_data.get("assumptions", []),
                        "issues": project_data.get("issues", []),
                        "dependencies": project_data.get("dependencies", []),
                        "decisions": project_data.get("decisions", [])
                    }
                }
                
                # Here we would call the OpenAI API to generate the document
                # For now, we'll display sample content
                document_content = generate_sample_document(selected_doc_type, generation_data, output_format)
                
                # Store the generated document in session state
                if 'generated_documents' not in st.session_state:
                    st.session_state.generated_documents = {}
                    
                doc_id = f"{selected_doc_type}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
                st.session_state.generated_documents[doc_id] = {
                    "content": document_content,
                    "type": document_types[selected_doc_type],
                    "format": output_format,
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Display success message
                st.success(f"{document_types[selected_doc_type]} generated successfully!")
    
    with col2:
        # Recent documents
        st.subheader("Recent Documents")
        
        if 'generated_documents' in st.session_state and st.session_state.generated_documents:
            for doc_id, doc_info in reversed(list(st.session_state.generated_documents.items())):
                with st.expander(f"{doc_info['type']} ({doc_info['timestamp']})"):
                    st.markdown(f"**Format:** {doc_info['format']}")
                    
                    # Add download button for each document
                    doc_content = doc_info['content']
                    file_extension = ".md" if doc_info['format'] == "Markdown" else ".html" if doc_info['format'] == "HTML" else ".txt"
                    
                    # Create a download button for the document
                    st.download_button(
                        label="Download Document",
                        data=doc_content,
                        file_name=f"{doc_id}{file_extension}",
                        mime="text/plain"
                    )
                    
                    # Show preview
                    with st.expander("Preview"):
                        if doc_info['format'] == "HTML":
                            st.code(doc_content, language="html")
                        elif doc_info['format'] == "Markdown":
                            st.code(doc_content, language="markdown")
                        else:
                            st.code(doc_content)
        else:
            st.info("No documents generated yet.")
    
    # Document content preview (displays when a document is generated)
    if 'generated_documents' in st.session_state and st.session_state.generated_documents:
        latest_doc_id = list(st.session_state.generated_documents.keys())[-1]
        latest_doc = st.session_state.generated_documents[latest_doc_id]
        
        st.subheader("Document Preview")
        
        if latest_doc['format'] == "Markdown":
            st.markdown(latest_doc['content'])
        elif latest_doc['format'] == "HTML":
            st.components.v1.html(latest_doc['content'], height=500)
        else:
            st.text(latest_doc['content'])

def generate_sample_document(doc_type, data, output_format):
    """
    Generate a sample document based on the document type and project data.
    In a real implementation, this would call the OpenAI API.
    
    Args:
        doc_type: Type of document to generate
        data: Project and custom data for generation
        output_format: Desired output format (Markdown, HTML, or Plain Text)
        
    Returns:
        String containing the document content
    """
    project_name = data['project_name']
    custom_options = data['custom_options']
    
    # For status report
    if doc_type == "status_report":
        report_period = custom_options.get('report_period', 'Weekly')
        sections = custom_options.get('include_sections', [])
        
        # Generate based on Markdown format initially
        content = f"# {project_name} - {report_period} Status Report\n\n"
        content += f"**Date:** {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n"
        
        if "Executive Summary" in sections:
            content += "## Executive Summary\n\n"
            content += "The project is currently on track with all major milestones being met according to the timeline. "
            content += "Team performance has been strong, with effective collaboration across departments. "
            content += "Some minor risks have been identified and are being actively monitored.\n\n"
        
        if "Milestone Status" in sections:
            content += "## Milestone Status\n\n"
            content += "| Milestone | Due Date | Status | Comments |\n"
            content += "|-----------|----------|--------|----------|\n"
            content += "| Requirements Gathering | 2025-03-15 | Completed | All requirements documented and approved |\n"
            content += "| Design Phase | 2025-04-10 | Completed | Design documents signed off |\n"
            content += "| Development Sprint 1 | 2025-04-30 | In Progress | 75% complete, on track |\n"
            content += "| Testing Phase | 2025-05-15 | Not Started | Test cases in preparation |\n\n"
        
        if "Risk Summary" in sections:
            content += "## Risk Summary\n\n"
            content += "### Top Risks\n\n"
            content += "1. **Resource Availability**: Team members may be pulled into other high-priority projects\n"
            content += "   - **Mitigation**: Cross-training team members and documenting processes\n\n"
            content += "2. **Technology Integration**: New API may not meet performance requirements\n"
            content += "   - **Mitigation**: Early performance testing and backup plan implementation\n\n"
        
        if "Next Steps" in sections:
            content += "## Next Steps\n\n"
            content += "1. Complete Development Sprint 1 by April 30\n"
            content += "2. Begin Development Sprint 2 on May 1\n"
            content += "3. Conduct mid-project review with stakeholders on May 5\n"
            content += "4. Prepare testing environment by May 10\n\n"
            
    # For risk register
    elif doc_type == "risk_register":
        risk_categories = custom_options.get('risk_categories', [])
        existing_risks = custom_options.get('existing_risks', [])
        
        content = f"# {project_name} - Risk Register\n\n"
        content += f"**Date:** {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n"
        content += "## Risk Categories\n\n"
        
        for category in risk_categories:
            content += f"- {category}\n"
        
        content += "\n## Identified Risks\n\n"
        content += "| ID | Risk Description | Category | Severity | Probability | Impact | Mitigation Strategy | Owner | Status |\n"
        content += "|----|--------------------|----------|----------|------------|--------|---------------------|-------|--------|\n"
        
        # Include existing risks if available
        if existing_risks:
            for i, risk in enumerate(existing_risks):
                content += f"| R{i+1} | {risk.get('description', 'N/A')} | {risk.get('category', 'N/A')} | "
                content += f"{risk.get('severity', 'Medium')} | {risk.get('probability', 'Medium')} | "
                content += f"{risk.get('impact', 'Medium')} | {risk.get('mitigation', 'TBD')} | "
                content += f"{risk.get('owner', 'TBD')} | {risk.get('status', 'Open')} |\n"
        else:
            # Sample risk entries
            content += "| R1 | Vendor delays in delivering critical components | External | High | Medium | High | "
            content += "Identify backup vendors and maintain buffer stock | Procurement Team | Open |\n"
            content += "| R2 | Key team member leaving during critical phase | Resource | Medium | Low | High | "
            content += "Cross-training and documentation | Project Manager | Open |\n"
            content += "| R3 | Scope creep due to evolving requirements | Scope | Medium | High | Medium | "
            content += "Strict change control process | Project Manager | Open |\n"
        
        content += "\n## Risk Assessment Matrix\n\n"
        content += "```\n"
        content += "     │ Low Impact │ Med Impact │ High Impact │\n"
        content += "─────┼────────────┼────────────┼─────────────┤\n"
        content += "High │            │            │      R1     │\n"
        content += "Prob │            │     R3     │             │\n"
        content += "─────┼────────────┼────────────┼─────────────┤\n"
        content += "Med  │            │            │             │\n"
        content += "Prob │            │            │      R1     │\n"
        content += "─────┼────────────┼────────────┼─────────────┤\n"
        content += "Low  │            │            │             │\n"
        content += "Prob │            │            │      R2     │\n"
        content += "```\n"
    
    # For meeting minutes
    elif doc_type == "meeting_minutes":
        meeting_type = custom_options.get('meeting_type', 'Status Meeting')
        attendees = custom_options.get('attendees', [])
        meeting_date = custom_options.get('meeting_date', datetime.datetime.now().strftime("%Y-%m-%d"))
        
        content = f"# {project_name} - {meeting_type} Minutes\n\n"
        content += f"**Date:** {meeting_date}\n\n"
        
        content += "## Attendees\n\n"
        if attendees:
            for attendee in attendees:
                content += f"- {attendee}\n"
        else:
            content += "- [List of attendees]\n"
        content += "\n"
        
        content += "## Agenda\n\n"
        content += "1. Review of previous action items\n"
        content += "2. Project status update\n"
        content += "3. Discussion of current challenges\n"
        content += "4. Next steps and action items\n\n"
        
        content += "## Discussion Points\n\n"
        content += "### 1. Review of Previous Action Items\n\n"
        content += "- Action 1: [Status and updates]\n"
        content += "- Action 2: [Status and updates]\n\n"
        
        content += "### 2. Project Status Update\n\n"
        content += "- Current progress: [Details]\n"
        content += "- Timeline status: [On track/Behind/Ahead]\n"
        content += "- Budget status: [Within budget/Over budget/Under budget]\n\n"
        
        content += "### 3. Discussion of Current Challenges\n\n"
        content += "- Challenge 1: [Details]\n"
        content += "  - Proposed solution: [Details]\n"
        content += "- Challenge 2: [Details]\n"
        content += "  - Proposed solution: [Details]\n\n"
        
        content += "## Action Items\n\n"
        content += "| Action | Owner | Due Date | Status |\n"
        content += "|--------|-------|----------|--------|\n"
        content += "| [Action 1] | [Owner] | [Date] | New |\n"
        content += "| [Action 2] | [Owner] | [Date] | New |\n\n"
        
        content += "## Next Meeting\n\n"
        content += "- Date: [Next meeting date]\n"
        content += "- Time: [Time]\n"
        content += "- Location: [Location/Virtual link]\n"
    
    # For project charter
    elif doc_type == "project_charter":
        objectives = custom_options.get('objectives', [])
        scope = custom_options.get('scope', '')
        constraints = custom_options.get('constraints', [])
        
        content = f"# {project_name} - Project Charter\n\n"
        content += f"**Date:** {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n"
        
        content += "## Project Overview\n\n"
        content += "This document defines the purpose, objectives, scope, and structure of the project.\n\n"
        
        content += "## Project Objectives\n\n"
        if objectives:
            for i, objective in enumerate(objectives):
                content += f"{i+1}. {objective}\n"
        else:
            content += "- [List objectives here]\n"
        content += "\n"
        
        content += "## Project Scope\n\n"
        if scope:
            content += scope + "\n\n"
        else:
            content += "[Define project scope here]\n\n"
        
        content += "## Project Constraints\n\n"
        if constraints:
            for constraint in constraints:
                content += f"- {constraint}\n"
        else:
            content += "- [List constraints here]\n"
        content += "\n"
        
        content += "## Stakeholders\n\n"
        content += "| Role | Name | Department | Responsibilities |\n"
        content += "|------|------|------------|------------------|\n"
        content += "| Project Sponsor | [Name] | [Department] | [Responsibilities] |\n"
        content += "| Project Manager | [Name] | [Department] | [Responsibilities] |\n"
        content += "| Team Member | [Name] | [Department] | [Responsibilities] |\n\n"
        
        content += "## Timeline\n\n"
        content += "| Phase | Start Date | End Date | Deliverables |\n"
        content += "|-------|------------|----------|-------------|\n"
        content += "| Initiation | [Date] | [Date] | [Deliverables] |\n"
        content += "| Planning | [Date] | [Date] | [Deliverables] |\n"
        content += "| Execution | [Date] | [Date] | [Deliverables] |\n"
        content += "| Closure | [Date] | [Date] | [Deliverables] |\n\n"
        
        content += "## Budget\n\n"
        content += "| Category | Amount | Notes |\n"
        content += "|----------|--------|-------|\n"
        content += "| Personnel | $[Amount] | [Notes] |\n"
        content += "| Equipment | $[Amount] | [Notes] |\n"
        content += "| Software | $[Amount] | [Notes] |\n"
        content += "| Contingency | $[Amount] | [Notes] |\n"
        content += "| **Total** | $[Total Amount] | |\n\n"
        
        content += "## Approval\n\n"
        content += "| Role | Name | Signature | Date |\n"
        content += "|------|------|-----------|------|\n"
        content += "| Project Sponsor | [Name] | | |\n"
        content += "| Project Manager | [Name] | | |\n"
    
    # For other document types (generic template)
    else:
        content = f"# {project_name} - {data['document_type']}\n\n"
        content += f"**Date:** {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n"
        content += f"**Generated By:** AI PM Buddy v2.0\n\n"
        content += "## Document Content\n\n"
        content += "This is a placeholder for the document content. In the actual implementation, "
        content += "this would be generated by the OpenAI API based on your project data and "
        content += "specific document requirements.\n\n"
        content += "The document would include relevant sections and information tailored to your "
        content += f"project and the specific {data['document_type']} format.\n\n"
    
    # Convert to the desired output format
    if output_format == "HTML":
        # Convert markdown to HTML (this is a simple placeholder - actual implementation would use a proper converter)
        # Create the HTML template first
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{project_name} - {data['document_type']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; }}
                h1 {{ color: #4CAF50; }}
                h2 {{ color: #2E7D32; border-bottom: 1px solid #ddd; padding-bottom: 5px; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            CONTENT_PLACEHOLDER
        </body>
        </html>
        """
        
        # Apply replacements to content separately
        processed_content = content
        replacements = [
            ('# ', '<h1>'),
            ('\n\n## ', '</h1>\n\n<h2>'),
            ('\n\n', '</p><p>'),
            ('- ', '<li>'),
            ('\n-', '\n<li>'),
            ('|', '</td><td>'),
            ('\n|', '</tr>\n<tr><td>'),
            ('```', '<pre>'),
            ('**', '<strong>'),
            ('*', '<em>')
        ]
        
        for old, new in replacements:
            processed_content = processed_content.replace(old, new)
            
        # Insert processed content into the HTML template
        html_content = html_template.replace('CONTENT_PLACEHOLDER', processed_content)
        return html_content
    
    elif output_format == "Plain Text":
        # Convert markdown to plain text
        plain_text = content.replace('# ', '\n').replace('## ', '\n').replace('### ', '\n')
        plain_text = plain_text.replace('**', '').replace('*', '')
        plain_text = plain_text.replace('```', '').replace('|', '\t')
        return plain_text
    
    else:  # Markdown is the default
        return content