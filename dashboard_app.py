import dash
from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd
import os

# Leer CSVs de ejemplo
base_dir = os.path.dirname(__file__)
shipments = pd.read_csv(os.path.join(base_dir, "navigator_shipments.csv"))
finished_goods = pd.read_csv(os.path.join(base_dir, "navigator_finished_goods.csv"))
depletions = pd.read_csv(os.path.join(base_dir, "vip_depletions.csv"))
dist_inv = pd.read_csv(os.path.join(base_dir, "vip_distributor_inventory.csv"))
bev = pd.read_csv(os.path.join(base_dir, "powerbi_bev_export.csv"))

# Concatenar datasets (simple demo)
shipments['type'] = 'shipments'
depletions['type'] = 'depletions'
bev_ship = bev[['date','brand','market','shipments']].rename(columns={'shipments':'value'})
bev_ship['type'] = 'shipments'
bev_dep = bev[['date','brand','market','depletions']].rename(columns={'depletions':'value'})
bev_dep['type'] = 'depletions'

cpg_ship = shipments.rename(columns={'shipments':'value'})
cpg_dep = depletions.rename(columns={'depletions':'value'})

all_sales = pd.concat([cpg_ship[['date','brand','market','value','type']], 
                       cpg_dep[['date','brand','market','value','type']],
                       bev_ship, bev_dep])

# Dash App
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Sales & Inventory Dashboard"),
    dcc.Dropdown(
        id="brand-filter",
        options=[{"label": b, "value": b} for b in all_sales["brand"].unique()],
        value="CPG"
    ),
    dcc.Graph(id="sales-trend"),
    dash_table.DataTable(id="table", page_size=5)
])

@app.callback(
    [dash.Output("sales-trend","figure"),
     dash.Output("table","data")],
    [dash.Input("brand-filter","value")]
)
def update(brand):
    df = all_sales[all_sales["brand"]==brand]
    fig = px.line(df, x="date", y="value", color="type", title=f"Sales trend - {brand}")
    return fig, df.to_dict("records")

if __name__ == "__main__":
    app.run_server(debug=True)
