import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import datetime
import random
from datetime import timedelta

def show_risk_simulator(project_data):
    """
    Display the Risk Simulation module.
    
    Args:
        project_data: Dictionary containing project information
    """
    st.subheader("Risk Simulation & Impact Analysis")
    
    # Create tabs for different simulation types
    tab1, tab2, tab3 = st.tabs(["Monte Carlo Simulation", "Risk Impact Analysis", "Mitigation Strategies"])
    
    with tab1:
        show_monte_carlo_simulation(project_data)
    
    with tab2:
        show_risk_impact_analysis(project_data)
        
    with tab3:
        show_mitigation_strategies(project_data)

def show_monte_carlo_simulation(project_data):
    """Display Monte Carlo simulation for project schedule and cost."""
    st.markdown("### Monte Carlo Schedule Simulation")
    st.write("This simulation runs multiple iterations to predict the most likely project completion dates based on task duration uncertainties.")
    
    # Get project tasks
    tasks = project_data.get('wbs', [])
    
    if not tasks:
        st.warning("No tasks found in the project. Please add tasks to the WBS first.")
        return
    
    # Configuration options
    col1, col2 = st.columns(2)
    
    with col1:
        confidence_levels = st.multiselect(
            "Confidence Levels to Display", 
            ["50%", "80%", "90%", "95%"],
            default=["80%", "95%"]
        )
        
        simulation_runs = st.slider("Number of Simulation Runs", 
                                   min_value=100, 
                                   max_value=10000, 
                                   value=1000, 
                                   step=100)
    
    with col2:
        uncertainty_level = st.slider("Task Duration Uncertainty (%)", 
                                     min_value=5, 
                                     max_value=50, 
                                     value=20, 
                                     step=5)
        
        critical_path_focus = st.checkbox("Focus on Critical Path Only", value=True)
    
    # Run simulation button
    if st.button("Run Monte Carlo Simulation"):
        with st.spinner(f"Running {simulation_runs} simulations..."):
            # Filter tasks if critical path focus is enabled
            simulation_tasks = [t for t in tasks if t.get('critical', False)] if critical_path_focus else tasks
            
            if not simulation_tasks:
                st.warning("No critical path tasks found. Please mark tasks as critical or disable 'Focus on Critical Path Only'.")
                return
            
            # Run the simulation
            simulation_results = run_monte_carlo_simulation(
                simulation_tasks, 
                uncertainty_level / 100, 
                simulation_runs
            )
            
            # Store results in session state
            st.session_state.monte_carlo_results = simulation_results
            
            # Display simulation results
            st.success(f"Simulation completed with {simulation_runs} iterations.")
            
            # Create results dataframe
            results_df = pd.DataFrame({
                'Completion Date': simulation_results['completion_dates'],
                'Total Duration (days)': simulation_results['durations']
            })
            
            # Calculate statistics
            min_date = results_df['Completion Date'].min()
            max_date = results_df['Completion Date'].max()
            mean_date = min_date + timedelta(days=np.mean((results_df['Completion Date'] - min_date).dt.days))
            
            # Calculate confidence levels
            confidence_percentiles = {
                "50%": 50,
                "80%": 80,
                "90%": 90,
                "95%": 95
            }
            
            confidence_results = {}
            for level, percentile in confidence_percentiles.items():
                if level in confidence_levels:
                    days_percentile = np.percentile(simulation_results['durations'], percentile)
                    date_percentile = min_date + timedelta(days=days_percentile - min(simulation_results['durations']))
                    confidence_results[level] = {
                        'days': days_percentile,
                        'date': date_percentile
                    }
            
            # Display summary statistics
            st.markdown("#### Simulation Results Summary")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Earliest Completion", min_date.strftime("%Y-%m-%d"))
            with col2:
                st.metric("Most Likely Completion", mean_date.strftime("%Y-%m-%d"))
            with col3:
                st.metric("Latest Completion", max_date.strftime("%Y-%m-%d"))
            
            # Display confidence levels
            st.markdown("#### Confidence Levels")
            
            confidence_df = pd.DataFrame({
                'Confidence Level': list(confidence_results.keys()),
                'Completion Date': [results['date'].strftime("%Y-%m-%d") for results in confidence_results.values()],
                'Total Duration (days)': [results['days'] for results in confidence_results.values()]
            })
            
            st.dataframe(confidence_df, use_container_width=True)
            
            # Create histogram of completion dates
            fig = px.histogram(
                results_df, 
                x='Completion Date', 
                marginal='box',
                title='Distribution of Possible Completion Dates',
                labels={'Completion Date': 'Project Completion Date'},
                color_discrete_sequence=['#4CAF50']
            )
            
            # Add vertical lines for confidence levels
            for level, results in confidence_results.items():
                fig.add_vline(
                    x=results['date'], 
                    line_dash="dash", 
                    line_color="#FF9800",
                    annotation_text=f"{level} Confidence",
                    annotation_position="top right"
                )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Duration cumulative distribution
            durations = sorted(simulation_results['durations'])
            cumulative_prob = [i / len(durations) for i in range(1, len(durations) + 1)]
            
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=durations,
                y=cumulative_prob,
                mode='lines',
                name='Cumulative Probability',
                line=dict(color='#4CAF50', width=2)
            ))
            
            # Add reference lines for confidence levels
            for level, results in confidence_results.items():
                percentile = confidence_percentiles[level] / 100
                fig2.add_trace(go.Scatter(
                    x=[results['days'], results['days']],
                    y=[0, percentile],
                    mode='lines',
                    line=dict(color='#FF9800', width=1, dash='dash'),
                    showlegend=False
                ))
                fig2.add_trace(go.Scatter(
                    x=[min(durations), results['days']],
                    y=[percentile, percentile],
                    mode='lines',
                    line=dict(color='#FF9800', width=1, dash='dash'),
                    showlegend=False
                ))
                fig2.add_annotation(
                    x=results['days'],
                    y=percentile,
                    text=f"{level}",
                    showarrow=True,
                    arrowhead=1
                )
            
            fig2.update_layout(
                title='Cumulative Probability Distribution of Project Duration',
                xaxis_title='Project Duration (days)',
                yaxis_title='Cumulative Probability',
                yaxis=dict(tickformat='.0%')
            )
            
            st.plotly_chart(fig2, use_container_width=True)

def show_risk_impact_analysis(project_data):
    """Display risk impact analysis on project objectives."""
    st.markdown("### Risk Impact Analysis")
    st.write("Analyze how identified risks could impact project objectives.")
    
    # Get project risks
    risks = project_data.get('risks', [])
    
    if not risks:
        st.warning("No risks found in the project. Please add risks to the RAID log first.")
        return
    
    # Risk selection
    selected_risks = st.multiselect(
        "Select Risks to Analyze",
        [risk.get('description', f"Risk {i+1}") for i, risk in enumerate(risks)],
        default=[risk.get('description', f"Risk {i+1}") for i, risk in enumerate(risks) if risk.get('severity', '').lower() == 'high']
    )
    
    # If no risks are selected, use all risks
    if not selected_risks:
        st.info("No risks selected. Using all risks for analysis.")
        selected_risks = [risk.get('description', f"Risk {i+1}") for i, risk in enumerate(risks)]
    
    # Project objectives to analyze
    objectives = ["Schedule", "Budget", "Scope", "Quality", "Resources"]
    selected_objectives = st.multiselect(
        "Select Project Objectives to Analyze",
        objectives,
        default=objectives[:3]  # Default to first 3 objectives
    )
    
    # Run impact analysis button
    if st.button("Run Impact Analysis"):
        with st.spinner("Analyzing risk impacts..."):
            # Filter selected risks
            filtered_risks = [r for r in risks if r.get('description', '') in selected_risks]
            
            # Run impact analysis
            impact_results = analyze_risk_impacts(filtered_risks, selected_objectives)
            
            # Display impact matrix
            st.markdown("#### Risk Impact Matrix")
            
            # Create impact matrix dataframe
            impact_df = pd.DataFrame(impact_results['impact_matrix'])
            impact_df = impact_df.set_index('Risk')
            
            # Apply color styling based on impact level
            def color_impact(val):
                if val == 'High':
                    return 'background-color: rgba(255, 0, 0, 0.2)'
                elif val == 'Medium':
                    return 'background-color: rgba(255, 165, 0, 0.2)'
                elif val == 'Low':
                    return 'background-color: rgba(0, 128, 0, 0.2)'
                return ''
            
            styled_impact = impact_df.style.applymap(color_impact)
            st.dataframe(styled_impact)
            
            # Create radar chart of overall impact by objective
            fig = go.Figure()
            
            # Add a trace for each risk
            for risk in impact_results['risk_scores']:
                fig.add_trace(go.Scatterpolar(
                    r=risk['scores'],
                    theta=risk['objectives'],
                    fill='toself',
                    name=risk['risk']
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 10]
                    )
                ),
                title='Risk Impact by Objective',
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display combined impact
            st.markdown("#### Combined Risk Impact")
            
            combined_impact = impact_results['combined_impact']
            impact_levels = ['Low', 'Medium', 'High']
            
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                x=combined_impact['objectives'],
                y=combined_impact['impact_scores'],
                marker_color=['#4CAF50' if score < 3.33 else '#FF9800' if score < 6.67 else '#F44336' for score in combined_impact['impact_scores']]
            ))
            
            fig2.update_layout(
                title='Combined Risk Impact by Objective',
                xaxis_title='Project Objective',
                yaxis_title='Impact Score (0-10)',
                yaxis=dict(range=[0, 10])
            )
            
            st.plotly_chart(fig2, use_container_width=True)
            
            # Display most impacted objectives
            max_impact_obj = combined_impact['objectives'][np.argmax(combined_impact['impact_scores'])]
            max_impact_score = np.max(combined_impact['impact_scores'])
            
            st.markdown(f"**Most Impacted Objective:** {max_impact_obj} (Impact Score: {max_impact_score:.1f}/10)")
            
            # Recommendations based on impact analysis
            st.markdown("#### Recommendations")
            
            # Generate recommendations for objectives with high impact
            high_impact_objs = [obj for obj, score in zip(combined_impact['objectives'], combined_impact['impact_scores']) if score >= 6.67]
            
            if high_impact_objs:
                st.markdown("Consider the following recommendations for high-impact objectives:")
                
                for obj in high_impact_objs:
                    st.markdown(f"**{obj}**")
                    if obj == "Schedule":
                        st.markdown("- Develop contingency plans for schedule delays")
                        st.markdown("- Add buffer time to critical path activities")
                        st.markdown("- Identify acceleration opportunities for critical activities")
                    elif obj == "Budget":
                        st.markdown("- Establish budget reserves (recommended: 15-20% of total budget)")
                        st.markdown("- Identify cost-saving opportunities")
                        st.markdown("- Implement stricter cost control measures")
                    elif obj == "Scope":
                        st.markdown("- Strengthen change control processes")
                        st.markdown("- Clarify scope boundaries with stakeholders")
                        st.markdown("- Prioritize requirements to identify potential scope reduction if needed")
                    elif obj == "Quality":
                        st.markdown("- Enhance quality assurance processes")
                        st.markdown("- Increase testing coverage")
                        st.markdown("- Implement additional quality control checkpoints")
                    elif obj == "Resources":
                        st.markdown("- Identify backup resources for critical roles")
                        st.markdown("- Cross-train team members")
                        st.markdown("- Develop contingency staffing plans")
            else:
                st.success("No objectives are at high risk level. Continue with regular risk monitoring.")

def show_mitigation_strategies(project_data):
    """Display risk mitigation strategies and effectiveness simulation."""
    st.markdown("### Mitigation Strategy Analysis")
    st.write("Evaluate the effectiveness of different risk mitigation strategies.")
    
    # Get project risks
    risks = project_data.get('risks', [])
    
    if not risks:
        st.warning("No risks found in the project. Please add risks to the RAID log first.")
        return
    
    # Select a risk to analyze
    risk_options = [risk.get('description', f"Risk {i+1}") for i, risk in enumerate(risks)]
    
    selected_risk_desc = st.selectbox(
        "Select a Risk to Analyze",
        risk_options
    )
    
    # Find the selected risk
    selected_risk = next((r for r in risks if r.get('description', '') == selected_risk_desc), None)
    
    if not selected_risk:
        st.error("Selected risk not found.")
        return
    
    # Display risk details
    st.markdown(f"#### Selected Risk: {selected_risk_desc}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Severity", selected_risk.get('severity', 'Unknown'))
    with col2:
        st.metric("Probability", selected_risk.get('probability', 'Unknown'))
    with col3:
        st.metric("Impact", selected_risk.get('impact', 'Unknown'))
    
    # Current mitigation strategy
    current_mitigation = selected_risk.get('mitigation', 'No mitigation strategy defined')
    
    st.markdown("#### Current Mitigation Strategy")
    st.write(current_mitigation)
    
    # Define alternative mitigation strategies
    st.markdown("#### Alternative Mitigation Strategies")
    
    # Generate sample alternative strategies
    alternative_strategies = generate_alternative_strategies(selected_risk)
    
    # Allow user to edit or add strategies
    strategies_text = st.text_area(
        "Edit or Add Mitigation Strategies (one per line)", 
        value="\n".join(alternative_strategies),
        height=150
    )
    
    # Parse strategies from text area
    strategies = [s.strip() for s in strategies_text.split("\n") if s.strip()]
    
    # Strategy effectiveness estimation
    st.markdown("#### Strategy Effectiveness Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        probability_reduction = st.slider(
            "Probability Reduction Potential (%)", 
            min_value=0, 
            max_value=100, 
            value=50, 
            step=5
        )
    
    with col2:
        impact_reduction = st.slider(
            "Impact Reduction Potential (%)", 
            min_value=0, 
            max_value=100, 
            value=30, 
            step=5
        )
    
    # Cost of implementation
    implementation_costs = []
    st.markdown("#### Implementation Costs")
    
    for i, strategy in enumerate(strategies):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**Strategy {i+1}:** {strategy}")
        with col2:
            cost = st.number_input(
                f"Cost ($)",
                min_value=0,
                max_value=1000000,
                value=random.randint(5000, 50000),
                step=1000,
                key=f"cost_{i}"
            )
            implementation_costs.append(cost)
    
    # Run effectiveness simulation button
    if st.button("Simulate Mitigation Effectiveness"):
        with st.spinner("Simulating mitigation effectiveness..."):
            # Get initial risk score
            initial_score = calculate_risk_score(selected_risk)
            
            # Simulate effectiveness of each strategy
            simulation_results = []
            
            for i, strategy in enumerate(strategies):
                # Randomize effectiveness within the specified range
                prob_effectiveness = (probability_reduction / 100) * (0.8 + 0.4 * random.random())
                impact_effectiveness = (impact_reduction / 100) * (0.8 + 0.4 * random.random())
                
                # Calculate new risk score
                new_prob = convert_level_to_score(selected_risk.get('probability', 'Medium')) * (1 - prob_effectiveness)
                new_impact = convert_level_to_score(selected_risk.get('impact', 'Medium')) * (1 - impact_effectiveness)
                new_score = new_prob * new_impact
                
                # Calculate reduction percentage
                reduction = (initial_score - new_score) / initial_score * 100
                
                # Calculate cost-effectiveness ratio (reduction per $1000)
                cost_effectiveness = reduction / (implementation_costs[i] / 1000) if implementation_costs[i] > 0 else 0
                
                simulation_results.append({
                    'strategy': strategy,
                    'initial_score': initial_score,
                    'new_score': new_score,
                    'reduction_percent': reduction,
                    'cost': implementation_costs[i],
                    'cost_effectiveness': cost_effectiveness
                })
            
            # Sort by cost-effectiveness
            simulation_results.sort(key=lambda x: x['cost_effectiveness'], reverse=True)
            
            # Display results
            st.markdown("#### Simulation Results")
            
            # Create results dataframe
            results_df = pd.DataFrame(simulation_results)
            results_df.columns = ['Strategy', 'Initial Risk Score', 'New Risk Score', 
                                 'Reduction (%)', 'Cost ($)', 'Cost-Effectiveness']
            
            # Format dataframe values
            results_df['Initial Risk Score'] = results_df['Initial Risk Score'].map(lambda x: f"{x:.1f}")
            results_df['New Risk Score'] = results_df['New Risk Score'].map(lambda x: f"{x:.1f}")
            results_df['Reduction (%)'] = results_df['Reduction (%)'].map(lambda x: f"{x:.1f}%")
            results_df['Cost ($)'] = results_df['Cost ($)'].map(lambda x: f"${x:,.0f}")
            results_df['Cost-Effectiveness'] = results_df['Cost-Effectiveness'].map(lambda x: f"{x:.3f}")
            
            st.dataframe(results_df, use_container_width=True)
            
            # Display effectiveness chart
            fig = go.Figure()
            
            # Add bar for each strategy
            for i, result in enumerate(simulation_results):
                fig.add_trace(go.Bar(
                    x=[result['strategy']],
                    y=[result['reduction_percent']],
                    name=f"Strategy {i+1}",
                    text=[f"{result['reduction_percent']:.1f}%"],
                    textposition='auto'
                ))
            
            fig.update_layout(
                title='Risk Reduction by Mitigation Strategy',
                xaxis_title='Strategy',
                yaxis_title='Risk Reduction (%)',
                barmode='group'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Cost vs. Effectiveness chart
            fig2 = px.scatter(
                x=[result['cost'] for result in simulation_results],
                y=[result['reduction_percent'] for result in simulation_results],
                text=[f"S{i+1}" for i in range(len(simulation_results))],
                labels={'x': 'Implementation Cost ($)', 'y': 'Risk Reduction (%)'},
                title='Cost vs. Effectiveness'
            )
            
            # Add size representing cost-effectiveness
            fig2.update_traces(
                marker=dict(
                    size=[result['cost_effectiveness'] * 5 + 10 for result in simulation_results],
                    color='#4CAF50'
                ),
                textposition='top center'
            )
            
            # Add line for optimal cost-effectiveness
            max_ce = max(result['cost_effectiveness'] for result in simulation_results)
            max_ce_result = next(result for result in simulation_results if result['cost_effectiveness'] == max_ce)
            
            fig2.add_shape(
                type="line",
                x0=0, y0=0,
                x1=max_ce_result['cost'], y1=max_ce_result['reduction_percent'],
                line=dict(color="red", width=2, dash="dash")
            )
            
            st.plotly_chart(fig2, use_container_width=True)
            
            # Recommendation
            st.markdown("#### Recommendation")
            
            best_strategy = simulation_results[0]
            st.success(f"**Recommended Strategy:** {best_strategy['strategy']}")
            st.markdown(f"This strategy offers the best balance of risk reduction ({best_strategy['reduction_percent']:.1f}%) and cost (${best_strategy['cost']:,.0f}).")
            st.markdown(f"Cost-effectiveness ratio: {best_strategy['cost_effectiveness']:.3f} (% reduction per $1,000 spent)")

def run_monte_carlo_simulation(tasks, uncertainty, num_iterations):
    """
    Run a Monte Carlo simulation for project schedule.
    
    Args:
        tasks: List of task dictionaries
        uncertainty: Uncertainty factor for task durations (e.g., 0.2 for 20%)
        num_iterations: Number of simulation iterations
    
    Returns:
        Dictionary with simulation results
    """
    # Get the baseline schedule
    baseline_start = datetime.datetime.now()
    
    # Calculate baseline durations and dependencies
    baseline_durations = {i: task.get('duration', 0) for i, task in enumerate(tasks)}
    
    # For now, we'll use a simplified model without dependencies
    # In a real implementation, we would respect task dependencies
    
    # Run simulations
    simulation_durations = []
    simulation_completion_dates = []
    
    for _ in range(num_iterations):
        # Apply uncertainty to each task duration
        simulated_durations = {}
        
        for i, base_duration in baseline_durations.items():
            # Apply triangular distribution for duration uncertainty
            min_duration = base_duration * (1 - uncertainty)
            max_duration = base_duration * (1 + uncertainty)
            
            # Random duration between min and max, with base as most likely
            simulated_durations[i] = random.triangular(min_duration, max_duration, base_duration)
        
        # Calculate total project duration
        # In a real implementation, we would calculate based on the critical path
        total_duration = sum(simulated_durations.values())
        
        # Calculate completion date
        completion_date = baseline_start + timedelta(days=total_duration)
        
        # Store results
        simulation_durations.append(total_duration)
        simulation_completion_dates.append(completion_date)
    
    return {
        'durations': simulation_durations,
        'completion_dates': simulation_completion_dates
    }

def analyze_risk_impacts(risks, objectives):
    """
    Analyze the impact of risks on project objectives.
    
    Args:
        risks: List of risk dictionaries
        objectives: List of objectives to analyze
    
    Returns:
        Dictionary with analysis results
    """
    # Create impact matrix
    impact_matrix = []
    risk_scores = []
    
    for risk in risks:
        risk_name = risk.get('description', 'Unknown Risk')
        severity = risk.get('severity', 'Medium').lower()
        probability = risk.get('probability', 'Medium').lower()
        
        # Convert severity and probability to numeric values
        severity_score = convert_level_to_score(severity)
        probability_score = convert_level_to_score(probability)
        
        # Base risk score
        base_score = severity_score * probability_score
        
        # Generate impact levels for each objective
        impact_row = {'Risk': risk_name}
        objective_scores = []
        
        for objective in objectives:
            # Simulate different impact distributions based on risk type
            risk_category = risk.get('category', '').lower()
            
            # Adjust impact based on risk category and objective
            impact_level = generate_impact_level(risk_category, objective, base_score)
            impact_row[objective] = impact_level
            
            # Convert impact level to score for radar chart
            impact_score = convert_level_to_score(impact_level.lower())
            objective_scores.append(impact_score * 10 / 3)  # Scale to 0-10
        
        impact_matrix.append(impact_row)
        risk_scores.append({
            'risk': risk_name,
            'objectives': objectives,
            'scores': objective_scores
        })
    
    # Calculate combined impact by objective
    combined_impact = {'objectives': objectives, 'impact_scores': []}
    
    for objective in objectives:
        # Get impact levels for this objective across all risks
        impact_levels = [row[objective].lower() for row in impact_matrix]
        
        # Convert to scores and calculate weighted sum
        impact_scores = [convert_level_to_score(level) for level in impact_levels]
        combined_score = sum(impact_scores) / len(impact_scores) * 10 / 3  # Scale to 0-10
        
        combined_impact['impact_scores'].append(combined_score)
    
    return {
        'impact_matrix': impact_matrix,
        'risk_scores': risk_scores,
        'combined_impact': combined_impact
    }

def generate_alternative_strategies(risk):
    """
    Generate alternative mitigation strategies for a risk.
    
    Args:
        risk: Risk dictionary
    
    Returns:
        List of alternative strategies
    """
    risk_category = risk.get('category', '').lower()
    
    # Generic strategies
    generic_strategies = [
        "Accept the risk and monitor closely",
        "Develop contingency plan to implement if risk occurs",
        "Transfer risk to third party or insurance"
    ]
    
    # Category-specific strategies
    category_strategies = {
        'technical': [
            "Conduct technical proof of concept",
            "Implement more rigorous testing procedures",
            "Bring in technical expert consultant"
        ],
        'schedule': [
            "Add buffer time to critical path activities",
            "Implement fast-tracking for critical activities",
            "Add additional resources to key activities"
        ],
        'cost': [
            "Establish cost contingency reserve",
            "Implement stricter cost control measures",
            "Identify alternative lower-cost approaches"
        ],
        'resource': [
            "Cross-train team members for key roles",
            "Identify and onboard backup resources",
            "Redistribute workload across the team"
        ],
        'scope': [
            "Implement stricter change control process",
            "Clarify scope boundaries with stakeholders",
            "Prioritize requirements to identify potential scope reduction"
        ],
        'quality': [
            "Enhance quality assurance processes",
            "Implement additional quality control checkpoints",
            "Increase testing coverage and depth"
        ],
        'external': [
            "Develop partnerships with alternative vendors",
            "Establish contractual safeguards",
            "Develop influence strategies for external stakeholders"
        ]
    }
    
    # Get strategies for the specific risk category
    specific_strategies = category_strategies.get(risk_category, [])
    
    # Start with current mitigation if available
    current_mitigation = risk.get('mitigation', '')
    strategies = [current_mitigation] if current_mitigation else []
    
    # Add category-specific strategies
    strategies.extend(specific_strategies)
    
    # Add generic strategies
    strategies.extend(generic_strategies)
    
    # Remove empty strings and duplicates
    return list(dict.fromkeys(s for s in strategies if s))

def calculate_risk_score(risk):
    """
    Calculate a numeric risk score based on probability and impact.
    
    Args:
        risk: Risk dictionary
    
    Returns:
        Numeric risk score (1-9)
    """
    probability = convert_level_to_score(risk.get('probability', 'Medium'))
    impact = convert_level_to_score(risk.get('impact', 'Medium'))
    
    return probability * impact

def convert_level_to_score(level):
    """
    Convert a text level to a numeric score.
    
    Args:
        level: Text level (low, medium, high)
    
    Returns:
        Numeric score (1-3)
    """
    level_lower = level.lower()
    
    if level_lower in ['high', 'h']:
        return 3
    elif level_lower in ['medium', 'med', 'm']:
        return 2
    elif level_lower in ['low', 'l']:
        return 1
    else:
        return 2  # Default to medium if unknown

def generate_impact_level(risk_category, objective, base_score):
    """
    Generate an impact level for a specific objective based on risk category.
    
    Args:
        risk_category: Category of the risk
        objective: Project objective
        base_score: Base risk score
        
    Returns:
        Impact level (Low, Medium, High)
    """
    # Define impact probabilities based on risk category and objective
    # This simulates how different risk types impact different objectives
    category_impact = {
        'technical': {
            'Schedule': 0.7,
            'Budget': 0.5,
            'Scope': 0.3,
            'Quality': 0.8,
            'Resources': 0.4
        },
        'schedule': {
            'Schedule': 0.9,
            'Budget': 0.6,
            'Scope': 0.3,
            'Quality': 0.4,
            'Resources': 0.5
        },
        'cost': {
            'Schedule': 0.4,
            'Budget': 0.9,
            'Scope': 0.5,
            'Quality': 0.3,
            'Resources': 0.6
        },
        'resource': {
            'Schedule': 0.7,
            'Budget': 0.5,
            'Scope': 0.3,
            'Quality': 0.6,
            'Resources': 0.9
        },
        'scope': {
            'Schedule': 0.6,
            'Budget': 0.7,
            'Scope': 0.9,
            'Quality': 0.5,
            'Resources': 0.4
        },
        'quality': {
            'Schedule': 0.5,
            'Budget': 0.4,
            'Scope': 0.3,
            'Quality': 0.9,
            'Resources': 0.4
        },
        'external': {
            'Schedule': 0.7,
            'Budget': 0.6,
            'Scope': 0.5,
            'Quality': 0.4,
            'Resources': 0.6
        }
    }
    
    # Get default impact probability
    default_impact = {
        'Schedule': 0.6,
        'Budget': 0.6,
        'Scope': 0.5,
        'Quality': 0.5,
        'Resources': 0.5
    }
    
    # Get the impact probability for this category and objective
    category_impacts = category_impact.get(risk_category, default_impact)
    impact_prob = category_impacts.get(objective, 0.5)
    
    # Adjust by base score and random factor
    adjusted_prob = impact_prob * (base_score / 4.5) * (0.8 + 0.4 * random.random())
    
    # Convert to impact level
    if adjusted_prob > 0.66:
        return "High"
    elif adjusted_prob > 0.33:
        return "Medium"
    else:
        return "Low"