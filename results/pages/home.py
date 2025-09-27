from dash import register_page, html, dcc
import dash_bootstrap_components as dbc
from results.dashboard import create_main_page  # Changed to absolute import

register_page(__name__, path='/')

layout = create_main_page()
