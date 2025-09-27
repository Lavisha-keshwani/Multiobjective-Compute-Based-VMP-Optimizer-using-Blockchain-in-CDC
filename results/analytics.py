from dash import register_page, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from results.dashboard import COLORS, CUSTOM_STYLE, df

register_page(__name__, path='/analytics')

def create_baseline_comparison():
    """Create comparison graphs with baseline methods"""
    baseline_data = pd.DataFrame({
        'Method': ['First-Fit', 'BFD', 'DVFS', 'PABFD', 'Our NSGA-II'],
        'Energy_Reduction': [10, 15, 18, 20, 25],
        'Carbon_Reduction': [5, 12, 15, 18, 30],
        'SLA_Compliance': [85, 88, 90, 92, 95],
        'Resource_Utilization': [70, 75, 78, 80, 85],
        'Cost_Savings': [5, 10, 12, 15, 20]
    })

    # Multi-objective comparison radar chart
    radar_fig = go.Figure()
    categories = ['Energy', 'Carbon', 'SLA', 'Resource', 'Cost']
    
    methods = ['First-Fit', 'BFD', 'DVFS', 'PABFD', 'Our NSGA-II']
    values = {
        'First-Fit': [10, 5, 85, 70, 5],
        'BFD': [15, 12, 88, 75, 10],
        'DVFS': [18, 15, 90, 78, 12],
        'PABFD': [20, 18, 92, 80, 15],
        'Our NSGA-II': [25, 30, 95, 85, 20]
    }
    
    for method in methods:
        radar_fig.add_trace(go.Scatterpolar(
            r=values[method],
            theta=categories,
            fill='toself',
            name=method
        ))
    
    radar_fig.update_layout(**CUSTOM_STYLE['graph'])

    # Bar comparison
    bar_fig = go.Figure()
    metrics = ['Energy_Reduction', 'Carbon_Reduction', 'SLA_Compliance']
    for metric in metrics:
        bar_fig.add_trace(go.Bar(
            name=metric,
            x=baseline_data['Method'],
            y=baseline_data[metric],
            text=baseline_data[metric],
            textposition='auto',
        ))
    
    bar_fig.update_layout(
        barmode='group',
        title='Performance Comparison Across Methods',
        **CUSTOM_STYLE['graph']
    )

    # Line comparison
    line_fig = go.Figure()
    x_points = [20, 40, 60, 80, 100]  # Load percentages
    
    # Sample data for each method
    method_data = {
        'First-Fit': [10, 15, 25, 35, 45],
        'BFD': [12, 18, 28, 38, 48],
        'DVFS': [15, 22, 32, 42, 52],
        'PABFD': [18, 25, 35, 45, 55],
        'Our NSGA-II': [20, 30, 40, 50, 60]
    }
    
    for method, values in method_data.items():
        line_fig.add_trace(go.Scatter(
            x=x_points,
            y=values,
            mode='lines+markers',
            name=method
        ))
    
    line_fig.update_layout(
        title='Performance Scaling with Load',
        xaxis_title='Load (%)',
        yaxis_title='Performance',
        **CUSTOM_STYLE['graph']
    )

    return radar_fig, bar_fig, line_fig

def create_analytics_layout():
    # Add baseline comparison data
    baseline_data = pd.DataFrame({
        'Method': ['First-Fit', 'BFD', 'DVFS', 'PABFD', 'Our NSGA-II'],
        'Energy_Reduction': [10, 15, 18, 20, 25],
        'Carbon_Reduction': [5, 12, 15, 18, 30],
        'SLA_Compliance': [85, 88, 90, 92, 95],
        'Resource_Utilization': [70, 75, 78, 80, 85]
    })

    # Header
    header = html.Div([
        html.H1("Detailed Analytics",
               style={'color': COLORS['text'], 'textAlign': 'center'}),
        html.Hr(style={'borderColor': COLORS['primary']})
    ], style=CUSTOM_STYLE['header'])

    # Performance Metrics Graph
    performance_metrics_graph = dbc.Col([
        dbc.Card([
            dbc.CardHeader([
                html.I(className="fas fa-tachometer-alt me-2"),
                "Performance Metrics"
            ], style={'background': COLORS['card'], 'color': COLORS['primary']}),
            dbc.CardBody([
                dcc.Graph(
                    figure=go.Figure([
                        go.Indicator(
                            mode="gauge+number",
                            value=df['Energy'].mean(),
                            title={'text': "Avg Energy"},
                            gauge={'axis': {'range': [0, df['Energy'].max()]}}
                        )
                    ]).update_layout(**CUSTOM_STYLE['graph'])
                )
            ])
        ], style=CUSTOM_STYLE['card'])
    ], width=6)

    # Resource Usage Graph
    resource_usage_graph = dbc.Col([
        dbc.Card([
            dbc.CardHeader([
                html.I(className="fas fa-server me-2"),
                "Resource Usage"
            ], style={'background': COLORS['card'], 'color': COLORS['success']}),
            dbc.CardBody([
                dcc.Graph(
                    figure=px.bar(
                        df, x='method', y=['Energy', 'SLA'],
                        barmode='group',
                        title="Resource Usage by Method"
                ).update_layout(**CUSTOM_STYLE['graph'])
                )
            ])
        ], style=CUSTOM_STYLE['card'])
    ], width=6)

    # Time Series Analysis Graph
    time_series_graph = dbc.Col([
        dbc.Card([
            dbc.CardHeader([
                html.I(className="fas fa-chart-line me-2"),
                "Time Series Analysis"
            ], style={'background': COLORS['card'], 'color': COLORS['info']}),
            dbc.CardBody([
                dcc.Graph(
                    figure=go.Figure([
                        go.Scatter(
                            x=df.index,
                            y=df['Energy'],
                            mode='lines+markers',
                            name='Energy'
                        )
                    ]).update_layout(**CUSTOM_STYLE['graph'])
                )
            ])
        ], style=CUSTOM_STYLE['card'])
    ], width=12)

    # Add Baseline Comparison Section
    radar_fig, bar_fig, line_fig = create_baseline_comparison()
    
    baseline_section = html.Div([
        html.H2("Baseline Method Comparison", 
                style={'color': COLORS['text'], 'textAlign': 'center', 'margin': '30px 0'}),
        
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-spider me-2"),
                    "Multi-objective Comparison"
                ], style={'background': COLORS['card'], 'color': COLORS['text']}),
                dbc.CardBody(dcc.Graph(figure=radar_fig))
            ], style=CUSTOM_STYLE['card']), width=12),
        ], className='mb-4'),

        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-chart-bar me-2"),
                    "Performance Metrics"
                ], style={'background': COLORS['card'], 'color': COLORS['text']}),
                dbc.CardBody(dcc.Graph(figure=bar_fig))
            ], style=CUSTOM_STYLE['card']), width=6),
            
            dbc.Col(dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-chart-line me-2"),
                    "Scaling Analysis"
                ], style={'background': COLORS['card'], 'color': COLORS['text']}),
                dbc.CardBody(dcc.Graph(figure=line_fig))
            ], style=CUSTOM_STYLE['card']), width=6),
        ], className='mb-4'),

        # Method descriptions
        dbc.Card([
            dbc.CardHeader([
                html.I(className="fas fa-info-circle me-2"),
                "Method Comparison Details"
            ], style={'background': COLORS['card'], 'color': COLORS['text']}),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H5("First Fit / Round Robin", className="text-primary"),
                        html.P("Simple heuristic that allocates VMs to the first available host. Fast but ignores energy and carbon intensity.", 
                              className="text-muted mb-4"),
                        html.H5("Best Fit Decreasing (BFD)", className="text-primary"),
                        html.P("Resource packing heuristic optimizing for consolidated usage. Energy-aware but blind to carbon intensity.",
                              className="text-muted"),
                    ], width=6),
                    dbc.Col([
                        html.H5("DVFS", className="text-primary"),
                        html.P("Dynamic voltage/frequency scaling at host level. Reduces power but cannot optimize placement location.",
                              className="text-muted mb-4"),
                        html.H5("Power-aware BFD (PABFD)", className="text-primary"),
                        html.P("Enhanced BFD with power optimization. Single-objective focused without multi-objective capabilities.",
                              className="text-muted"),
                    ], width=6),
                ])
            ])
        ], style=CUSTOM_STYLE['card'])
    ])

    # Insert baseline section before final statistics card
    layout_children = layout.children[:-1] + [baseline_section] + [layout.children[-1]]
    layout.children = layout_children

    return layout

layout = create_analytics_layout()
                        html.H5("Power-aware BFD", className="text-primary"),
                        html.P("Enhanced BFD with power optimization. Single-objective focused, "
                              "cannot handle multi-objective tradeoffs.",
                              className="text-muted"),
                    ], width=6),
                ]),
            ])
        ], style=CUSTOM_STYLE['card']),

        # Performance Metrics Section
        dbc.Row([
            # Original Performance Metrics
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Key Performance Indicators"),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=px.bar(baseline_data, x='Method', 
                                        y=['Energy_Reduction', 'SLA_Compliance', 'Resource_Utilization'],
                                        title='Performance Comparison',
                                        barmode='group')
                            .update_layout(**CUSTOM_STYLE['graph'])
                        )
                    ])
                ], style=CUSTOM_STYLE['card'])
            ], width=12),
        ], className='mb-4'),

        # Method Comparison Section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Comparison with Existing Solutions"),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=px.line(baseline_data, x='Method', 
                                         y=['Energy_Reduction', 'Carbon_Reduction'],
                                         title='Energy and Carbon Reduction by Method',
                                         markers=True)
                            .update_layout(**CUSTOM_STYLE['graph'])
                        )
                    ])
                ], style=CUSTOM_STYLE['card'])
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Solution Effectiveness"),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=go.Figure(data=[
                                go.Scatterpolar(
                                    r=[25, 30, 95, 85, 90],
                                    theta=['Energy', 'Carbon', 'SLA', 'Resource', 'Adaptation'],
                                    fill='toself',
                                    name='Our Solution'
                                ),
                                go.Scatterpolar(
                                    r=[15, 18, 88, 75, 70],
                                    theta=['Energy', 'Carbon', 'SLA', 'Resource', 'Adaptation'],
                                    fill='toself',
                                    name='Best Baseline'
                                )
                            ]).update_layout(**CUSTOM_STYLE['graph'])
                        )
                    ])
                ], style=CUSTOM_STYLE['card'])
            ], width=6)
        ], className='mb-4'),

        # Time Series Analysis
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Performance Over Time"),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=px.scatter(df, x='index', y=['Energy', 'SLA'],
                                            title='Metrics Evolution',
                                            trendline="lowess")
                            .update_layout(**CUSTOM_STYLE['graph'])
                        )
                    ])
                ], style=CUSTOM_STYLE['card'])
            ], width=12)
        ], className='mb-4'),

        # Method Descriptions
        dbc.Card([
            dbc.CardHeader("Baseline Methods Analysis"),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H5("First Fit / Round Robin"),
                        html.P("Simple heuristic approach. Fast but ignores energy and carbon."),
                        html.H5("Best Fit Decreasing (BFD)"),
                        html.P("Resource packing heuristic. Energy-aware but blind to carbon.")
                    ], width=6),
                    dbc.Col([
                        html.H5("DVFS"),
                        html.P("Dynamic voltage/frequency scaling. Reduces power but not placement."),
                        html.H5("Power-aware BFD"),
                        html.P("Enhanced BFD with power focus. Single-objective optimization.")
                    ], width=6)
                ])
            ])
        ], style=CUSTOM_STYLE['card']),

        # Statistical Summary
        dbc.Card([
            dbc.CardHeader("Statistical Summary"),
            dbc.CardBody([
                html.Div([
                    html.H5("Energy Reduction Statistics", className="text-primary"),
                    html.P(f"Mean: {baseline_data['Energy_Reduction'].mean():.2f}%",
                           className="text-muted"),
                    html.P(f"Standard Deviation: {baseline_data['Energy_Reduction'].std():.2f}%",
                           className="text-muted"),
                    html.P(f"Minimum: {baseline_data['Energy_Reduction'].min():.2f}%, "
                           f"Maximum: {baseline_data['Energy_Reduction'].max():.2f}%",
                           className="text-muted"),
                ], className="mb-4"),
                
                html.Div([
                    html.H5("Carbon Reduction Statistics", className="text-primary"),
                    html.P(f"Mean: {baseline_data['Carbon_Reduction'].mean():.2f}%",
                           className="text-muted"),
                    html.P(f"Standard Deviation: {baseline_data['Carbon_Reduction'].std():.2f}%",
                           className="text-muted"),
                    html.P(f"Minimum: {baseline_data['Carbon_Reduction'].min():.2f}%, "
                           f"Maximum: {baseline_data['Carbon_Reduction'].max():.2f}%",
                           className="text-muted"),
                ], className="mb-4"),
                
                html.Div([
                    html.H5("SLA Compliance Statistics", className="text-primary"),
                    html.P(f"Mean: {baseline_data['SLA_Compliance'].mean():.2f}%",
                           className="text-muted"),
                    html.P(f"Standard Deviation: {baseline_data['SLA_Compliance'].std():.2f}%",
                           className="text-muted"),
                    html.P(f"Minimum: {baseline_data['SLA_Compliance'].min():.2f}%, "
                           f"Maximum: {baseline_data['SLA_Compliance'].max():.2f}%",
                           className="text-muted"),
                ], className="mb-4"),
                
                html.Div([
                    html.H5("Resource Utilization Statistics", className="text-primary"),
                    html.P(f"Mean: {baseline_data['Resource_Utilization'].mean():.2f}%",
                           className="text-muted"),
                    html.P(f"Standard Deviation: {baseline_data['Resource_Utilization'].std():.2f}%",
                           className="text-muted"),
                    html.P(f"Minimum: {baseline_data['Resource_Utilization'].min():.2f}%, "
                           f"Maximum: {baseline_data['Resource_Utilization'].max():.2f}%",
                           className="text-muted"),
                ], className="mb-4"),
                
                html.Div([
                    html.H5("Adaptation Score Statistics", className="text-primary"),
                    html.P(f"Mean: {baseline_data['Adaptation_Score'].mean():.2f}%",
                           className="text-muted"),
                    html.P(f"Standard Deviation: {baseline_data['Adaptation_Score'].std():.2f}%",
                           className="text-muted"),
                    html.P(f"Minimum: {baseline_data['Adaptation_Score'].min():.2f}%, "
                           f"Maximum: {baseline_data['Adaptation_Score'].max():.2f}%",
                           className="text-muted"),
                ], className="mb-4"),
            ])
        ], style=CUSTOM_STYLE['card']),
    ], style=CUSTOM_STYLE['container'])

    return layout

layout = create_analytics_layout()
