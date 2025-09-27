# # theory.py
# from dash import register_page, html, dcc
# import dash_bootstrap_components as dbc
# from results.dashboard import COLORS, CUSTOM_STYLE

# register_page(__name__, path='/theory')

# def create_theory_layout():
#     return html.Div([
#         # Header
#         html.Div([
#             html.H1("Theoretical Framework",
#                    style={'textAlign': 'center', 'color': COLORS['text']}),
#             html.P("Understanding VM Placement Optimization",
#                    style={'textAlign': 'center', 'color': COLORS['text'], 'opacity': '0.8'})
#         ], style=CUSTOM_STYLE['header']),

#         dbc.Row([
#             # Problem Statement
#             dbc.Col(dbc.Card([
#                 html.H3("Problem Statement", style={'color': COLORS['primary']}),
#                 html.Hr(style={'borderColor': COLORS['muted']}),
#                 dcc.Markdown("""
#                     ### Multi-Objective VM Placement
#                     Optimizing the placement of Virtual Machines (VMs) across physical hosts while considering:
#                     * Energy consumption
#                     * SLA violations
#                     * Resource utilization
#                     * System performance
#                     * Operational costs
#                 """, style={'color': COLORS['text']})
#             ], style=CUSTOM_STYLE['card']), width=6),

#             # Solution Approach
#             dbc.Col(dbc.Card([
#                 html.H3("Solution Approach", style={'color': COLORS['success']}),
#                 html.Hr(style={'borderColor': COLORS['muted']}),
#                 dcc.Markdown("""
#                     ### NSGA-II Algorithm
#                     * Multi-objective genetic algorithm
#                     * Non-dominated sorting
#                     * Elitism preservation
#                     * Diversity maintenance
#                     * Blockchain integration for transparency
#                 """, style={'color': COLORS['text']})
#             ], style=CUSTOM_STYLE['card']), width=6),
#         ], className='mb-4'),

#         # Metrics and Evaluation
#         dbc.Card([
#             html.H3("Metrics & Evaluation", style={'color': COLORS['warning'], 'padding': '15px'}),
#             html.Hr(style={'borderColor': COLORS['muted']}),
#             dbc.Row([
#                 dbc.Col(dcc.Markdown("""
#                     ### Key Performance Indicators
#                     1. **Energy Efficiency**
#                        * Power consumption metrics
#                        * Carbon footprint
#                     2. **SLA Compliance**
#                        * Resource availability
#                        * Performance guarantees
#                     3. **Resource Utilization**
#                        * CPU and memory usage
#                        * Network bandwidth
#                 """, style={'color': COLORS['text']}), width=6),
                
#                 dbc.Col(dcc.Markdown("""
#                     ### Blockchain Integration
#                     * Immutable placement records
#                     * Transparent decision tracking
#                     * Smart contract automation
#                     * Trustless verification
#                 """, style={'color': COLORS['text']}), width=6),
#             ], style={'padding': '15px'})
#         ], style=CUSTOM_STYLE['card'])
#     ], style=CUSTOM_STYLE['container'])

# layout = create_theory_layout()

# theory.py
from dash import register_page, html, dcc
import dash_bootstrap_components as dbc
from results.dashboard import COLORS, CUSTOM_STYLE

register_page(__name__, path='/theory')

def create_theory_layout():
    return html.Div([
        # Header
        html.Div([
            html.H1("Theoretical Framework",
                   style={'textAlign': 'center', 'color': COLORS['text']}),
            html.P("A Comprehensive Understanding of VM Placement Optimization with Blockchain Transparency",
                   style={'textAlign': 'center', 'color': COLORS['text'], 'opacity': '0.8'})
        ], style=CUSTOM_STYLE['header']),

        # Problem + Solution
        dbc.Row([
            # Problem Statement
            dbc.Col(dbc.Card([
                html.H3("Problem Statement", style={'color': COLORS['primary']}),
                html.Hr(style={'borderColor': COLORS['muted']}),

                dcc.Markdown("""
                    ### Challenges in Cloud VM Placement
                    Cloud data centers host thousands of Virtual Machines (VMs) on physical servers.  
                    The placement of VMs is critical because it directly affects **energy usage, performance, and cost**.  

                    **Key issues in traditional VM placement:**
                    * High **energy consumption** due to inefficient allocation
                    * **SLA (Service Level Agreement) violations** when VMs do not get required resources
                    * Poor **resource utilization** (servers underloaded or overloaded)
                    * High **operational costs**
                    * Lack of **transparency** in placement decisions, which reduces trust
                """, style={'color': COLORS['text']})
            ], style=CUSTOM_STYLE['card']), width=6),

            # Solution Approach
            dbc.Col(dbc.Card([
                html.H3("Proposed Solution", style={'color': COLORS['success']}),
                html.Hr(style={'borderColor': COLORS['muted']}),

                dcc.Markdown("""
                    ### NSGA-II + Blockchain Based VM Placement
                    To overcome the limitations of heuristic methods, we propose:  

                    * **NSGA-II (Non-dominated Sorting Genetic Algorithm-II):**
                      - A **multi-objective evolutionary algorithm**
                      - Optimizes for **energy, SLA, utilization, and adaptation** simultaneously
                      - Ensures **diversity** and prevents premature convergence
                      - Uses **elitism** to retain best solutions

                    * **Blockchain Integration:**
                      - Placement decisions are recorded on an immutable ledger
                      - Ensures **transparency and trust** among stakeholders
                      - Smart contracts automate policy enforcement
                      - Provides **tamper-proof audit trail**
                """, style={'color': COLORS['text']})
            ], style=CUSTOM_STYLE['card']), width=6),
        ], className='mb-4'),

        # Metrics and Evaluation
        dbc.Card([
            html.H3("Evaluation Metrics", style={'color': COLORS['warning'], 'padding': '15px'}),
            html.Hr(style={'borderColor': COLORS['muted']}),

            dbc.Row([
                dbc.Col(dcc.Markdown("""
                    ### 1. **Energy Efficiency**
                    - Measures total power consumed by servers  
                    - Lower energy → reduced carbon footprint  
                    - Directly impacts **sustainability** of cloud systems  

                    ### 2. **SLA Compliance**
                    - SLA = agreement on guaranteed performance (e.g., uptime, speed)  
                    - Ensures VMs get enough CPU, memory, bandwidth  
                    - Higher compliance = fewer performance violations  

                    ### 3. **Resource Utilization**
                    - Percentage of **CPU, memory, and network** used effectively  
                    - Avoids underutilization (wasted resources) and overutilization (failures)  

                    ### 4. **Adaptation Score**
                    - Ability of the system to **adapt dynamically** to workload changes  
                    - Reflects flexibility during demand spikes and failures  

                    ### 5. **Carbon Reduction**
                    - Evaluates reduction in carbon emissions by lowering power consumption  
                    - Critical for **green cloud computing** and sustainability goals
                """, style={'color': COLORS['text']}), width=6),

                dbc.Col(dcc.Markdown("""
                    ### Blockchain Role in Metrics
                    - **Energy & Carbon Tracking:** Blockchain records power usage and green energy credits  
                    - **SLA Auditing:** SLA violations are logged transparently  
                    - **Resource Proof:** Immutable records of VM-to-host mapping prevent manipulation  
                    - **Adaptation Tracking:** Blockchain logs reallocation decisions for audit  
                    - **Trust & Compliance:** Enables trustless verification of provider performance
                """, style={'color': COLORS['text']}), width=6),
            ], style={'padding': '15px'})
        ], style=CUSTOM_STYLE['card'], className='mb-4'),

        # Comparison with Existing Approaches
        dbc.Card([
            html.H3("Comparison with Existing Approaches", style={'color': COLORS['info'], 'padding': '15px'}),
            html.Hr(style={'borderColor': COLORS['muted']}),

            dcc.Markdown("""
                ### Traditional Approaches
                * **First Fit / Round Robin:**  
                  - Fast but **energy-inefficient**  
                  - Ignores SLA and carbon concerns  

                * **Best Fit Decreasing (BFD):**  
                  - Packs VMs tightly to reduce energy  
                  - Limited in handling **multi-objective tradeoffs**  

                * **DVFS (Dynamic Voltage and Frequency Scaling):**  
                  - Saves power at CPU level  
                  - Does not optimize VM placement strategy  

                * **PABFD (Power-aware BFD):**  
                  - Focuses only on power reduction  
                  - **Single-objective**, ignores SLA & adaptation  

                ### Proposed NSGA-II + Blockchain
                * Multi-objective optimization (**Energy, SLA, Utilization, Carbon, Adaptation**)  
                * **Blockchain ensures transparency** → decisions are verifiable  
                * Outperforms heuristics in both **efficiency and trust**  
                * Better suited for **real-world large-scale cloud systems**
            """, style={'color': COLORS['text']})
        ], style=CUSTOM_STYLE['card'], className='mb-4'),

        # Conclusion
        dbc.Card([
            html.H3("Conclusion", style={'color': COLORS['danger'], 'padding': '15px'}),
            html.Hr(style={'borderColor': COLORS['muted']}),

            dcc.Markdown("""
                The integration of **NSGA-II for multi-objective optimization** and **Blockchain for transparency**  
                provides a powerful framework for cloud VM placement.  

                ✅ Reduces **energy consumption** and **carbon emissions**  
                ✅ Improves **SLA compliance** and **resource utilization**  
                ✅ Provides **trustworthy, tamper-proof records**  
                ✅ Outperforms existing heuristic-based approaches  

                This hybrid model is not only efficient but also **future-ready** for sustainable and transparent cloud computing.
            """, style={'color': COLORS['text']})
        ], style=CUSTOM_STYLE['card'])
    ], style=CUSTOM_STYLE['container'])


layout = create_theory_layout()
