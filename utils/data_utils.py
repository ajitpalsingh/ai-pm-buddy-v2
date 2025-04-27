import pandas as pd
import numpy as np
import json
import os
import streamlit as st
import datetime

def load_sample_data():
    """
    Create a sample project data structure.
    Returns:
        dict: Sample project data
    """
    today = datetime.datetime.now()
    
    # Load multiple sample projects into session state
    if 'project_data' not in st.session_state:
        st.session_state.project_data = {}
    
    if 'Sample Project' not in st.session_state.project_data:
        st.session_state.project_data['Sample Project'] = generate_sample_project_1(today)
    
    if 'Enterprise Software Implementation' not in st.session_state.project_data:
        st.session_state.project_data['Enterprise Software Implementation'] = generate_sample_project_2(today)
    
    return generate_sample_project_1(today)

def generate_sample_project_1(today):
    """
    Generate the first sample project data (Generic IT Project).
    
    Args:
        today: Current date
        
    Returns:
        dict: Sample project data
    """
    
    # Create WBS (Work Breakdown Structure) data
    wbs = [
        {
            "id": 1,
            "task": "Project Initiation",
            "description": "Initial project setup and planning",
            "start_date": (today - datetime.timedelta(days=30)).strftime("%Y-%m-%d"),
            "end_date": (today - datetime.timedelta(days=20)).strftime("%Y-%m-%d"),
            "duration": 10,
            "progress": 100,
            "assigned_to": "John Smith",
            "dependencies": [],
            "critical": True
        },
        {
            "id": 2,
            "task": "Stakeholder Analysis",
            "description": "Identify key stakeholders and their requirements",
            "start_date": (today - datetime.timedelta(days=25)).strftime("%Y-%m-%d"),
            "end_date": (today - datetime.timedelta(days=18)).strftime("%Y-%m-%d"),
            "duration": 7,
            "progress": 100,
            "assigned_to": "John Smith",
            "dependencies": [1],
            "critical": False
        },
        {
            "id": 3,
            "task": "Requirements Gathering",
            "description": "Collect and document project requirements",
            "start_date": (today - datetime.timedelta(days=20)).strftime("%Y-%m-%d"),
            "end_date": (today - datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
            "duration": 15,
            "progress": 90,
            "assigned_to": "Sarah Johnson",
            "dependencies": [1],
            "critical": True
        },
        {
            "id": 4,
            "task": "Requirements Approval",
            "description": "Get sign-off on requirements from key stakeholders",
            "start_date": (today - datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
            "end_date": (today).strftime("%Y-%m-%d"),
            "duration": 5,
            "progress": 70,
            "assigned_to": "John Smith",
            "dependencies": [3],
            "critical": True
        },
        {
            "id": 5,
            "task": "Design Phase",
            "description": "System architecture and design",
            "start_date": (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=15)).strftime("%Y-%m-%d"),
            "duration": 15,
            "progress": 0,
            "assigned_to": "Mike Williams",
            "dependencies": [4],
            "critical": True
        },
        {
            "id": 6,
            "task": "Database Design",
            "description": "Design database schema and relationships",
            "start_date": (today + datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=12)).strftime("%Y-%m-%d"),
            "duration": 7,
            "progress": 0,
            "assigned_to": "Database Team",
            "dependencies": [5],
            "critical": True
        },
        {
            "id": 7,
            "task": "UI/UX Design",
            "description": "Create user interface mockups and user experience flows",
            "start_date": (today + datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=15)).strftime("%Y-%m-%d"),
            "duration": 10,
            "progress": 0,
            "assigned_to": "Design Team",
            "dependencies": [5],
            "critical": False
        },
        {
            "id": 8,
            "task": "Design Review",
            "description": "Review and approve design documents",
            "start_date": (today + datetime.timedelta(days=16)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=18)).strftime("%Y-%m-%d"),
            "duration": 3,
            "progress": 0,
            "assigned_to": "John Smith",
            "dependencies": [5, 6, 7],
            "critical": True
        },
        {
            "id": 9,
            "task": "Development Sprint 1",
            "description": "First development iteration",
            "start_date": (today + datetime.timedelta(days=19)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=32)).strftime("%Y-%m-%d"),
            "duration": 14,
            "progress": 0,
            "assigned_to": "Dev Team",
            "dependencies": [8],
            "critical": True
        },
        {
            "id": 10,
            "task": "Development Sprint 2",
            "description": "Second development iteration",
            "start_date": (today + datetime.timedelta(days=33)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=46)).strftime("%Y-%m-%d"),
            "duration": 14,
            "progress": 0,
            "assigned_to": "Dev Team",
            "dependencies": [9],
            "critical": True
        },
        {
            "id": 11,
            "task": "Quality Assurance Planning",
            "description": "Prepare test plans and test cases",
            "start_date": (today + datetime.timedelta(days=10)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=20)).strftime("%Y-%m-%d"),
            "duration": 10,
            "progress": 0,
            "assigned_to": "QA Team",
            "dependencies": [5],
            "critical": False
        },
        {
            "id": 12,
            "task": "User Acceptance Testing Setup",
            "description": "Prepare UAT environment and test scenarios",
            "start_date": (today + datetime.timedelta(days=20)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=27)).strftime("%Y-%m-%d"),
            "duration": 7,
            "progress": 0,
            "assigned_to": "QA Team",
            "dependencies": [11],
            "critical": False
        },
        {
            "id": 13,
            "task": "Testing Sprint 1",
            "description": "Test deliverables from first development sprint",
            "start_date": (today + datetime.timedelta(days=33)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=39)).strftime("%Y-%m-%d"),
            "duration": 7,
            "progress": 0,
            "assigned_to": "QA Team",
            "dependencies": [9, 11],
            "critical": True
        },
        {
            "id": 14,
            "task": "Bug Fixes Sprint 1",
            "description": "Fix issues found during first testing sprint",
            "start_date": (today + datetime.timedelta(days=40)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=46)).strftime("%Y-%m-%d"),
            "duration": 7,
            "progress": 0,
            "assigned_to": "Dev Team",
            "dependencies": [13],
            "critical": True
        },
        {
            "id": 15,
            "task": "User Acceptance Testing",
            "description": "Conduct UAT with key stakeholders",
            "start_date": (today + datetime.timedelta(days=47)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=54)).strftime("%Y-%m-%d"),
            "duration": 8,
            "progress": 0,
            "assigned_to": "QA Team",
            "dependencies": [14, 12],
            "critical": True
        },
        {
            "id": 16,
            "task": "Deployment Planning",
            "description": "Create deployment strategy and rollback plan",
            "start_date": (today + datetime.timedelta(days=35)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=42)).strftime("%Y-%m-%d"),
            "duration": 8,
            "progress": 0,
            "assigned_to": "Mike Williams",
            "dependencies": [8],
            "critical": False
        },
        {
            "id": 17,
            "task": "Deployment",
            "description": "Deploy application to production",
            "start_date": (today + datetime.timedelta(days=55)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=57)).strftime("%Y-%m-%d"),
            "duration": 3,
            "progress": 0,
            "assigned_to": "Dev Team",
            "dependencies": [15, 16],
            "critical": True
        },
        {
            "id": 18,
            "task": "Post-Implementation Review",
            "description": "Evaluate project success and document lessons learned",
            "start_date": (today + datetime.timedelta(days=58)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=62)).strftime("%Y-%m-%d"),
            "duration": 5,
            "progress": 0,
            "assigned_to": "John Smith",
            "dependencies": [17],
            "critical": False
        }
    ]
    
    # Create resource data
    resources = [
        {
            "name": "John Smith",
            "role": "Project Manager",
            "availability": 100,
            "allocated": 85,
            "skills": ["Project Management", "Risk Management", "Stakeholder Management"]
        },
        {
            "name": "Sarah Johnson",
            "role": "Business Analyst",
            "availability": 100,
            "allocated": 110,
            "skills": ["Requirements Analysis", "Process Modeling", "User Story Writing", "User Research"]
        },
        {
            "name": "Mike Williams",
            "role": "Solution Architect",
            "availability": 80,
            "allocated": 95,
            "skills": ["System Design", "Technical Documentation", "Integration", "Cloud Architecture"]
        },
        {
            "name": "Emily Chen",
            "role": "UX Designer",
            "availability": 100,
            "allocated": 70,
            "skills": ["User Interface Design", "User Experience", "Wireframing", "Prototyping"]
        },
        {
            "name": "Raj Patel",
            "role": "Senior Developer",
            "availability": 100,
            "allocated": 120,
            "skills": ["Frontend Development", "Backend Development", "Database Design", "API Development"]
        },
        {
            "name": "Database Team",
            "role": "Database Specialists",
            "availability": 200,
            "allocated": 150,
            "skills": ["Database Design", "SQL Development", "Data Modeling", "Performance Tuning"]
        },
        {
            "name": "Design Team",
            "role": "UI/UX Team",
            "availability": 200,
            "allocated": 160,
            "skills": ["UI Design", "UX Design", "Visual Design", "User Research"]
        },
        {
            "name": "Dev Team",
            "role": "Development Team",
            "availability": 500,
            "allocated": 480,
            "skills": ["Programming", "Testing", "Documentation", "DevOps"]
        },
        {
            "name": "QA Team",
            "role": "Quality Assurance",
            "availability": 300,
            "allocated": 260,
            "skills": ["Test Planning", "Test Execution", "Defect Management", "Automation Testing"]
        },
        {
            "name": "Alex Thompson",
            "role": "DevOps Engineer",
            "availability": 100,
            "allocated": 60,
            "skills": ["CI/CD", "Deployment Automation", "Infrastructure as Code", "Cloud Services"]
        }
    ]
    
    # Create RAID (Risks, Assumptions, Issues, Dependencies) data
    raid = {
        "risks": [
            {
                "id": 1,
                "description": "Key technical lead may be unavailable during critical phase",
                "impact": "High",
                "probability": "Medium",
                "mitigation": "Cross-train another team member to serve as backup",
                "owner": "John Smith",
                "status": "Open"
            },
            {
                "id": 2,
                "description": "Requirements may change significantly after design phase",
                "impact": "High",
                "probability": "Medium",
                "mitigation": "Implement change control process, include buffer in schedule",
                "owner": "Sarah Johnson",
                "status": "Open"
            },
            {
                "id": 3,
                "description": "Integration with third-party API may have unexpected issues",
                "impact": "High",
                "probability": "High",
                "mitigation": "Early prototype development and testing with third-party system",
                "owner": "Mike Williams",
                "status": "Mitigated"
            },
            {
                "id": 4,
                "description": "Performance may not meet SLA requirements",
                "impact": "Medium",
                "probability": "Low",
                "mitigation": "Performance testing early in development, infrastructure scalability planning",
                "owner": "Dev Team",
                "status": "Open"
            },
            {
                "id": 5,
                "description": "Security vulnerabilities may be discovered late in development",
                "impact": "High",
                "probability": "Medium",
                "mitigation": "Regular security reviews and penetration testing",
                "owner": "QA Team",
                "status": "Open"
            },
            {
                "id": 6,
                "description": "Budget constraints may limit resources in later phases",
                "impact": "Medium",
                "probability": "Medium",
                "mitigation": "Regular budget tracking, prioritization of features",
                "owner": "John Smith",
                "status": "Open"
            }
        ],
        "assumptions": [
            {
                "id": 1,
                "description": "All stakeholders will be available for meetings as scheduled",
                "impact": "Medium",
                "owner": "John Smith",
                "validation": "Pending"
            },
            {
                "id": 2,
                "description": "Existing systems have accurate documentation",
                "impact": "High",
                "owner": "Mike Williams",
                "validation": "Validated"
            },
            {
                "id": 3,
                "description": "Current infrastructure can support the new application",
                "impact": "High",
                "owner": "Mike Williams",
                "validation": "Invalidated"
            },
            {
                "id": 4,
                "description": "Users have basic technical proficiency",
                "impact": "Medium",
                "owner": "Sarah Johnson",
                "validation": "Validated"
            },
            {
                "id": 5,
                "description": "Compliance requirements will not change during the project",
                "impact": "High",
                "owner": "John Smith",
                "validation": "Pending"
            }
        ],
        "issues": [
            {
                "id": 1,
                "description": "Development environment setup delayed",
                "impact": "Medium",
                "raised_date": (today - datetime.timedelta(days=15)).strftime("%Y-%m-%d"),
                "owner": "Mike Williams",
                "resolution": "Working with IT to expedite setup",
                "status": "Resolved"
            },
            {
                "id": 2,
                "description": "Key stakeholder unavailable for requirements approval",
                "impact": "High",
                "raised_date": (today - datetime.timedelta(days=7)).strftime("%Y-%m-%d"),
                "owner": "John Smith",
                "resolution": "Escalated to executive sponsor",
                "status": "In Progress"
            },
            {
                "id": 3,
                "description": "Licensing costs higher than budgeted",
                "impact": "Medium",
                "raised_date": (today - datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
                "owner": "John Smith",
                "resolution": "Negotiating with vendor for discount",
                "status": "In Progress"
            },
            {
                "id": 4,
                "description": "Technical debt in existing system affecting integration",
                "impact": "High",
                "raised_date": (today - datetime.timedelta(days=2)).strftime("%Y-%m-%d"),
                "owner": "Dev Team",
                "resolution": "Identifying critical refactoring needs",
                "status": "Open"
            }
        ],
        "dependencies": [
            {
                "id": 1,
                "description": "Integration with legacy system requires IT support",
                "depends_on": "IT Department",
                "impact": "High",
                "due_date": (today + datetime.timedelta(days=15)).strftime("%Y-%m-%d"),
                "status": "Not Started"
            },
            {
                "id": 2,
                "description": "UX approval needed from marketing department",
                "depends_on": "Marketing",
                "impact": "Medium",
                "due_date": (today + datetime.timedelta(days=20)).strftime("%Y-%m-%d"),
                "status": "In Progress"
            },
            {
                "id": 3,
                "description": "Cloud infrastructure provisioning by IT operations",
                "depends_on": "IT Operations",
                "impact": "High",
                "due_date": (today + datetime.timedelta(days=25)).strftime("%Y-%m-%d"),
                "status": "Not Started"
            },
            {
                "id": 4,
                "description": "Legal approval of terms and conditions",
                "depends_on": "Legal Department",
                "impact": "Medium",
                "due_date": (today + datetime.timedelta(days=10)).strftime("%Y-%m-%d"),
                "status": "At Risk"
            }
        ]
    }
    
    # Create decision log
    decisions = [
        {
            "id": 1,
            "description": "Use cloud-based infrastructure instead of on-premises",
            "rationale": "Better scalability and reduced maintenance overhead",
            "decision_date": (today - datetime.timedelta(days=25)).strftime("%Y-%m-%d"),
            "decided_by": "Project Board",
            "impact": "High",
            "status": "Approved"
        },
        {
            "id": 2,
            "description": "Implement phased delivery approach",
            "rationale": "Allows for earlier feedback and risk mitigation",
            "decision_date": (today - datetime.timedelta(days=22)).strftime("%Y-%m-%d"),
            "decided_by": "Project Manager",
            "impact": "Medium",
            "status": "Approved"
        },
        {
            "id": 3,
            "description": "Use React for frontend development",
            "rationale": "Existing team expertise and component reusability",
            "decision_date": (today - datetime.timedelta(days=18)).strftime("%Y-%m-%d"),
            "decided_by": "Technical Team",
            "impact": "Medium",
            "status": "Approved"
        },
        {
            "id": 4,
            "description": "Implement additional security layer",
            "rationale": "Increased protection for sensitive data",
            "decision_date": (today - datetime.timedelta(days=12)).strftime("%Y-%m-%d"),
            "decided_by": "Security Team",
            "impact": "High",
            "status": "Approved"
        },
        {
            "id": 5,
            "description": "Outsource mobile app development",
            "rationale": "Lack of in-house expertise and tight timeline",
            "decision_date": (today - datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
            "decided_by": "Project Board",
            "impact": "High",
            "status": "Pending Approval"
        },
        {
            "id": 6,
            "description": "Switch to microservices architecture",
            "rationale": "Better scalability and team autonomy",
            "decision_date": (today - datetime.timedelta(days=3)).strftime("%Y-%m-%d"),
            "decided_by": "Architecture Team",
            "impact": "High",
            "status": "Rejected"
        },
        {
            "id": 7,
            "description": "Add feature for real-time notifications",
            "rationale": "Enhanced user experience and engagement",
            "decision_date": (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            "decided_by": "Product Owner",
            "impact": "Medium",
            "status": "Under Review"
        }
    ]
    
    # Create team feedback for sentiment analysis
    team_feedback = [
        "The project scope is well-defined and I'm clear on my tasks.",
        "Communication has been good so far, but we need more regular updates from management.",
        "I'm concerned about the tight timeline for the development phase. We might need more resources.",
        "The requirements documentation is excellent and very helpful for understanding the project goals.",
        "Team morale is high but we're worried about potential scope creep affecting our work-life balance.",
        "The new project management tool has been a great improvement for tracking our tasks.",
        "I find the daily stand-ups effective, but some team members are consistently late.",
        "Working with the design team has been challenging due to conflicting priorities.",
        "The technical documentation is incomplete which is slowing down our development efforts.",
        "Our team lead has been very supportive and helps remove blockers quickly.",
        "The client keeps changing requirements which is frustrating and causes rework.",
        "I appreciate the clear decision-making process we have in place for this project.",
        "The development environment issues have been resolved but it took too long.",
        "We need more cross-team collaboration to ensure all components integrate well.",
        "The weekly demos are valuable for getting stakeholder feedback early.",
        "I'm excited about the technologies we're using and learning new skills.",
        "There seems to be a lack of clarity around the long-term project vision.",
        "The project has good momentum but I'm worried about sustaining it for the duration.",
        "Our testing processes are too manual and time-consuming.",
        "I think we need to improve our estimation process as tasks often take longer than expected."
    ]
    
    # Create baseline WBS for scope creep detection (fewer tasks than current WBS)
    baseline_wbs = [
        {
            "id": 1,
            "task": "Project Initiation",
            "description": "Initial project setup and planning",
            "start_date": (today - datetime.timedelta(days=30)).strftime("%Y-%m-%d"),
            "end_date": (today - datetime.timedelta(days=20)).strftime("%Y-%m-%d"),
            "duration": 10,
            "progress": 100,
            "assigned_to": "John Smith",
            "dependencies": [],
            "critical": True
        },
        {
            "id": 2,
            "task": "Requirements Gathering",
            "description": "Collect and document project requirements",
            "start_date": (today - datetime.timedelta(days=20)).strftime("%Y-%m-%d"),
            "end_date": (today - datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
            "duration": 15,
            "progress": 90,
            "assigned_to": "Sarah Johnson",
            "dependencies": [1],
            "critical": True
        },
        {
            "id": 3,
            "task": "Design Phase",
            "description": "System architecture and design",
            "start_date": (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=15)).strftime("%Y-%m-%d"),
            "duration": 15,
            "progress": 0,
            "assigned_to": "Mike Williams",
            "dependencies": [2],
            "critical": True
        },
        {
            "id": 4,
            "task": "Development",
            "description": "Build the application",
            "start_date": (today + datetime.timedelta(days=16)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=46)).strftime("%Y-%m-%d"),
            "duration": 30,
            "progress": 0,
            "assigned_to": "Dev Team",
            "dependencies": [3],
            "critical": True
        },
        {
            "id": 5,
            "task": "Testing",
            "description": "Test the application",
            "start_date": (today + datetime.timedelta(days=47)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=54)).strftime("%Y-%m-%d"),
            "duration": 8,
            "progress": 0,
            "assigned_to": "QA Team",
            "dependencies": [4],
            "critical": True
        },
        {
            "id": 6,
            "task": "Deployment",
            "description": "Deploy application to production",
            "start_date": (today + datetime.timedelta(days=55)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=57)).strftime("%Y-%m-%d"),
            "duration": 3,
            "progress": 0,
            "assigned_to": "Dev Team",
            "dependencies": [5],
            "critical": True
        }
    ]
    
    # Return complete project data structure
    return {
        "wbs": wbs,
        "resources": resources,
        "raid": raid,
        "decisions": decisions,
        "team_feedback": team_feedback,
        "baseline_wbs": baseline_wbs  # For scope creep detection - simpler original plan
    }

def save_data(project_data):
    """
    Save project data to session state.
    This function would typically save to a database, but for this app we'll use session state.
    
    Args:
        project_data: Dictionary of project data
    """
    st.session_state.project_data = project_data

def load_agile_knowledge():
    """
    Load Agile knowledge data from CSV or create if it doesn't exist.
    
    Returns:
        DataFrame: Agile knowledge data
    """
    try:
        return pd.read_csv('data/agile_knowledge.csv')
    except:
        # Create default agile knowledge data
        data = {
            'topic': [
                'Scrum', 'Scrum', 'Scrum', 'Kanban', 'Kanban',
                'Agile Principles', 'Agile Principles', 'Sprint Planning', 'Daily Standup', 'Retrospective'
            ],
            'question': [
                'What is Scrum?', 'What are the key roles in Scrum?', 'What are Scrum ceremonies?',
                'What is Kanban?', 'What are WIP limits?',
                'What are the key Agile principles?', 'What is the Agile Manifesto?',
                'How should Sprint Planning be conducted?', 'What is the purpose of Daily Standup?',
                'How to run an effective Retrospective?'
            ],
            'answer': [
                'Scrum is an agile framework for managing complex work, emphasizing teamwork, accountability and iterative progress toward a well-defined goal.',
                'The key roles in Scrum are: 1) Product Owner - represents the stakeholders, 2) Scrum Master - removes impediments and facilitates the process, 3) Development Team - cross-functional team that delivers the work.',
                'Scrum ceremonies include: Sprint Planning, Daily Standup, Sprint Review, Sprint Retrospective, and Backlog Refinement.',
                'Kanban is a visual method for managing workflow that emphasizes continuous delivery while not overloading team members. It visualizes work, limits work in progress, and maximizes flow.',
                'WIP (Work In Progress) limits restrict the number of items in progress at any one time. They help prevent bottlenecks, reduce context switching, and increase flow efficiency.',
                'Key Agile principles include: customer satisfaction, embracing change, frequent delivery, collaboration, motivated individuals, face-to-face communication, working software as progress measure, sustainable development, technical excellence, simplicity, self-organizing teams, and regular reflection.',
                'The Agile Manifesto values: Individuals and interactions over processes and tools, Working software over comprehensive documentation, Customer collaboration over contract negotiation, Responding to change over following a plan.',
                'Sprint Planning should: 1) Set a clear sprint goal, 2) Select items from the backlog to achieve that goal, 3) Break down items into tasks, 4) Estimate effort, 5) Commit as a team to the sprint backlog.',
                'The Daily Standup (or Daily Scrum) is a 15-minute time-boxed event where each team member answers: 1) What did I do yesterday? 2) What will I do today? 3) Are there any impediments in my way? It promotes team communication and identifies blockers quickly.',
                'Effective retrospectives should: 1) Create a safe environment, 2) Focus on improvement not blame, 3) Discuss what went well, what didn\'t, and what could be improved, 4) Result in actionable items, 5) Follow up on previous retro action items.'
            ]
        }
        df = pd.DataFrame(data)
        df.to_csv('data/agile_knowledge.csv', index=False)
        return df

def load_pm_knowledge():
    """
    Load Project Management knowledge data from CSV or create if it doesn't exist.
    
    Returns:
        DataFrame: PM knowledge data
    """
    try:
        return pd.read_csv('data/pm_knowledge.csv')
    except:
        # Create default PM knowledge data
        data = {
            'area': [
                'Project Initiation', 'Project Initiation', 'Project Planning',
                'Project Planning', 'Project Execution', 'Project Execution',
                'Project Monitoring', 'Project Monitoring', 'Project Closure',
                'Project Closure'
            ],
            'topic': [
                'Project Charter', 'Business Case', 'Work Breakdown Structure',
                'Risk Management', 'Team Management', 'Communication',
                'Earned Value Management', 'Change Control', 'Lessons Learned',
                'Project Handover'
            ],
            'guidance': [
                'The Project Charter formally authorizes the project and provides the PM with authority to apply resources. It should include: project purpose, objectives, high-level requirements, assumptions, constraints, risks, stakeholders, milestones, and budget summary.',
                'The Business Case justifies the project investment and should demonstrate: strategic alignment, problem statement, cost-benefit analysis, alternatives considered, and success criteria.',
                'The WBS decomposes project deliverables into smaller, manageable components. Create a WBS by: identifying major deliverables, decomposing to appropriate level, assigning identifiers, verifying decomposition is sufficient.',
                'Risk Management involves identifying, analyzing, responding to, and monitoring risks. Key steps: risk identification, qualitative/quantitative analysis, response planning, implementation, and monitoring.',
                'Effective team management includes: clear role definition, RACI matrix development, team building activities, conflict resolution protocols, performance feedback, and recognition systems.',
                'Project communication should be planned via a Communication Management Plan including: stakeholder communication requirements, information to be communicated, frequency, methods, responsible parties, and escalation paths.',
                'EVM integrates scope, schedule, and cost measurement using metrics like: Planned Value (PV), Earned Value (EV), Actual Cost (AC), Schedule Variance (SV), Cost Variance (CV), CPI, and SPI.',
                'Change control requires a formal process including: change request submission, impact assessment, change board review, approval/rejection, implementation, and documentation.',
                'Lessons Learned should capture: what went well, what could be improved, recommendations, and knowledge gained. Conduct sessions throughout the project, not just at closure.',
                'Project Handover requires: finalized documentation, formal acceptance, transition plan, support arrangements, warranty information, and final project report.'
            ]
        }
        df = pd.DataFrame(data)
        df.to_csv('data/pm_knowledge.csv', index=False)
        return df
        
def generate_sample_project_2(today):
    """
    Generate the second sample project data (Enterprise Software Implementation).
    
    Args:
        today: Current date
        
    Returns:
        dict: Sample project data for Enterprise Software Implementation
    """
    # Create WBS (Work Breakdown Structure) data for Enterprise Software Implementation
    wbs = [
        {
            "id": 1,
            "task": "Project Charter Approval",
            "description": "Finalize and approve project charter with executive sponsors",
            "start_date": (today - datetime.timedelta(days=45)).strftime("%Y-%m-%d"),
            "end_date": (today - datetime.timedelta(days=30)).strftime("%Y-%m-%d"),
            "duration": 15,
            "progress": 100,
            "assigned_to": "Maria Rodriguez",
            "dependencies": [],
            "critical": True
        },
        {
            "id": 2,
            "task": "Vendor Selection",
            "description": "Evaluate and select software vendor through RFP process",
            "start_date": (today - datetime.timedelta(days=60)).strftime("%Y-%m-%d"),
            "end_date": (today - datetime.timedelta(days=40)).strftime("%Y-%m-%d"),
            "duration": 20,
            "progress": 100,
            "assigned_to": "Procurement Team",
            "dependencies": [],
            "critical": True
        },
        {
            "id": 3,
            "task": "Contract Negotiation",
            "description": "Finalize contract terms with selected vendor",
            "start_date": (today - datetime.timedelta(days=39)).strftime("%Y-%m-%d"),
            "end_date": (today - datetime.timedelta(days=25)).strftime("%Y-%m-%d"),
            "duration": 14,
            "progress": 100,
            "assigned_to": "Legal Team",
            "dependencies": [2],
            "critical": True
        },
        {
            "id": 4,
            "task": "Current State Assessment",
            "description": "Document current business processes and systems",
            "start_date": (today - datetime.timedelta(days=30)).strftime("%Y-%m-%d"),
            "end_date": (today - datetime.timedelta(days=10)).strftime("%Y-%m-%d"),
            "duration": 20,
            "progress": 95,
            "assigned_to": "Business Analysts",
            "dependencies": [1],
            "critical": True
        },
        {
            "id": 5,
            "task": "Requirements Workshops",
            "description": "Conduct workshops with stakeholders to gather detailed requirements",
            "start_date": (today - datetime.timedelta(days=25)).strftime("%Y-%m-%d"),
            "end_date": (today - datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
            "duration": 20,
            "progress": 85,
            "assigned_to": "Business Analysts",
            "dependencies": [1, 3],
            "critical": True
        },
        {
            "id": 6,
            "task": "Future State Design",
            "description": "Design future state business processes",
            "start_date": (today - datetime.timedelta(days=7)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=8)).strftime("%Y-%m-%d"),
            "duration": 15,
            "progress": 40,
            "assigned_to": "Solution Architects",
            "dependencies": [4, 5],
            "critical": True
        },
        {
            "id": 7,
            "task": "Data Migration Strategy",
            "description": "Define approach for migrating data to new system",
            "start_date": (today - datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=10)).strftime("%Y-%m-%d"),
            "duration": 15,
            "progress": 25,
            "assigned_to": "Data Team",
            "dependencies": [4],
            "critical": False
        },
        {
            "id": 8,
            "task": "Infrastructure Planning",
            "description": "Design and plan technical infrastructure",
            "start_date": (today - datetime.timedelta(days=10)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
            "duration": 15,
            "progress": 60,
            "assigned_to": "Infrastructure Team",
            "dependencies": [3],
            "critical": True
        },
        {
            "id": 9,
            "task": "System Configuration - Phase 1",
            "description": "Configure core system modules",
            "start_date": (today + datetime.timedelta(days=9)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=29)).strftime("%Y-%m-%d"),
            "duration": 20,
            "progress": 0,
            "assigned_to": "Implementation Team",
            "dependencies": [6, 8],
            "critical": True
        },
        {
            "id": 10,
            "task": "System Configuration - Phase 2",
            "description": "Configure additional system modules",
            "start_date": (today + datetime.timedelta(days=30)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=50)).strftime("%Y-%m-%d"),
            "duration": 20,
            "progress": 0,
            "assigned_to": "Implementation Team",
            "dependencies": [9],
            "critical": True
        },
        {
            "id": 11,
            "task": "Integration Development",
            "description": "Develop integrations with other systems",
            "start_date": (today + datetime.timedelta(days=15)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=45)).strftime("%Y-%m-%d"),
            "duration": 30,
            "progress": 0,
            "assigned_to": "Integration Team",
            "dependencies": [8],
            "critical": True
        },
        {
            "id": 12,
            "task": "Data Migration Development",
            "description": "Develop data migration scripts and tools",
            "start_date": (today + datetime.timedelta(days=11)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=31)).strftime("%Y-%m-%d"),
            "duration": 20,
            "progress": 0,
            "assigned_to": "Data Team",
            "dependencies": [7],
            "critical": False
        },
        {
            "id": 13,
            "task": "User Training Materials",
            "description": "Develop user training documentation and materials",
            "start_date": (today + datetime.timedelta(days=30)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=50)).strftime("%Y-%m-%d"),
            "duration": 20,
            "progress": 0,
            "assigned_to": "Training Team",
            "dependencies": [6],
            "critical": False
        },
        {
            "id": 14,
            "task": "System Testing",
            "description": "Conduct functional and non-functional testing",
            "start_date": (today + datetime.timedelta(days=51)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=71)).strftime("%Y-%m-%d"),
            "duration": 20,
            "progress": 0,
            "assigned_to": "QA Team",
            "dependencies": [10, 11],
            "critical": True
        },
        {
            "id": 15,
            "task": "Data Migration Testing",
            "description": "Test data migration scripts with test data",
            "start_date": (today + datetime.timedelta(days=32)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=42)).strftime("%Y-%m-%d"),
            "duration": 10,
            "progress": 0,
            "assigned_to": "Data Team",
            "dependencies": [12],
            "critical": False
        },
        {
            "id": 16,
            "task": "User Acceptance Testing",
            "description": "Conduct UAT with business users",
            "start_date": (today + datetime.timedelta(days=72)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=92)).strftime("%Y-%m-%d"),
            "duration": 20,
            "progress": 0,
            "assigned_to": "Business Users",
            "dependencies": [14],
            "critical": True
        },
        {
            "id": 17,
            "task": "End User Training",
            "description": "Train end users on new system",
            "start_date": (today + datetime.timedelta(days=72)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=92)).strftime("%Y-%m-%d"),
            "duration": 20,
            "progress": 0,
            "assigned_to": "Training Team",
            "dependencies": [13, 14],
            "critical": True
        },
        {
            "id": 18,
            "task": "Cutover Planning",
            "description": "Develop detailed go-live cutover plan",
            "start_date": (today + datetime.timedelta(days=80)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=90)).strftime("%Y-%m-%d"),
            "duration": 10,
            "progress": 0,
            "assigned_to": "Implementation Team",
            "dependencies": [14],
            "critical": True
        },
        {
            "id": 19,
            "task": "Go-Live",
            "description": "Production deployment and cutover to new system",
            "start_date": (today + datetime.timedelta(days=93)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=97)).strftime("%Y-%m-%d"),
            "duration": 5,
            "progress": 0,
            "assigned_to": "Implementation Team",
            "dependencies": [16, 17, 18],
            "critical": True
        },
        {
            "id": 20,
            "task": "Post Go-Live Support",
            "description": "Provide support after system goes live",
            "start_date": (today + datetime.timedelta(days=98)).strftime("%Y-%m-%d"),
            "end_date": (today + datetime.timedelta(days=128)).strftime("%Y-%m-%d"),
            "duration": 30,
            "progress": 0,
            "assigned_to": "Support Team",
            "dependencies": [19],
            "critical": False
        }
    ]
    
    # Create resource data
    resources = [
        {
            "name": "Maria Rodriguez",
            "role": "Program Manager",
            "availability": 100,
            "allocated": 90,
            "skills": ["Program Management", "Enterprise Software", "Stakeholder Management", "Risk Management"]
        },
        {
            "name": "Business Analysts",
            "role": "Business Analysis Team",
            "availability": 300,
            "allocated": 320,
            "skills": ["Requirements Gathering", "Process Modeling", "Documentation", "Stakeholder Management"]
        },
        {
            "name": "Solution Architects",
            "role": "Architecture Team",
            "availability": 200,
            "allocated": 240,
            "skills": ["Enterprise Architecture", "Solution Design", "Integration", "Technical Leadership"]
        },
        {
            "name": "Legal Team",
            "role": "Contract Management",
            "availability": 100,
            "allocated": 60,
            "skills": ["Contract Law", "Negotiation", "Vendor Management", "Risk Assessment"]
        },
        {
            "name": "Procurement Team",
            "role": "Vendor Management",
            "availability": 150,
            "allocated": 120,
            "skills": ["Vendor Selection", "RFP Management", "Contract Negotiation", "Cost Analysis"]
        },
        {
            "name": "Implementation Team",
            "role": "Core Implementation",
            "availability": 400,
            "allocated": 380,
            "skills": ["System Configuration", "Business Process Implementation", "Testing", "Cutover Management"]
        },
        {
            "name": "Data Team",
            "role": "Data Migration Specialists",
            "availability": 200,
            "allocated": 170,
            "skills": ["Data Migration", "ETL", "Data Mapping", "Data Quality", "Database Management"]
        },
        {
            "name": "Infrastructure Team",
            "role": "IT Infrastructure",
            "availability": 200,
            "allocated": 160,
            "skills": ["Cloud Infrastructure", "Network Design", "Security", "Performance Optimization"]
        },
        {
            "name": "Integration Team",
            "role": "Integration Specialists",
            "availability": 250,
            "allocated": 270,
            "skills": ["API Development", "Middleware", "Integration Testing", "System Interfaces"]
        },
        {
            "name": "QA Team",
            "role": "Quality Assurance",
            "availability": 300,
            "allocated": 280,
            "skills": ["Test Planning", "Functional Testing", "Regression Testing", "Performance Testing"]
        },
        {
            "name": "Training Team",
            "role": "User Training",
            "availability": 200,
            "allocated": 150,
            "skills": ["Training Development", "Instructional Design", "Training Delivery", "Documentation"]
        },
        {
            "name": "Business Users",
            "role": "Subject Matter Experts",
            "availability": 300,
            "allocated": 200,
            "skills": ["Business Knowledge", "UAT", "Process Expertise", "Change Management"]
        },
        {
            "name": "Support Team",
            "role": "Post-Implementation Support",
            "availability": 250,
            "allocated": 200,
            "skills": ["Tier 1-3 Support", "Issue Resolution", "End User Support", "System Administration"]
        }
    ]
    
    # Create risk data
    risks = [
        {
            "id": 1,
            "title": "Vendor Delays",
            "description": "Vendor may not deliver key functionality on time",
            "severity": "High",
            "probability": "Medium",
            "impact": "Significant project delays and potential scope reduction",
            "mitigation": "Regular vendor status meetings, clear contractual obligations with penalties",
            "owner": "Maria Rodriguez",
            "status": "Active"
        },
        {
            "id": 2,
            "title": "Resource Constraints",
            "description": "Business users have limited availability for requirements and testing",
            "severity": "Medium",
            "probability": "High",
            "impact": "Incomplete requirements gathering leading to rework",
            "mitigation": "Early engagement with department heads, clear resource commitment documentation",
            "owner": "Business Analysts",
            "status": "Active"
        },
        {
            "id": 3,
            "title": "Data Migration Complexity",
            "description": "Legacy data structure is poorly documented and may require extensive cleansing",
            "severity": "High",
            "probability": "High",
            "impact": "Data migration delays and potential data quality issues",
            "mitigation": "Early data profiling, additional data expertise, data cleansing tools",
            "owner": "Data Team",
            "status": "Active"
        },
        {
            "id": 4,
            "title": "Integration Challenges",
            "description": "Multiple legacy systems with limited documentation need to be integrated",
            "severity": "Medium",
            "probability": "Medium",
            "impact": "Integration failures or performance issues",
            "mitigation": "Detailed integration inventory, proof of concepts for complex integrations",
            "owner": "Integration Team",
            "status": "Active"
        },
        {
            "id": 5,
            "title": "Change Resistance",
            "description": "Users may resist adopting the new system due to significant process changes",
            "severity": "Medium",
            "probability": "High",
            "impact": "Low adoption rates and reduced return on investment",
            "mitigation": "Comprehensive change management plan, early user involvement, executive sponsorship",
            "owner": "Maria Rodriguez",
            "status": "Active"
        },
        {
            "id": 6,
            "title": "Scope Creep",
            "description": "Stakeholders requesting additional features beyond initial requirements",
            "severity": "Medium",
            "probability": "High",
            "impact": "Schedule delays and budget overruns",
            "mitigation": "Robust change control process, clear prioritization framework",
            "owner": "Maria Rodriguez",
            "status": "Active"
        },
        {
            "id": 7,
            "title": "Performance Issues",
            "description": "System may not meet performance expectations under full load",
            "severity": "High",
            "probability": "Medium",
            "impact": "User dissatisfaction and possible business disruption",
            "mitigation": "Early performance testing, infrastructure optimization, performance SLAs",
            "owner": "Infrastructure Team",
            "status": "Active"
        }
    ]
    
    # Create RAID data
    raid = {
        "risks": risks,
        "assumptions": [
            {
                "id": 1,
                "description": "Executive sponsors will remain committed throughout the project",
                "impact": "High",
                "validation_method": "Regular executive steering committee meetings",
                "status": "Validated"
            },
            {
                "id": 2,
                "description": "Legacy systems will remain stable during transition period",
                "impact": "Medium",
                "validation_method": "System monitoring and support arrangements",
                "status": "Partially Validated"
            },
            {
                "id": 3,
                "description": "Vendor implementation team has necessary expertise",
                "impact": "High",
                "validation_method": "Skills assessment during vendor selection",
                "status": "Validated"
            },
            {
                "id": 4,
                "description": "Department heads can commit 20% of SME time to the project",
                "impact": "High",
                "validation_method": "Written commitment from department heads",
                "status": "Partially Validated"
            }
        ],
        "issues": [
            {
                "id": 1,
                "description": "Legacy system documentation is incomplete",
                "impact": "Medium",
                "raised_date": (today - datetime.timedelta(days=20)).strftime("%Y-%m-%d"),
                "owner": "Business Analysts",
                "status": "In Progress",
                "resolution": "Conducting interviews with system experts to document current state"
            },
            {
                "id": 2,
                "description": "Key business stakeholder left the company",
                "impact": "High",
                "raised_date": (today - datetime.timedelta(days=15)).strftime("%Y-%m-%d"),
                "owner": "Maria Rodriguez",
                "status": "Resolved",
                "resolution": "Replacement stakeholder identified and onboarded"
            },
            {
                "id": 3,
                "description": "Vendor contract missing service level agreements",
                "impact": "High",
                "raised_date": (today - datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
                "owner": "Legal Team",
                "status": "In Progress",
                "resolution": "Negotiating contract amendment with vendor"
            }
        ],
        "dependencies": [
            {
                "id": 1,
                "description": "Network infrastructure upgrade must be completed before system installation",
                "dependency_type": "External",
                "dependent_on": "IT Infrastructure Department",
                "due_date": (today + datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
                "status": "On Track"
            },
            {
                "id": 2,
                "description": "Legacy system APIs need to be documented",
                "dependency_type": "Internal",
                "dependent_on": "Integration Team",
                "due_date": (today + datetime.timedelta(days=15)).strftime("%Y-%m-%d"),
                "status": "At Risk"
            },
            {
                "id": 3,
                "description": "Vendor needs to provide integration specifications",
                "dependency_type": "External",
                "dependent_on": "Software Vendor",
                "due_date": (today + datetime.timedelta(days=10)).strftime("%Y-%m-%d"),
                "status": "Completed"
            }
        ]
    }
    
    # Create decisions log
    decisions = [
        {
            "id": 1,
            "title": "Vendor Selection",
            "description": "Selected ERP vendor based on functional fit and implementation timeline",
            "date": (today - datetime.timedelta(days=40)).strftime("%Y-%m-%d"),
            "made_by": "Executive Committee",
            "status": "Approved",
            "impact": "High",
            "alternatives_considered": "Three vendors were evaluated in the final round"
        },
        {
            "id": 2,
            "title": "Phased Implementation Approach",
            "description": "Decision to implement in three phases rather than big bang approach",
            "date": (today - datetime.timedelta(days=35)).strftime("%Y-%m-%d"),
            "made_by": "Program Steering Committee",
            "status": "Approved",
            "impact": "High",
            "alternatives_considered": "Big bang, phased by module, phased by business unit"
        },
        {
            "id": 3,
            "title": "Cloud Hosting",
            "description": "Decision to use cloud hosting instead of on-premises infrastructure",
            "date": (today - datetime.timedelta(days=25)).strftime("%Y-%m-%d"),
            "made_by": "Technical Committee",
            "status": "Approved",
            "impact": "Medium",
            "alternatives_considered": "On-premises, hybrid model"
        },
        {
            "id": 4,
            "title": "Custom Development for Specialized Processes",
            "description": "Decision to build custom module for specialized business processes",
            "date": (today - datetime.timedelta(days=15)).strftime("%Y-%m-%d"),
            "made_by": "Program Steering Committee",
            "status": "Pending",
            "impact": "Medium",
            "alternatives_considered": "Process adaptation to standard software, external point solution"
        }
    ]
    
    # Team sentiment data
    sentiment = {
        "overall_score": 0.65,  # Range from -1 (negative) to 1 (positive)
        "key_themes": ["Training concerns", "Timeline pressure", "System capabilities", "Process improvements"],
        "feedback": [
            {
                "date": (today - datetime.timedelta(days=10)).strftime("%Y-%m-%d"),
                "content": "Concerned about the timeline for training before go-live. Otherwise excited about the new system capabilities.",
                "sentiment": 0.4,
                "source": "Implementation Team Member"
            },
            {
                "date": (today - datetime.timedelta(days=8)).strftime("%Y-%m-%d"),
                "content": "Looking forward to the improved reporting features. The requirements gathering process was well managed.",
                "sentiment": 0.8,
                "source": "Business User"
            },
            {
                "date": (today - datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
                "content": "Worried about the data migration strategy. The legacy data has many inconsistencies that need to be addressed.",
                "sentiment": 0.2,
                "source": "Data Team Member"
            },
            {
                "date": (today - datetime.timedelta(days=3)).strftime("%Y-%m-%d"),
                "content": "The project leadership has been responsive to our concerns about process changes. Good collaboration overall.",
                "sentiment": 0.7,
                "source": "Department Manager"
            }
        ]
    }
    
    # Create baseline WBS (original plan for scope creep detection)
    baseline_wbs = wbs.copy()
    # Remove some tasks from the original plan for comparison
    baseline_wbs = [task for task in baseline_wbs if task["id"] not in [11, 12, 13, 20]]
    
    # Assemble the project data
    project_data = {
        "name": "Enterprise Software Implementation",
        "description": "Implementation of enterprise software solution across all business units with data migration from legacy systems",
        "start_date": (today - datetime.timedelta(days=60)).strftime("%Y-%m-%d"),
        "end_date": (today + datetime.timedelta(days=128)).strftime("%Y-%m-%d"),
        "budget": 2500000,
        "actual_cost": 900000,
        "status": "In Progress",
        "wbs": wbs,
        "baseline_wbs": baseline_wbs,
        "resources": resources,
        "raid": raid,
        "risks": risks,
        "decisions": decisions,
        "sentiment": sentiment,
        "team_feedback": sentiment["feedback"]
    }
    
    return project_data
