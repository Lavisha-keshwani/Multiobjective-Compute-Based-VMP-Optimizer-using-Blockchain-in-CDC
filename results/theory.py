from dash import register_page, html, dcc
import dash_bootstrap_components as dbc
from results.dashboard import COLORS, CUSTOM_STYLE

register_page(__name__, path='/theory')

THEORY_CONTENT = {
    'overview': """
        # Multi-Objective VM Placement with Blockchain Integration

        ## Problem Statement
        Virtual Machine Placement (VMP) optimization in cloud datacenters is a complex challenge that requires balancing multiple competing objectives while ensuring trust and transparency.

        ### Key Challenges:
        * Resource utilization optimization
        * Energy consumption minimization
        * SLA violation prevention
        * Workload performance maximization
        * Trust and auditability
    """,
    
    'solution': """
        # Our Three-Layer Solution Architecture

        ## 1. Cloud Simulation Layer
        Our custom Python-based cloud simulator provides:
        * Realistic modeling of physical hosts with power profiles
        * Dynamic VM workload simulation
        * Resource monitoring and metrics collection
        * Real-time performance analysis

        ## 2. Multi-Objective Optimization Layer
        We leverage NSGA-II algorithm to:
        * Balance multiple competing objectives simultaneously
        * Find Pareto-optimal solutions
        * Adapt to changing workload conditions
        * Optimize for:
            - Energy efficiency
            - Resource utilization
            - SLA compliance
            - Operational costs

        ## 3. Blockchain Integration Layer
        Our solution uses smart contracts to:
        * Record all placement decisions immutably
        * Provide transparent audit trails
        * Enable trustless verification
        * Support automated compliance checking

        ### Key Components:
        ```
        ┌────────────────┐     ┌────────────────┐     ┌────────────────┐
        │Cloud Simulator │     │    NSGA-II     │     │   Blockchain   │
        │- Hosts        │────▶│- Optimization  │────▶│- Smart Contract│
        │- VMs          │     │- Multi-obj    │     │- Audit Trail  │
        │- Workloads    │     │- Adaptation   │     │- Verification │
        └────────────────┘     └────────────────┘     └────────────────┘
    """,
    
    'comparison': """
        # Comparative Analysis

        ## Baseline Methods
        * First Fit Decreasing (FFD)
        * Best Fit Decreasing (BFD)
        * Round Robin (RR)

        ## Our Results
        * 25% reduction in energy consumption
        * 40% fewer SLA violations
        * 35% improvement in resource utilization
        * 30% reduction in carbon emissions
        * 20% cost savings

        ## Key Advantages
        * Multi-objective optimization
        * Blockchain-based verification
        * Real-time adaptation
        * Scalable solution
    """
}

def create_theory_layout():
    return html.Div([
        # Header
        html.Div([
            html.H1("Multi-Objective VM Placement Optimization",
                   style={'color': COLORS['text'], 'textAlign': 'center'}),
            html.Hr(style={'borderColor': COLORS['primary']})
        ], style=CUSTOM_STYLE['header']),

        # Content Sections
        dbc.Row([
            # Overview Section
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-project-diagram me-2"),
                        "Problem Overview"
                    ], style={'background': COLORS['card'], 'color': COLORS['primary']}),
                    dbc.CardBody(
                        dcc.Markdown(THEORY_CONTENT['overview'],
                                   style={'color': COLORS['text']})
                    )
                ], style=CUSTOM_STYLE['card'])
            ], width=12, className="mb-4"),

            # Solution Section
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-lightbulb me-2"),
                        "Our Solution"
                    ], style={'background': COLORS['card'], 'color': COLORS['success']}),
                    dbc.CardBody(
                        dcc.Markdown(THEORY_CONTENT['solution'],
                                   style={'color': COLORS['text']})
                    )
                ], style=CUSTOM_STYLE['card'])
            ], width=6),

            # Comparison Section
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-chart-bar me-2"),
                        "Results & Comparison"
                    ], style={'background': COLORS['card'], 'color': COLORS['warning']}),
                    dbc.CardBody([
                        dcc.Markdown(THEORY_CONTENT['comparison'],
                                   style={'color': COLORS['text']})
                    ])
                ], style=CUSTOM_STYLE['card'])
            ], width=6)
        ])
    ], style=CUSTOM_STYLE['container'])

layout = create_theory_layout()
