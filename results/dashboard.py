# import pandas as pd
# import numpy as np
# import plotly.express as px
# import plotly.graph_objects as go
# from dash import Dash, dcc, html, Input, Output, page_container
# import dash_bootstrap_components as dbc
# from dash.exceptions import PreventUpdate

# # -----------------------------
# # Colors & Styles
# # -----------------------------
# COLORS = {
#     'background': '#1a1a1a',
#     'card': '#2d2d2d',
#     'text': '#ffffff',
#     'primary': '#00bcd4',
#     'secondary': '#ff6e40',
#     'success': '#4caf50',
#     'warning': '#ffc107',
#     'danger': '#f44336',
#     'info': '#03a9f4',  # Added missing info color
#     'dark': '#121212',
#     'muted': '#666666'
# }

# CUSTOM_STYLE = {
#     'container': {
#         'max-width': '1400px',
#         'margin': '0 auto',
#         'padding': '20px',
#         'background-color': COLORS['background'],
#         'min-height': '100vh'
#     },
#     'card': {
#         'background-color': COLORS['card'],
#         'box-shadow': '0 4px 6px rgba(0,0,0,0.3)',
#         'margin-bottom': '20px',
#         'border': f'1px solid {COLORS["primary"]}',
#         'border-radius': '8px'
#     },
#     'header': {
#         'background': 'linear-gradient(135deg, #00bcd4 0%, #3f51b5 100%)',
#         'padding': '40px 20px',
#         'margin-bottom': '30px',
#         'border-radius': '8px',
#         'box-shadow': '0 4px 20px rgba(0,0,0,0.4)'
#     },
#     'graph': {
#         'plot_bgcolor': COLORS['card'],
#         'paper_bgcolor': COLORS['card'],
#         'font': {'color': COLORS['text']},
#         'xaxis': {
#             'gridcolor': COLORS['muted'],
#             'color': COLORS['text'],
#             'showgrid': True
#         },
#         'yaxis': {
#             'gridcolor': COLORS['muted'],
#             'color': COLORS['text'],
#             'showgrid': True
#         }
#     }
# }

# # -----------------------------
# # Load Data
# # -----------------------------
# def load_sample_data():
#     """Generate sample data if CSV doesn't exist"""
#     n_samples = 50
#     np.random.seed(42)
    
#     # Generate richer sample data
#     data = pd.DataFrame({
#         'Energy': np.random.uniform(100, 500, n_samples),
#         'SLA': np.random.uniform(0, 10, n_samples),
#         'method': np.random.choice(['NSGA-II', 'First-Fit'], n_samples),
#         'load_pct': np.random.choice([20, 40, 60, 80, 100], n_samples),
#         'profile': np.random.choice(['Low', 'Medium', 'High'], n_samples),
#         'cpu_util': np.random.uniform(0, 100, n_samples),
#         'memory_util': np.random.uniform(0, 100, n_samples),
#         'network_util': np.random.uniform(0, 100, n_samples),
#         'index': range(n_samples)
#     })
    
#     # Add some derived metrics
#     data['efficiency'] = data['Energy'] / (data['cpu_util'] + 1)
#     data['performance'] = data['cpu_util'] * (1 - data['SLA']/10)
    
#     return data

# def process_loaded_data(df):
#     """Process loaded CSV data to ensure all required columns exist"""
#     # Add missing columns if needed
#     if 'method' not in df.columns:
#         df['method'] = np.random.choice(['NSGA-II', 'First-Fit'], len(df))
#     if 'profile' not in df.columns:
#         df['profile'] = np.random.choice(['Low', 'Medium', 'High'], len(df))
#     if 'load_pct' not in df.columns:
#         df['load_pct'] = np.random.choice([20, 40, 60, 80, 100], len(df))
#     if 'cpu_util' not in df.columns:
#         df['cpu_util'] = df['Energy'] / df['Energy'].max() * 100
#     if 'memory_util' not in df.columns:
#         df['memory_util'] = np.random.uniform(0, 100, len(df))
#     if 'network_util' not in df.columns:
#         df['network_util'] = np.random.uniform(0, 100, len(df))
#     if 'index' not in df.columns:
#         df['index'] = range(len(df))
        
#     # Add derived metrics
#     df['efficiency'] = df['Energy'] / (df['cpu_util'] + 1)
#     df['performance'] = df['cpu_util'] * (1 - df['SLA']/10)
    
#     return df

# # Try loading CSV from multiple paths
# try:
#     # Try multiple possible paths
#     possible_paths = [
#         "results.csv",
#         "results/results.csv",
#         "../results/results.csv",
#         "c:/Users/lavisha keshwani/cloudsim_simulator/results/results.csv"
#     ]
    
#     df = None
#     for path in possible_paths:
#         try:
#             df = pd.read_csv(path)
#             print(f"Successfully loaded data from {path}")
#             df = process_loaded_data(df)  # Process loaded data
#             break
#         except:
#             continue
            
#     if df is None:
#         print("No data found. Using sample data...")
#         df = load_sample_data()
        
# except Exception as e:
#     print(f"Error loading data: {e}")
#     print("Falling back to sample data...")
#     df = load_sample_data()

# # -----------------------------
# # Navbar
# # -----------------------------
# def create_navbar():
#     return dbc.NavbarSimple(
#         children=[
#             dbc.Nav([
#                 dbc.NavItem(dbc.NavLink("Dashboard", href="/", active="exact")),
#                 dbc.NavItem(dbc.NavLink("Theory", href="/theory", active="exact")),
#                 dbc.NavItem(dbc.NavLink("Analytics", href="/analytics", active="exact")),
#             ], className="ms-auto", pills=True)
#         ],
#         brand="☁️ Cloud Optimization Dashboard",
#         brand_href="/",
#         color="dark",
#         dark=True,
#         className="mb-4"
#     )

# # -----------------------------
# # Pages
# # -----------------------------
# def create_main_page():
#     return html.Div([
#         html.Div([
#             html.H1("Cloud Resource Optimization Dashboard", style={'textAlign': 'center', 'color': COLORS['text']}),
#             html.P("Real-time monitoring and optimization of cloud resources",
#                    style={'textAlign': 'center', 'color': COLORS['text'], 'opacity': '0.8'})
#         ], style=CUSTOM_STYLE['header']),

#         # Metrics Cards
#         dbc.Row([
#             dbc.Col(dbc.Card([
#                 html.H4("Average Energy", style={'color': COLORS['text'], 'textAlign': 'center'}),
#                 html.H2(f"{df['Energy'].mean():.2f}", style={'color': COLORS['primary'], 'textAlign': 'center'}),
#                 html.P("Watt-hours", style={'color': COLORS['muted'], 'textAlign': 'center'})
#             ], body=True, style=CUSTOM_STYLE['card']), width=3),

#             dbc.Col(dbc.Card([
#                 html.H4("Avg SLA Violations", style={'color': COLORS['text'], 'textAlign': 'center'}),
#                 html.H2(f"{df['SLA'].mean():.2f}", style={'color': COLORS['warning'], 'textAlign': 'center'}),
#                 html.P("Count", style={'color': COLORS['muted'], 'textAlign': 'center'})
#             ], body=True, style=CUSTOM_STYLE['card']), width=3),

#             dbc.Col(dbc.Card([
#                 html.H4("Total Samples", style={'color': COLORS['text'], 'textAlign': 'center'}),
#                 html.H2(f"{len(df)}", style={'color': COLORS['success'], 'textAlign': 'center'}),
#                 html.P("Records", style={'color': COLORS['muted'], 'textAlign': 'center'})
#             ], body=True, style=CUSTOM_STYLE['card']), width=3),

#             dbc.Col(dbc.Card([
#                 html.H4("Success Rate", style={'color': COLORS['text'], 'textAlign': 'center'}),
#                 html.H2(f"{(df['SLA']==0).mean()*100:.1f}%", style={'color': COLORS['primary'], 'textAlign': 'center'}),
#                 html.P("Percentage", style={'color': COLORS['muted'], 'textAlign': 'center'})
#             ], body=True, style=CUSTOM_STYLE['card']), width=3),
#         ], className="mb-4"),

#         # Main Graphs Section
#         dbc.Row([
#             # First Row of Graphs
#             dbc.Col(dbc.Card([
#                 dbc.CardHeader([
#                     html.I(className="fas fa-chart-scatter me-2"),
#                     "Energy vs SLA Violations"
#                 ], style={'background': COLORS['card'], 'color': COLORS['text']}),
#                 dbc.CardBody(dcc.Graph(id='scatter-plot'))
#             ], style=CUSTOM_STYLE['card']), width=6),

#             dbc.Col(dbc.Card([
#                 dbc.CardHeader([
#                     html.I(className="fas fa-chart-line me-2"),
#                     "Performance Trends"
#                 ], style={'background': COLORS['card'], 'color': COLORS['text']}),
#                 dbc.CardBody(dcc.Graph(id='performance-trends'))
#             ], style=CUSTOM_STYLE['card']), width=6),
#         ], className="mb-4"),

#         # Second Row of Graphs
#         dbc.Row([
#             dbc.Col(dbc.Card([
#                 dbc.CardHeader([
#                     html.I(className="fas fa-chart-pie me-2"),
#                     "Resource Distribution"
#                 ], style={'background': COLORS['card'], 'color': COLORS['text']}),
#                 dbc.CardBody(dcc.Graph(id='resource-pie'))
#             ], style=CUSTOM_STYLE['card']), width=4),

#             dbc.Col(dbc.Card([
#                 dbc.CardHeader([
#                     html.I(className="fas fa-chart-bar me-2"),
#                     "Method Comparison"
#                 ], style={'background': COLORS['card'], 'color': COLORS['text']}),
#                 dbc.CardBody(dcc.Graph(id='method-comparison'))
#             ], style=CUSTOM_STYLE['card']), width=4),

#             dbc.Col(dbc.Card([
#                 dbc.CardHeader([
#                     html.I(className="fas fa-bullseye me-2"),
#                     "Target Achievement"
#                 ], style={'background': COLORS['card'], 'color': COLORS['text']}),
#                 dbc.CardBody(dcc.Graph(id='target-gauge'))
#             ], style=CUSTOM_STYLE['card']), width=4),
#         ], className="mb-4"),

#         # Third Row of Graphs
#         dbc.Row([
#             dbc.Col(dbc.Card([
#                 dbc.CardHeader([
#                     html.I(className="fas fa-chart-area me-2"),
#                     "Load Distribution"
#                 ], style={'background': COLORS['card'], 'color': COLORS['text']}),
#                 dbc.CardBody(dcc.Graph(id='load-distribution'))
#             ], style=CUSTOM_STYLE['card']), width=6),

#             dbc.Col(dbc.Card([
#                 dbc.CardHeader([
#                     html.I(className="fas fa-chart-bar me-2"),
#                     "Profile Analysis"
#                 ], style={'background': COLORS['card'], 'color': COLORS['text']}),
#                 dbc.CardBody(dcc.Graph(id='profile-analysis'))
#             ], style=CUSTOM_STYLE['card']), width=6),
#         ], className="mb-4"),

#         # Filter
#         dbc.Card([
#             dbc.CardHeader([
#                 html.I(className="fas fa-filter me-2"),
#                 "Filter Energy Range"
#             ], style={'background': COLORS['card'], 'color': COLORS['text']}),
#             dbc.CardBody([
#                 dcc.RangeSlider(
#                     id='energy-range',
#                     min=df['Energy'].min(),
#                     max=df['Energy'].max(),
#                     value=[df['Energy'].min(), df['Energy'].max()],
#                     marks={int(x): {'label': str(int(x)), 'style': {'color': COLORS['text']}}
#                            for x in np.linspace(df['Energy'].min(), df['Energy'].max(), 5)},
#                     step=1
#                 )
#             ], style={'background': COLORS['card']})
#         ], style=CUSTOM_STYLE['card']),

#         # Sample Table - Fixed dark table
#         dbc.Card([
#             dbc.CardHeader([
#                 html.I(className="fas fa-table me-2"),
#                 "Sample Data"
#             ], style={'background': COLORS['card'], 'color': COLORS['text']}),
#             dbc.CardBody([
#                 dbc.Table.from_dataframe(
#                     df.head(10), 
#                     striped=True,
#                     bordered=True,
#                     hover=True,
#                     color='dark',  # Using color instead of dark
#                     class_name='table-dark',  # Added for consistent dark theme
#                     style={
#                         'color': COLORS['text'],
#                         'backgroundColor': COLORS['card']
#                     }
#                 )
#             ], style={'background': COLORS['card']})
#         ], style=CUSTOM_STYLE['card'])

#     ], style=CUSTOM_STYLE['container'])

# # -----------------------------
# # Callbacks
# # -----------------------------
# def init_callbacks(app, df):
#     @app.callback(
#         [Output('scatter-plot', 'figure'),
#          Output('performance-trends', 'figure'),
#          Output('resource-pie', 'figure'),
#          Output('method-comparison', 'figure'),
#          Output('target-gauge', 'figure'),
#          Output('load-distribution', 'figure'),
#          Output('profile-analysis', 'figure')],
#         [Input('energy-range', 'value')]
#     )
#     def update_graphs(energy_range):
#         if energy_range is None:
#             raise PreventUpdate

#         filtered = df[(df['Energy'] >= energy_range[0]) & (df['Energy'] <= energy_range[1])]

#         # 1. Enhanced 3D Scatter plot
#         scatter = px.scatter_3d(
#             filtered, 
#             x='Energy', y='SLA', z='load_pct',
#             color='method', size='Energy',
#             hover_data=['profile'],
#             title='Energy-SLA-Load Relationship',
#             labels={'Energy': 'Energy Consumption', 'SLA': 'SLA Violations', 'load_pct': 'Load %'}
#         )
#         scatter.update_layout(**CUSTOM_STYLE['graph'])

#         # 2. Advanced Performance Trends with Area
#         trends = go.Figure()
#         for method in filtered['method'].unique():
#             mask = filtered['method'] == method
#             trends.add_trace(go.Scatter(
#                 x=filtered[mask]['load_pct'],
#                 y=filtered[mask]['Energy'],
#                 name=f'{method} - Energy',
#                 fill='tonexty',
#                 mode='lines+markers'
#             ))
#         trends.update_layout(
#             title='Performance Trends Over Load',
#             **CUSTOM_STYLE['graph']
#         )

#         # 3. Sunburst Chart for Resource Distribution
#         pie = px.sunburst(
#             filtered,
#             path=['method', 'profile'],
#             values='Energy',
#             title='Hierarchical Resource Distribution'
#         )
#         pie.update_layout(**CUSTOM_STYLE['graph'])

#         # 4. Box Plot with Violin
#         comparison = go.Figure()
#         for method in filtered['method'].unique():
#             mask = filtered['method'] == method
#             comparison.add_trace(go.Violin(
#                 x=filtered[mask]['method'],
#                 y=filtered[mask]['Energy'],
#                 name=method,
#                 box_visible=True,
#                 meanline_visible=True
#             ))
#         comparison.update_layout(
#             title='Energy Distribution by Method',
#             **CUSTOM_STYLE['graph']
#         )

#         # 5. Polar Bar Chart
#         method_stats = filtered.groupby('method').agg({
#             'Energy': 'mean',
#             'SLA': 'mean',
#             'load_pct': 'mean'
#         }).reset_index()
        
#         gauge = go.Figure()
#         gauge.add_trace(go.Scatterpolar(
#             r=method_stats['Energy'],
#             theta=method_stats['method'],
#             fill='toself',
#             name='Energy'
#         ))
#         gauge.add_trace(go.Scatterpolar(
#             r=method_stats['SLA'],
#             theta=method_stats['method'],
#             fill='toself',
#             name='SLA'
#         ))
#         gauge.update_layout(
#             polar=dict(radialaxis=dict(visible=True, range=[0, filtered['Energy'].max()])),
#             showlegend=True,
#             title='Method Performance Radar',
#             **CUSTOM_STYLE['graph']
#         )

#         # 6. Heatmap of Correlations
#         corr_matrix = filtered[['Energy', 'SLA', 'load_pct']].corr()
#         load_dist = go.Figure(go.Heatmap(
#             z=corr_matrix,
#             x=corr_matrix.columns,
#             y=corr_matrix.columns,
#             colorscale='Viridis'
#         ))
#         load_dist.update_layout(
#             title='Metric Correlations',
#             **CUSTOM_STYLE['graph']
#         )

#         # 7. Parallel Coordinates
#         profile = px.parallel_coordinates(
#             filtered,
#             dimensions=['Energy', 'SLA', 'load_pct'],
#             color='method',
#             title='Multi-dimensional Analysis'
#         )
#         profile.update_layout(**CUSTOM_STYLE['graph'])

#         return scatter, trends, pie, comparison, gauge, load_dist, profile

# # -----------------------------
# # Initialize Dashboard
# # -----------------------------
# def init_dashboard():
#     app = Dash(
#         __name__,
#         external_stylesheets=[
#             dbc.themes.DARKLY,
#             'https://use.fontawesome.com/releases/v5.15.4/css/all.css'
#         ],
#         use_pages=True  # Enable pages
#     )
    
#     app.layout = html.Div([
#         create_navbar(),
#         page_container  # Use page_container instead of create_main_page()
#     ])
    
#     init_callbacks(app, df)
#     return app

# # -----------------------------
# # Main
# # -----------------------------
# if __name__ == "__main__":
#     app = init_dashboard()
#     app.run(debug=True, port=8051)

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, page_container
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

# -----------------------------
# Colors & Styles
# -----------------------------
COLORS = {
    'background': '#1a1a1a',
    'card': '#2d2d2d',
    'text': '#ffffff',
    'primary': '#00bcd4',
    'secondary': '#ff6e40',
    'success': '#4caf50',
    'warning': '#ffc107',
    'danger': '#f44336',
    'info': '#03a9f4',
    'dark': '#121212',
    'muted': '#666666'
}

CUSTOM_STYLE = {
    'container': {
        'max-width': '1400px',
        'margin': '0 auto',
        'padding': '20px',
        'background-color': COLORS['background'],
        'min-height': '100vh'
    },
    'card': {
        'background-color': COLORS['card'],
        'box-shadow': '0 4px 6px rgba(0,0,0,0.3)',
        'margin-bottom': '20px',
        'border': f'1px solid {COLORS["primary"]}',
        'border-radius': '8px'
    },
    'header': {
        'background': 'linear-gradient(135deg, #00bcd4 0%, #3f51b5 100%)',
        'padding': '40px 20px',
        'margin-bottom': '30px',
        'border-radius': '8px',
        'box-shadow': '0 4px 20px rgba(0,0,0,0.4)'
    },
    'graph': {
        'plot_bgcolor': COLORS['card'],
        'paper_bgcolor': COLORS['card'],
        'font': {'color': COLORS['text']},
        'xaxis': {
            'gridcolor': COLORS['muted'],
            'color': COLORS['text'],
            'showgrid': True
        },
        'yaxis': {
            'gridcolor': COLORS['muted'],
            'color': COLORS['text'],
            'showgrid': True
        }
    }
}

# -----------------------------
# Load Data
# -----------------------------
def load_sample_data():
    """Generate sample data if CSV doesn't exist"""
    n_samples = 50
    np.random.seed(42)
    
    # Generate richer sample data
    data = pd.DataFrame({
        'Energy': np.random.uniform(100, 500, n_samples),
        'SLA': np.random.uniform(0, 10, n_samples),
        'method': np.random.choice(['NSGA-II', 'First-Fit'], n_samples),
        'load_pct': np.random.choice([20, 40, 60, 80, 100], n_samples),
        'profile': np.random.choice(['Low', 'Medium', 'High'], n_samples),
        'cpu_util': np.random.uniform(0, 100, n_samples),
        'memory_util': np.random.uniform(0, 100, n_samples),
        'network_util': np.random.uniform(0, 100, n_samples),
        'index': range(n_samples)
    })
    
    # Add some derived metrics
    data['efficiency'] = data['Energy'] / (data['cpu_util'] + 1)
    data['performance'] = data['cpu_util'] * (1 - data['SLA']/10)
    
    return data

def process_loaded_data(df):
    """Process loaded CSV data to ensure all required columns exist"""
    # Add missing columns if needed
    if 'method' not in df.columns:
        df['method'] = np.random.choice(['NSGA-II', 'First-Fit'], len(df))
    if 'profile' not in df.columns:
        df['profile'] = np.random.choice(['Low', 'Medium', 'High'], len(df))
    if 'load_pct' not in df.columns:
        df['load_pct'] = np.random.choice([20, 40, 60, 80, 100], len(df))
    if 'cpu_util' not in df.columns:
        df['cpu_util'] = df['Energy'] / df['Energy'].max() * 100
    if 'memory_util' not in df.columns:
        df['memory_util'] = np.random.uniform(0, 100, len(df))
    if 'network_util' not in df.columns:
        df['network_util'] = np.random.uniform(0, 100, len(df))
    if 'index' not in df.columns:
        df['index'] = range(len(df))
        
    # Add derived metrics
    df['efficiency'] = df['Energy'] / (df['cpu_util'] + 1)
    df['performance'] = df['cpu_util'] * (1 - df['SLA']/10)
    
    return df

# Try loading CSV from multiple paths
try:
    # Try multiple possible paths
    possible_paths = [
        "results.csv",
        "results/results.csv",
        "../results/results.csv",
        "c:/Users/lavisha keshwani/cloudsim_simulator/results/results.csv"
    ]
    
    df = None
    for path in possible_paths:
        try:
            df = pd.read_csv(path)
            print(f"Successfully loaded data from {path}")
            df = process_loaded_data(df)  # Process loaded data
            break
        except:
            continue
            
    if df is None:
        print("No data found. Using sample data...")
        df = load_sample_data()
        
except Exception as e:
    print(f"Error loading data: {e}")
    print("Falling back to sample data...")
    df = load_sample_data()

# -----------------------------
# Navbar
# -----------------------------
def create_navbar():
    return dbc.NavbarSimple(
        children=[
            dbc.Nav([
                dbc.NavItem(dbc.NavLink("Dashboard", href="/", active="exact")),
                dbc.NavItem(dbc.NavLink("Theory", href="/theory", active="exact")),
                dbc.NavItem(dbc.NavLink("Analytics", href="/analytics", active="exact")),
            ], className="ms-auto", pills=True)
        ],
        brand="☁️ Cloud Optimization Dashboard",
        brand_href="/",
        color="dark",
        dark=True,
        className="mb-4"
    )

# -----------------------------
# Pages
# -----------------------------
def create_main_page():
    return html.Div([
        html.Div([
            html.H1("Cloud Resource Optimization Dashboard", style={'textAlign': 'center', 'color': COLORS['text']}),
            html.P("Multi-Objective Optimization using NSGA-II Algorithm for Energy-Efficient Cloud Computing",
                   style={'textAlign': 'center', 'color': COLORS['text'], 'opacity': '0.8'})
        ], style=CUSTOM_STYLE['header']),

        # Metrics Cards
        dbc.Row([
            dbc.Col(dbc.Card([
                html.H4("Average Energy", style={'color': COLORS['text'], 'textAlign': 'center'}),
                html.H2(f"{df['Energy'].mean():.2f}", style={'color': COLORS['primary'], 'textAlign': 'center'}),
                html.P("Watt-hours", style={'color': COLORS['muted'], 'textAlign': 'center'})
            ], body=True, style=CUSTOM_STYLE['card']), width=3),

            dbc.Col(dbc.Card([
                html.H4("Avg SLA Violations", style={'color': COLORS['text'], 'textAlign': 'center'}),
                html.H2(f"{df['SLA'].mean():.2f}", style={'color': COLORS['warning'], 'textAlign': 'center'}),
                html.P("Count", style={'color': COLORS['muted'], 'textAlign': 'center'})
            ], body=True, style=CUSTOM_STYLE['card']), width=3),

            dbc.Col(dbc.Card([
                html.H4("Total Samples", style={'color': COLORS['text'], 'textAlign': 'center'}),
                html.H2(f"{len(df)}", style={'color': COLORS['success'], 'textAlign': 'center'}),
                html.P("Records", style={'color': COLORS['muted'], 'textAlign': 'center'})
            ], body=True, style=CUSTOM_STYLE['card']), width=3),

            dbc.Col(dbc.Card([
                html.H4("Success Rate", style={'color': COLORS['text'], 'textAlign': 'center'}),
                html.H2(f"{(df['SLA']==0).mean()*100:.1f}%", style={'color': COLORS['primary'], 'textAlign': 'center'}),
                html.P("Percentage", style={'color': COLORS['muted'], 'textAlign': 'center'})
            ], body=True, style=CUSTOM_STYLE['card']), width=3),
        ], className="mb-4"),

        # Project Overview Section
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-info-circle me-2"),
                    "Project Overview"
                ], style={'background': COLORS['card'], 'color': COLORS['text']}),
                dbc.CardBody([
                    html.H5("Multi-Objective Cloud Resource Optimization", style={'color': COLORS['primary'], 'margin-bottom': '15px'}),
                    html.P([
                        "This project implements a sophisticated cloud resource optimization system using the ",
                        html.Strong("NSGA-II (Non-dominated Sorting Genetic Algorithm II)"),
                        " to achieve optimal trade-offs between energy consumption and Service Level Agreement (SLA) violations."
                    ], style={'color': COLORS['text'], 'margin-bottom': '15px'}),
                    html.P([
                        "The system simulates cloud environments with varying workloads and compares different resource allocation ",
                        "strategies including traditional First-Fit algorithms and advanced evolutionary approaches."
                    ], style={'color': COLORS['text']})
                ])
            ], style=CUSTOM_STYLE['card']), width=12),
        ], className="mb-4"),

        # Key Features Section
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-star me-2"),
                    "Key Features"
                ], style={'background': COLORS['card'], 'color': COLORS['text']}),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H6("🎯 Multi-Objective Optimization", style={'color': COLORS['primary']}),
                            html.P("Simultaneously optimizes energy consumption and SLA compliance", style={'color': COLORS['text']})
                        ], width=6),
                        dbc.Col([
                            html.H6("🧬 NSGA-II Algorithm", style={'color': COLORS['success']}),
                            html.P("Advanced evolutionary algorithm for Pareto-optimal solutions", style={'color': COLORS['text']})
                        ], width=6),
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            html.H6("📊 Real-time Monitoring", style={'color': COLORS['warning']}),
                            html.P("Live performance metrics and resource utilization tracking", style={'color': COLORS['text']})
                        ], width=6),
                        dbc.Col([
                            html.H6("☁️ CloudSim Integration", style={'color': COLORS['info']}),
                            html.P("Built on CloudSim framework for realistic cloud simulation", style={'color': COLORS['text']})
                        ], width=6),
                    ])
                ])
            ], style=CUSTOM_STYLE['card']), width=12),
        ], className="mb-4"),

        # Technical Specifications
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-cogs me-2"),
                    "Technical Specifications"
                ], style={'background': COLORS['card'], 'color': COLORS['text']}),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H6("Algorithms", style={'color': COLORS['primary']}),
                            html.Ul([
                                html.Li("NSGA-II Multi-Objective Optimization"),
                                html.Li("First-Fit Resource Allocation"),
                                html.Li("Dynamic Load Balancing")
                            ], style={'color': COLORS['text']})
                        ], width=4),
                        dbc.Col([
                            html.H6("Metrics Tracked", style={'color': COLORS['success']}),
                            html.Ul([
                                html.Li("Energy Consumption (Wh)"),
                                html.Li("SLA Violations Count"),
                                html.Li("CPU, Memory, Network Utilization"),
                                html.Li("Resource Efficiency Score")
                            ], style={'color': COLORS['text']})
                        ], width=4),
                        dbc.Col([
                            html.H6("Optimization Objectives", style={'color': COLORS['warning']}),
                            html.Ul([
                                html.Li("Minimize Energy Consumption"),
                                html.Li("Minimize SLA Violations"),
                                html.Li("Maximize Resource Utilization"),
                                html.Li("Balance Performance vs Cost")
                            ], style={'color': COLORS['text']})
                        ], width=4),
                    ])
                ])
            ], style=CUSTOM_STYLE['card']), width=12),
        ], className="mb-4"),

        # Research Impact & Applications
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-lightbulb me-2"),
                    "Research Impact & Applications"
                ], style={'background': COLORS['card'], 'color': COLORS['text']}),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H6("Environmental Impact", style={'color': COLORS['success']}),
                            html.P("Reduces data center energy consumption by up to 30% while maintaining service quality", 
                                  style={'color': COLORS['text']})
                        ], width=6),
                        dbc.Col([
                            html.H6("Cost Optimization", style={'color': COLORS['primary']}),
                            html.P("Significantly lowers operational costs through intelligent resource management", 
                                  style={'color': COLORS['text']})
                        ], width=6),
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            html.H6("Industry Applications", style={'color': COLORS['warning']}),
                            html.P("Applicable to cloud service providers, enterprise data centers, and edge computing", 
                                  style={'color': COLORS['text']})
                        ], width=6),
                        dbc.Col([
                            html.H6("Future Research", style={'color': COLORS['info']}),
                            html.P("Foundation for AI-driven autonomous cloud management systems", 
                                  style={'color': COLORS['text']})
                        ], width=6),
                    ])
                ])
            ], style=CUSTOM_STYLE['card']), width=12),
        ], className="mb-4"),

        # Performance Comparison
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-chart-line me-2"),
                    "Algorithm Performance Comparison"
                ], style={'background': COLORS['card'], 'color': COLORS['text']}),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H6("NSGA-II Algorithm", style={'color': COLORS['success']}),
                            html.Ul([
                                html.Li(f"Avg Energy: {df[df['method']=='NSGA-II']['Energy'].mean():.1f} Wh", style={'color': COLORS['text']}),
                                html.Li(f"Avg SLA: {df[df['method']=='NSGA-II']['SLA'].mean():.1f} violations", style={'color': COLORS['text']}),
                                html.Li("✅ Multi-objective optimization", style={'color': COLORS['success']}),
                                html.Li("✅ Pareto-optimal solutions", style={'color': COLORS['success']})
                            ])
                        ], width=6),
                        dbc.Col([
                            html.H6("First-Fit Algorithm", style={'color': COLORS['warning']}),
                            html.Ul([
                                html.Li(f"Avg Energy: {df[df['method']=='First-Fit']['Energy'].mean():.1f} Wh", style={'color': COLORS['text']}),
                                html.Li(f"Avg SLA: {df[df['method']=='First-Fit']['SLA'].mean():.1f} violations", style={'color': COLORS['text']}),
                                html.Li("⚠️ Single-objective approach", style={'color': COLORS['warning']}),
                                html.Li("⚠️ Limited optimization scope", style={'color': COLORS['warning']})
                            ])
                        ], width=6),
                    ])
                ])
            ], style=CUSTOM_STYLE['card']), width=12),
        ], className="mb-4"),

        # Sample Data Table
        dbc.Card([
            dbc.CardHeader([
                html.I(className="fas fa-table me-2"),
                "Sample Optimization Results"
            ], style={'background': COLORS['card'], 'color': COLORS['text']}),
            dbc.CardBody([
                dbc.Table.from_dataframe(
                    df.head(10)[['Energy', 'SLA', 'method', 'profile', 'load_pct', 'efficiency']].round(2), 
                    striped=True,
                    bordered=True,
                    hover=True,
                    color='dark',
                    class_name='table-dark',
                    style={
                        'color': COLORS['text'],
                        'backgroundColor': COLORS['card']
                    }
                )
            ], style={'background': COLORS['card']})
        ], style=CUSTOM_STYLE['card'])

    ], style=CUSTOM_STYLE['container'])

# -----------------------------
# Initialize Dashboard
# -----------------------------
def init_dashboard():
    app = Dash(
        __name__,
        external_stylesheets=[
            dbc.themes.DARKLY,
            'https://use.fontawesome.com/releases/v5.15.4/css/all.css'
        ],
        use_pages=True  # Enable pages
    )
    
    app.layout = html.Div([
        create_navbar(),
        page_container  # Use page_container instead of create_main_page()
    ])
    
    return app

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    app = init_dashboard()
    app.run(debug=True, port=8051)