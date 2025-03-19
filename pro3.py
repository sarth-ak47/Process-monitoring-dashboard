import psutil
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import collections

# Initialize Dash app
app = dash.Dash(__name__)

# Store historical data for smooth line charts
cpu_history = collections.deque(maxlen=30)
memory_history = collections.deque(maxlen=30)
disk_history = collections.deque(maxlen=30)
net_history = collections.deque(maxlen=30)

# Layout
app.layout = html.Div(style={'backgroundColor': '#1e1e1e', 'color': 'white', 'textAlign': 'center', 'padding': '20px'}, children=[
    html.H1("Real-Time System Performance Dashboard", style={'color': '#FFD700'}),
    dcc.Interval(id='interval-component', interval=2000, n_intervals=0),  # Update every 2 seconds
    
    html.Div(style={'display': 'flex', 'justifyContent': 'space-around', 'flexWrap': 'wrap'}, children=[
        html.Div([
            html.H3("CPU Usage", style={'color': '#00FF00'}),
            dcc.Graph(id='cpu-usage-graph')
        ], style={'width': '45%'}),
        
        html.Div([
            html.H3("Memory Usage", style={'color': '#FF4500'}),
            dcc.Graph(id='memory-usage-graph')
        ], style={'width': '45%'}),
        
        html.Div([
            html.H3("Disk Usage", style={'color': '#1E90FF'}),
            dcc.Graph(id='disk-usage-graph')
        ], style={'width': '45%'}),
        
        html.Div([
            html.H3("Network Activity", style={'color': '#8A2BE2'}),
            dcc.Graph(id='net-usage-graph')
        ], style={'width': '45%'})
    ])
])

# Callbacks to update graphs
@app.callback(
    [Output('cpu-usage-graph', 'figure'),
     Output('memory-usage-graph', 'figure'),
     Output('disk-usage-graph', 'figure'),
     Output('net-usage-graph', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    # Get system metrics
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    net_usage = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
    
    # Append new values to history
    cpu_history.append(cpu_usage)
    memory_history.append(memory_usage)
    disk_history.append(disk_usage)
    net_history.append(net_usage / (1024 * 1024))  # Convert to MB
    
    # CPU Usage Graph
    cpu_fig = go.Figure()
    cpu_fig.add_trace(go.Scatter(y=list(cpu_history), mode='lines', name='CPU Usage', line=dict(color='#00FF00')))
    cpu_fig.update_layout(title='CPU Usage (%)', xaxis_title='Time', yaxis_title='Usage (%)', plot_bgcolor='#222222', paper_bgcolor='#1e1e1e', font=dict(color='white'))
    
    # Memory Usage Graph
    memory_fig = go.Figure()
    memory_fig.add_trace(go.Scatter(y=list(memory_history), mode='lines', name='Memory Usage', line=dict(color='#FF4500')))
    memory_fig.update_layout(title='Memory Usage (%)', xaxis_title='Time', yaxis_title='Usage (%)', plot_bgcolor='#222222', paper_bgcolor='#1e1e1e', font=dict(color='white'))
    
    # Disk Usage Graph
    disk_fig = go.Figure()
    disk_fig.add_trace(go.Scatter(y=list(disk_history), mode='lines', name='Disk Usage', line=dict(color='#1E90FF')))
    disk_fig.update_layout(title='Disk Usage (%)', xaxis_title='Time', yaxis_title='Usage (%)', plot_bgcolor='#222222', paper_bgcolor='#1e1e1e', font=dict(color='white'))
    
    # Network Usage Graph
    net_fig = go.Figure()
    net_fig.add_trace(go.Scatter(y=list(net_history), mode='lines', name='Network Usage (MB)', line=dict(color='#8A2BE2')))
    net_fig.update_layout(title='Network Activity (MB)', xaxis_title='Time', yaxis_title='Data (MB)', plot_bgcolor='#222222', paper_bgcolor='#1e1e1e', font=dict(color='white'))
    
    return cpu_fig, memory_fig, disk_fig, net_fig

# Run the app
if __name__ == '__main__':
     app.run(debug=True)