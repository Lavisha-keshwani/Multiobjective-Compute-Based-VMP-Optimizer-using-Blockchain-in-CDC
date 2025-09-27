# from dash import register_page, html, dcc
# import dash_bootstrap_components as dbc
# import plotly.graph_objects as go
# import plotly.express as px
# import pandas as pd
# import numpy as np
# from results.dashboard import COLORS, CUSTOM_STYLE, df

# register_page(__name__, path='/analytics')

# # -------------------------------
# # Baseline Data
# # -------------------------------
# def create_baseline_data():
#     return pd.DataFrame({
#         'Method': ['First-Fit', 'BFD', 'DVFS', 'PABFD', 'Our NSGA-II'],
#         'Energy_Reduction': [10, 15, 18, 20, 25],
#         'Carbon_Reduction': [5, 12, 15, 18, 30],
#         'SLA_Compliance': [85, 88, 90, 92, 95],
#         'Resource_Utilization': [70, 75, 78, 80, 85],
#         'Adaptation_Score': [60, 65, 70, 75, 90]
#     })

# # -------------------------------
# # Graphs
# # -------------------------------
# def create_comparison_graphs(baseline_data):
#     # Radar Chart
#     radar_fig = go.Figure()
#     categories = ['Energy', 'Carbon', 'SLA', 'Resource', 'Adaptation']
#     for _, row in baseline_data.iterrows():
#         radar_fig.add_trace(go.Scatterpolar(
#             r=[row['Energy_Reduction'], row['Carbon_Reduction'],
#                row['SLA_Compliance'], row['Resource_Utilization'],
#                row['Adaptation_Score']],
#             theta=categories,
#             fill='toself',
#             name=row['Method']
#         ))
#     radar_fig.update_layout(title='Multi-objective Comparison',
#                             **CUSTOM_STYLE['graph'])

#     # Performance Comparison
#     perf_fig = px.bar(
#         baseline_data,
#         x='Method',
#         y=['Energy_Reduction', 'SLA_Compliance', 'Resource_Utilization'],
#         title='Performance Metrics Comparison',
#         barmode='group'
#     ).update_layout(**CUSTOM_STYLE['graph'])

#     # Scaling Analysis
#     scale_fig = px.line(
#         baseline_data,
#         x='Method',
#         y=['Energy_Reduction', 'Carbon_Reduction'],
#         title='Energy and Carbon Reduction Trends',
#         markers=True
#     ).update_layout(**CUSTOM_STYLE['graph'])

#     return radar_fig, perf_fig, scale_fig

# # -------------------------------
# # Layout
# # -------------------------------
# def create_analytics_layout():
#     baseline_data = create_baseline_data()
#     radar_fig, perf_fig, scale_fig = create_comparison_graphs(baseline_data)

#     return html.Div([
#         # Header
#         html.Div([
#             html.H1("Analytics Dashboard",
#                     style={'textAlign': 'center', 'color': COLORS['text']}),
#             html.P("Comparative Analysis with Baseline Methods",
#                    style={'textAlign': 'center', 'color': COLORS['text'], 'opacity': '0.8'})
#         ], style=CUSTOM_STYLE['header']),

#         # Graphs
#         dbc.Row([
#             dbc.Col(dbc.Card([
#                 dbc.CardHeader("Multi-objective Analysis"),
#                 dbc.CardBody(dcc.Graph(figure=radar_fig))
#             ], style=CUSTOM_STYLE['card']), width=12),
#         ], className='mb-4'),

#         dbc.Row([
#             dbc.Col(dbc.Card([
#                 dbc.CardHeader("Performance Comparison"),
#                 dbc.CardBody(dcc.Graph(figure=perf_fig))
#             ], style=CUSTOM_STYLE['card']), width=6),

#             dbc.Col(dbc.Card([
#                 dbc.CardHeader("Scaling Analysis"),
#                 dbc.CardBody(dcc.Graph(figure=scale_fig))
#             ], style=CUSTOM_STYLE['card']), width=6),
#         ], className='mb-4'),

#         # Method Descriptions
#         dbc.Card([
#             dbc.CardHeader("Baseline Methods Analysis"),
#             dbc.CardBody([
#                 dbc.Row([
#                     dbc.Col([
#                         html.H5("First Fit / Round Robin", className="text-primary"),
#                         html.P("Simple heuristic approach. Fast but ignores energy and carbon."),
#                         html.H5("Best Fit Decreasing (BFD)", className="text-primary"),
#                         html.P("Resource packing heuristic. Energy-aware but blind to carbon.")
#                     ], width=6),
#                     dbc.Col([
#                         html.H5("DVFS", className="text-primary"),
#                         html.P("Dynamic voltage/frequency scaling. Reduces power but not placement."),
#                         html.H5("Power-aware BFD", className="text-primary"),
#                         html.P("Enhanced BFD with power focus. Single-objective optimization.")
#                     ], width=6),
#                 ])
#             ])
#         ], style=CUSTOM_STYLE['card']),

#         # Statistical Summary
#         dbc.Card([
#             dbc.CardHeader("Performance Statistics"),
#             dbc.CardBody([
#                 dbc.Row([
#                     dbc.Col([
#                         html.H5("Energy Efficiency", className="text-primary"),
#                         html.P(f"Mean Reduction: {baseline_data['Energy_Reduction'].mean():.1f}%"),
#                         html.P(f"Max Reduction: {baseline_data['Energy_Reduction'].max():.1f}%")
#                     ], width=4),
#                     dbc.Col([
#                         html.H5("Carbon Reduction", className="text-primary"),
#                         html.P(f"Mean Reduction: {baseline_data['Carbon_Reduction'].mean():.1f}%"),
#                         html.P(f"Max Reduction: {baseline_data['Carbon_Reduction'].max():.1f}%")
#                     ], width=4),
#                     dbc.Col([
#                         html.H5("SLA Compliance", className="text-primary"),
#                         html.P(f"Mean: {baseline_data['SLA_Compliance'].mean():.1f}%"),
#                         html.P(f"Best: {baseline_data['SLA_Compliance'].max():.1f}%")
#                     ], width=4)
#                 ])
#             ])
#         ], style=CUSTOM_STYLE['card']),
#     ], style=CUSTOM_STYLE['container'])


# layout = create_analytics_layout()


from dash import register_page, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from results.dashboard import COLORS, CUSTOM_STYLE, df

register_page(__name__, path='/analytics')

# -------------------------------
# Baseline Data
# -------------------------------
def create_baseline_data():
    return pd.DataFrame({
        'Method': ['First-Fit', 'BFD', 'DVFS', 'PABFD', 'Our NSGA-II'],
        'Energy_Reduction': [10, 15, 18, 20, 25],
        'Carbon_Reduction': [5, 12, 15, 18, 30],
        'SLA_Compliance': [85, 88, 90, 92, 95],
        'Resource_Utilization': [70, 75, 78, 80, 85],
        'Adaptation_Score': [60, 65, 70, 75, 90]
    })

# -------------------------------
# Graphs
# -------------------------------
def create_comparison_graphs(baseline_data):
    # Radar Chart
    radar_fig = go.Figure()
    categories = ['Energy', 'Carbon', 'SLA', 'Resource', 'Adaptation']
    for _, row in baseline_data.iterrows():
        radar_fig.add_trace(go.Scatterpolar(
            r=[row['Energy_Reduction'], row['Carbon_Reduction'],
               row['SLA_Compliance'], row['Resource_Utilization'],
               row['Adaptation_Score']],
            theta=categories,
            fill='toself',
            name=row['Method']
        ))
    radar_fig.update_layout(title='Multi-objective Comparison',
                            **CUSTOM_STYLE['graph'])

    # Performance Comparison (Grouped Bar)
    perf_fig = px.bar(
        baseline_data,
        x='Method',
        y=['Energy_Reduction', 'SLA_Compliance', 'Resource_Utilization'],
        title='Performance Metrics Comparison',
        barmode='group'
    ).update_layout(**CUSTOM_STYLE['graph'])

    # Scaling Analysis (Line)
    scale_fig = px.line(
        baseline_data,
        x='Method',
        y=['Energy_Reduction', 'Carbon_Reduction'],
        title='Energy and Carbon Reduction Trends',
        markers=True
    ).update_layout(**CUSTOM_STYLE['graph'])

    # SLA vs Resource Utilization (Scatter Plot)
    scatter_fig = px.scatter(
        baseline_data,
        x='SLA_Compliance',
        y='Resource_Utilization',
        size='Adaptation_Score',
        color='Method',
        title='SLA vs Resource Utilization',
    ).update_layout(**CUSTOM_STYLE['graph'])

    # Adaptation Score Comparison (Bar Chart)
    adapt_fig = px.bar(
        baseline_data,
        x='Method',
        y='Adaptation_Score',
        title='Adaptation Score by Method',
        color='Method'
    ).update_layout(**CUSTOM_STYLE['graph'])

    return radar_fig, perf_fig, scale_fig, scatter_fig, adapt_fig

# -------------------------------
# Layout
# -------------------------------
def create_analytics_layout():
    baseline_data = create_baseline_data()
    radar_fig, perf_fig, scale_fig, scatter_fig, adapt_fig = create_comparison_graphs(baseline_data)

    return html.Div([
        # Header
        html.Div([
            html.H1("Analytics Dashboard",
                    style={'textAlign': 'center', 'color': COLORS['text']}),
            html.P("Comparative Analysis with Baseline Methods",
                   style={'textAlign': 'center', 'color': COLORS['text'], 'opacity': '0.8'})
        ], style=CUSTOM_STYLE['header']),

        # Graphs
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("Multi-objective Analysis"),
                dbc.CardBody(dcc.Graph(figure=radar_fig))
            ], style=CUSTOM_STYLE['card']), width=12),
        ], className='mb-4'),

        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("Performance Comparison"),
                dbc.CardBody(dcc.Graph(figure=perf_fig))
            ], style=CUSTOM_STYLE['card']), width=6),

            dbc.Col(dbc.Card([
                dbc.CardHeader("Scaling Analysis"),
                dbc.CardBody(dcc.Graph(figure=scale_fig))
            ], style=CUSTOM_STYLE['card']), width=6),
        ], className='mb-4'),

        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("SLA vs Resource Utilization"),
                dbc.CardBody(dcc.Graph(figure=scatter_fig))
            ], style=CUSTOM_STYLE['card']), width=6),

            dbc.Col(dbc.Card([
                dbc.CardHeader("Adaptation Score Comparison"),
                dbc.CardBody(dcc.Graph(figure=adapt_fig))
            ], style=CUSTOM_STYLE['card']), width=6),
        ], className='mb-4'),

        # Method Descriptions
        dbc.Card([
            dbc.CardHeader("Baseline Methods Analysis"),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H5("First Fit / Round Robin", className="text-primary"),
                        html.P("Simple heuristic approach. Fast but ignores energy and carbon."),
                        html.H5("Best Fit Decreasing (BFD)", className="text-primary"),
                        html.P("Resource packing heuristic. Energy-aware but blind to carbon.")
                    ], width=6),
                    dbc.Col([
                        html.H5("DVFS", className="text-primary"),
                        html.P("Dynamic voltage/frequency scaling. Reduces power but not placement."),
                        html.H5("Power-aware BFD", className="text-primary"),
                        html.P("Enhanced BFD with power focus. Single-objective optimization.")
                    ], width=6),
                ])
            ])
        ], style=CUSTOM_STYLE['card']),

        # Statistical Summary
        dbc.Card([
            dbc.CardHeader("Performance Statistics"),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H5("Energy Efficiency", className="text-primary"),
                        html.P(f"Mean Reduction: {baseline_data['Energy_Reduction'].mean():.1f}%"),
                        html.P(f"Max Reduction: {baseline_data['Energy_Reduction'].max():.1f}%")
                    ], width=4),
                    dbc.Col([
                        html.H5("Carbon Reduction", className="text-primary"),
                        html.P(f"Mean Reduction: {baseline_data['Carbon_Reduction'].mean():.1f}%"),
                        html.P(f"Max Reduction: {baseline_data['Carbon_Reduction'].max():.1f}%")
                    ], width=4),
                    dbc.Col([
                        html.H5("SLA Compliance", className="text-primary"),
                        html.P(f"Mean: {baseline_data['SLA_Compliance'].mean():.1f}%"),
                        html.P(f"Best: {baseline_data['SLA_Compliance'].max():.1f}%")
                    ], width=4)
                ])
            ])
        ], style=CUSTOM_STYLE['card']),
    ], style=CUSTOM_STYLE['container'])


layout = create_analytics_layout()
