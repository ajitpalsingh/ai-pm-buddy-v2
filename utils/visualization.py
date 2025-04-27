import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
import streamlit as st
from wordcloud import WordCloud

def create_gantt_chart(wbs_data):
    """
    Create a Gantt chart for WBS tasks using Plotly.
    
    Args:
        wbs_data: List of WBS task dictionaries
        
    Returns:
        Plotly figure object
    """
    # Convert to DataFrame
    df = pd.DataFrame(wbs_data)
    
    # Create color mapping for critical path
    color_discrete_map = {True: "red", False: "blue"}
    
    # Create Gantt chart
    fig = px.timeline(
        df, 
        x_start="start_date", 
        x_end="end_date", 
        y="task",
        color="critical",
        color_discrete_map=color_discrete_map,
        hover_data=["description", "progress", "assigned_to"],
        labels={"task": "Task", "critical": "On Critical Path"}
    )
    
    # Add progress bars
    for i, task in enumerate(wbs_data):
        fig.add_shape(
            type="rect",
            x0=task["start_date"],
            x1=pd.to_datetime(task["start_date"]) + pd.Timedelta(days=task["duration"] * task["progress"] / 100),
            y0=i - 0.4,
            y1=i + 0.4,
            fillcolor="green",
            opacity=0.5,
            layer="below",
            line_width=0,
        )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Timeline",
        yaxis_title="Tasks",
        legend_title="Critical Path",
        height=400,
        margin=dict(l=10, r=10, b=10, t=30)
    )
    
    # Enable range slider for timeline
    fig.update_xaxes(rangeslider_visible=True)
    
    return fig

def create_resource_allocation_chart(resource_data):
    """
    Create a resource allocation chart using Plotly.
    
    Args:
        resource_data: List of resource dictionaries
        
    Returns:
        Plotly figure object
    """
    # Convert to DataFrame
    df = pd.DataFrame(resource_data)
    
    # Calculate utilization percentage
    df['utilization'] = (df['allocated'] / df['availability']) * 100
    
    # Create horizontal bar chart for resource allocation
    fig = go.Figure()
    
    # Add availability bars
    fig.add_trace(go.Bar(
        y=df['name'],
        x=df['availability'],
        name='Available',
        orientation='h',
        marker=dict(color='rgba(55, 128, 191, 0.3)')
    ))
    
    # Add allocated bars
    fig.add_trace(go.Bar(
        y=df['name'],
        x=df['allocated'],
        name='Allocated',
        orientation='h',
        marker=dict(color='rgba(55, 128, 191, 0.9)')
    ))
    
    # Add utilization percentage text
    for i, row in df.iterrows():
        fig.add_annotation(
            x=row['availability'],
            y=i,
            text=f"{row['utilization']:.0f}%",
            showarrow=False,
            xshift=15,
            font=dict(color="black")
        )
    
    # Update layout
    fig.update_layout(
        barmode='overlay',
        xaxis_title="Hours",
        yaxis_title="Resources",
        legend_title="Allocation",
        height=400,
        margin=dict(l=10, r=10, b=10, t=30)
    )
    
    return fig

def create_raid_compliance_chart(raid_data):
    """
    Create RAID compliance visualization using Plotly.
    
    Args:
        raid_data: Dictionary of RAID data
        
    Returns:
        Plotly figure object
    """
    # Analyze each RAID category for required fields
    categories = ['risks', 'assumptions', 'issues', 'dependencies']
    
    # Required fields for each category
    required_fields = {
        'risks': ['description', 'impact', 'probability', 'mitigation', 'owner'],
        'assumptions': ['description', 'impact', 'owner', 'validation'],
        'issues': ['description', 'impact', 'owner', 'resolution', 'status'],
        'dependencies': ['description', 'depends_on', 'impact', 'due_date', 'status']
    }
    
    # Calculate compliance percentage for each category
    compliance_data = []
    
    for category in categories:
        items = raid_data.get(category, [])
        if not items:
            compliance_data.append({'category': category, 'compliance': 0, 'count': 0})
            continue
        
        total_fields = len(items) * len(required_fields[category])
        filled_fields = 0
        
        for item in items:
            for field in required_fields[category]:
                if field in item and item[field]:
                    filled_fields += 1
        
        if total_fields > 0:
            compliance = (filled_fields / total_fields) * 100
        else:
            compliance = 0
            
        compliance_data.append({
            'category': category.capitalize(),
            'compliance': compliance,
            'count': len(items)
        })
    
    # Create DataFrame
    df = pd.DataFrame(compliance_data)
    
    # Create horizontal bar chart
    fig = px.bar(
        df,
        x='compliance',
        y='category',
        orientation='h',
        color='compliance',
        color_continuous_scale=px.colors.sequential.Viridis,
        text=df['count'].apply(lambda x: f"{x} items"),
        labels={'compliance': 'Compliance %', 'category': 'RAID Category'},
        range_color=[0, 100]
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Compliance Percentage",
        yaxis_title="RAID Category",
        height=400,
        margin=dict(l=10, r=10, b=10, t=30)
    )
    
    return fig

def create_decision_status_chart(decisions):
    """
    Create a decision status visualization using Plotly.
    
    Args:
        decisions: List of decision dictionaries
        
    Returns:
        Plotly figure object
    """
    if not decisions:
        return None
    
    # Count decisions by status
    status_counts = {}
    for decision in decisions:
        status = decision.get('status', 'Unknown')
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Create pie chart
    fig = px.pie(
        values=list(status_counts.values()),
        names=list(status_counts.keys()),
        title="Decision Status Distribution",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    
    # Update layout
    fig.update_layout(
        legend_title="Status",
        height=400,
        margin=dict(l=10, r=10, b=10, t=50)
    )
    
    return fig

def create_sentiment_gauge(sentiment_score):
    """
    Create a sentiment gauge chart using Plotly.
    
    Args:
        sentiment_score: Sentiment score between -1 and 1
        
    Returns:
        Plotly figure object
    """
    # Map sentiment score to 0-100 scale for gauge
    gauge_value = (sentiment_score + 1) * 50
    
    # Create gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=gauge_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Team Sentiment"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 33], 'color': "red"},
                {'range': [33, 66], 'color': "yellow"},
                {'range': [66, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': gauge_value
            }
        }
    ))
    
    # Update layout
    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, b=10, t=50)
    )
    
    return fig

def create_wordcloud(feedback_text):
    """
    Create a wordcloud from feedback text.
    
    Args:
        feedback_text: List of feedback text entries
        
    Returns:
        Matplotlib figure
    """
    if not feedback_text:
        return None
        
    # Combine all feedback
    text = ' '.join(feedback_text)
    
    # Create wordcloud
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        max_words=100,
        contour_width=1,
        contour_color='steelblue'
    ).generate(text)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    
    return fig

def create_critical_path_network(wbs_data):
    """
    Create a network diagram of the critical path using NetworkX and Matplotlib.
    
    Args:
        wbs_data: List of WBS task dictionaries
        
    Returns:
        Matplotlib figure
    """
    # Create directed graph
    G = nx.DiGraph()
    
    # Add nodes (tasks)
    for task in wbs_data:
        G.add_node(
            task['id'],
            name=task['task'],
            duration=task['duration'],
            progress=task['progress'],
            critical=task['critical']
        )
    
    # Add edges (dependencies)
    for task in wbs_data:
        for dep in task.get('dependencies', []):
            G.add_edge(dep, task['id'])
    
    # Position nodes using hierarchical layout
    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Draw non-critical nodes
    non_critical_nodes = [n for n, d in G.nodes(data=True) if not d.get('critical', False)]
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=non_critical_nodes,
        node_color='lightblue',
        node_size=1500,
        alpha=0.8
    )
    
    # Draw critical nodes
    critical_nodes = [n for n, d in G.nodes(data=True) if d.get('critical', True)]
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=critical_nodes,
        node_color='red',
        node_size=1500,
        alpha=0.8
    )
    
    # Draw edges
    nx.draw_networkx_edges(
        G, pos,
        width=2,
        alpha=0.5,
        edge_color='gray',
        arrows=True,
        arrowsize=20
    )
    
    # Add task labels with progress
    node_labels = {}
    for n, d in G.nodes(data=True):
        node_labels[n] = f"{d['name']}\n({d['progress']}% complete)"
    
    nx.draw_networkx_labels(
        G, pos,
        labels=node_labels,
        font_size=8,
        font_weight='bold'
    )
    
    # Remove axes
    ax.axis('off')
    plt.tight_layout()
    
    return fig

def create_scope_creep_chart(baseline_wbs, current_wbs):
    """
    Create a visualization comparing baseline WBS to current WBS to show scope creep.
    
    Args:
        baseline_wbs: Original WBS tasks
        current_wbs: Current WBS tasks
        
    Returns:
        Plotly figure object
    """
    # Extract task counts and durations
    baseline_count = len(baseline_wbs)
    current_count = len(current_wbs)
    
    baseline_duration = sum(task['duration'] for task in baseline_wbs)
    current_duration = sum(task['duration'] for task in current_wbs)
    
    # Calculate percentage changes
    task_change_pct = ((current_count - baseline_count) / baseline_count) * 100 if baseline_count > 0 else 0
    duration_change_pct = ((current_duration - baseline_duration) / baseline_duration) * 100 if baseline_duration > 0 else 0
    
    # Create DataFrame for comparison
    df = pd.DataFrame({
        'Category': ['Tasks', 'Duration (days)'],
        'Baseline': [baseline_count, baseline_duration],
        'Current': [current_count, current_duration],
        'Change %': [task_change_pct, duration_change_pct]
    })
    
    # Create bar chart
    fig = go.Figure()
    
    # Add bars for baseline
    fig.add_trace(go.Bar(
        name='Baseline',
        x=df['Category'],
        y=df['Baseline'],
        marker_color='blue'
    ))
    
    # Add bars for current
    fig.add_trace(go.Bar(
        name='Current',
        x=df['Category'],
        y=df['Current'],
        marker_color='red'
    ))
    
    # Add percentage change as text
    for i, row in df.iterrows():
        fig.add_annotation(
            x=row['Category'],
            y=max(row['Baseline'], row['Current']),
            text=f"{row['Change %']:.1f}%",
            showarrow=True,
            arrowhead=1,
            ax=0,
            ay=-30,
            font=dict(size=12, color="black")
        )
    
    # Update layout
    fig.update_layout(
        barmode='group',
        title="Scope Comparison: Baseline vs. Current",
        xaxis_title="Metric",
        yaxis_title="Count",
        legend_title="Version",
        height=400,
        margin=dict(l=10, r=10, b=10, t=50)
    )
    
    return fig
