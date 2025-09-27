import os
import sys

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from results.dashboard import init_dashboard

if __name__ == '__main__':
    app = init_dashboard()
    app.run(debug=True, port=8051)  # Fixed: run_server instead of run
