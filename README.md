# AI PM Buddy v2.0

A comprehensive AI-powered Project Management Assistant built with Streamlit and OpenAI integration.

![Project Management](https://img.icons8.com/fluency/96/000000/project-management.png)

## Overview

AI PM Buddy v2.0 is an advanced project management tool designed to enhance project execution, monitoring, communication, and risk management using artificial intelligence. The application provides intelligent insights, automations, risk management, reporting, and integration with existing project management tools.

This upgraded version builds upon the foundation of v1.0 with a completely redesigned UI, new features, and enhanced capabilities.

## Features

### Core Features (From v1.0)
- **AI PM Insights**: Real-time AI-powered project analysis and risk detection
- **WBS Overview**: Visual work breakdown structure management and tracking
- **Resource Allocation Monitoring**: Optimize team allocation and identify bottlenecks
- **RAID Compliance Checker**: Ensure proper documentation of risks, assumptions, issues, and dependencies
- **Decision Log Assistant**: Track and document project decisions
- **Team Sentiment Analyzer**: Monitor team morale and sentiment
- **Agile Coach Bot**: Get AI-powered answers to Agile methodology questions
- **PM Knowledge Assistant**: Access project management best practices and knowledge
- **Critical Path Slippage Warning**: Proactive monitoring of critical path tasks
- **Scope Creep Early Detection**: Identify and manage scope changes

### New in v2.0
- **Personalized Dashboard**: Customizable project overview with key metrics including progress, resource allocation, and risk status
- **AI Personal Assistant**: Get daily briefings, intelligent responses to queries, and AI-powered recommendations
- **Document Management**:
  - **Document Generator**: Create professional project documentation using AI (status reports, requirements documents, etc.)
  - **Template Management**: Create and manage custom document templates for consistent documentation
- **Scenario Simulation**:
  - **Risk Simulator**: Model the potential impact of identified risks with Monte Carlo simulation
  - **What-If Analysis**: Test different resource allocations, timeline changes, and budget scenarios
- **Enhanced Communication**:
  - **Team Communication**: Centralized communication hub with announcements, meeting notes, and feedback collection
  - **Notification Center**: Configurable project notifications with multi-channel delivery options
- **External Integrations**:
  - **JIRA Connector**: Synchronize tasks, statuses, and issues with JIRA
  - **MS Teams Integration**: Share updates and receive notifications through Microsoft Teams
- **Modern UI**: Completely redesigned interface with improved navigation, categorized modules, and better data visualization

## Technical Architecture

AI PM Buddy v2.0 is built using:
- **Streamlit**: For the web application framework
- **OpenAI API**: For AI-powered insights and assistance
- **Python**: Backend programming language
- **Plotly & Matplotlib**: For data visualization
- **NetworkX**: For critical path and network diagrams
- **Integration APIs**: For JIRA, MS Teams, and Outlook connectivity

## Getting Started

### Running on Replit

1. Fork this Replit project
2. Provide your OpenAI API key in the sidebar settings
3. Start exploring the features and modules

### Local Installation

For detailed local installation instructions, please refer to the [INSTALLATION.md](INSTALLATION.md) file.

## Usage Guide

### Getting Started
1. **Create or Select a Project**: Use the sidebar to create a new project or select an existing one.
2. **Dashboard Overview**: Review the project dashboard to see overall progress, resource allocation, and risk status.
3. **AI Assistant**: Access the AI Personal Assistant for project insights and recommendations.

### Using the Modules
AI PM Buddy organizes functionality into categorical modules:

#### Project Monitoring
- **AI PM Insights**: View AI-generated insights about your project's health and risks.
- **WBS Overview**: Manage your project's work breakdown structure with visual tracking.
- **Resource Allocation**: Monitor team workload and optimize resource distribution.
- **Critical Path Slippage**: Track tasks on the critical path and receive warnings about potential delays.
- **Scope Creep Detection**: Identify and manage changes to project scope.

#### Risk Management
- **RAID Compliance**: Maintain risks, assumptions, issues, and dependencies logs.
- **Decision Log**: Track key project decisions and their rationale.
- **Team Sentiment**: Monitor team morale and sentiment through feedback analysis.

#### Knowledge Management
- **Agile Coach Bot**: Get AI-powered answers to Agile methodology questions.
- **PM Knowledge Assistant**: Access project management best practices and templates.

#### Documents & Reports (New in v2.0)
- **Document Generator**: Create professional project documentation using AI and templates.
- **Template Management**: Manage custom document templates for various project needs.

#### Simulation & Analysis (New in v2.0)
- **Risk Simulator**: Run Monte Carlo simulations to model risk impact scenarios.
- **What-If Analysis**: Test different schedule, resource, and budget scenarios.

#### Communication (New in v2.0)
- **Team Communication**: Manage announcements, meeting notes, and team feedback.
- **Notification Center**: Configure and manage project notifications.

#### Integrations (New in v2.0)
- **JIRA Connector**: Sync project tasks with JIRA for seamless integration.
- **MS Teams Integration**: Send updates and notifications to Microsoft Teams.

### External Integrations
For full functionality of integration features, you'll need:

1. **OpenAI API Key**: Required for AI-powered features (insights, document generation, etc.)
2. **JIRA Credentials**: To synchronize with JIRA (optional)
3. **MS Teams Webhook URL**: To send notifications to Teams (optional)
4. **Twilio Credentials**: For SMS notifications (optional)

These can be configured in the respective module settings.

## Roadmap

- **v2.1**: Enhanced mobile support and offline capabilities
- **v2.2**: Advanced analytics and predictive modeling
- **v2.3**: Expanded integration options and API connectivity
- **v3.0**: Machine learning models trained on your specific project patterns

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the AI capabilities
- Streamlit for the excellent web application framework
- The project management community for valuable feedback

---

© 2025 PM Technologies Inc.