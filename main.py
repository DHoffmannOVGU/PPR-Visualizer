"""
This app creates a simple sidebar layout using inline style arguments and the
dbc.Nav component.

dcc.Location is used to track the current location, and a callback uses the
current location to render the appropriate page content. The active prop of
each NavLink is set automatically according to the current pathname. To use
this feature you must install dash-bootstrap-components >= 0.11.0.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, State
import dash_cytoscape as cyto
import json

FA = "https://use.fontawesome.com/releases/v5.12.1/css/all.css"

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY, FA])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "12rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "14rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

### Initial Graph ####  #### #### #### #### ####

with open('pan_assets/products.json', 'r') as f:
    products = json.load(f)

with open('pan_assets/processes.json', 'r') as f:
    processes = json.load(f)

with open('pan_assets/resources.json', 'r') as f:
    resources = json.load(f)

with open('pan_assets/relations.json', 'r') as f:
    relations = json.load(f)

elements=products + processes + resources + relations


with open('pan_assets/pan_stylesheet.json', 'r') as f:
    pan_stylesheet = json.load(f)

#### #### #### #### #### #### #### #### #### ####


### ####  #### Tabs  #### #### #### ####

tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Change", tab_id="tab-1"),
                dbc.Tab(label="Analyse", tab_id="tab-2"),
                dbc.Tab(label="Improve", tab_id="tab-3"),
                dbc.Tab(label="Maintain", tab_id="tab-4"),
            ],
            id="tabs",
            active_tab="tab-1",
        ),
        html.Div(id="tab_content"),
    ]
)

aml_transformer=html.Div(
    [
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop AML or JSON File or ',
            html.A('Select File')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),
    html.Hr(),
    dbc.Input(id="input", placeholder="Type new file name", type="text"),
    html.Hr(),
    dbc.Label("Choose JSON-style"),
    dbc.RadioItems(
        options=[
            {"label": "Normal ", "value": 1},
            {"label": "Compressed", "value": 2},
            {"label": "Cytoscape-JSON", "value": 3, "disabled": True},
        ],
        value=1,
        id="radioitems-input",
    ),
    html.Hr(),
    dbc.Label("Additional Configurations"),
    dbc.Checklist(
        options=[
            {"label": "Use Abbreviations", "value": 1},
            {"label": "Indent file", "value": 2},
            {"label": "Add missing Unique ID's", "value": 3},
            {"label": "Seperate into multiple files", "value": 4, "disabled": True},
        ],
        value=[1,2],
        id="switches-input",
        switch=True,
    ),
    html.Hr(),
    dbc.Button('Transform', id="add_node", color="primary", className="btn-block col-12",),
    html.Div(id='output-data-upload'),
    ]
)

analyze_tab=html.Div(
    [
        html.Div(id='cytoscape-tapNodeData-json')

    ]
)


@app.callback(Output('cytoscape-tapNodeData-json', 'children'),
              Input('pan', 'tapNode'))
def displayTapNodeData(data):
    return str(data["position"])


change_tab=html.Div(
    [
        dbc.Select(
            id="select_asset", 
            placeholder="Add...",
            options=[
                {"label": "Resource", "value": "Resource"},
                {"label": "Operator", "value": "Operator"},
            ],
        ),
        dbc.Select(id='asset_list'),
        dbc.Input(id="input", placeholder="Type node name...", type="text"),
        dbc.Button('Add Node', id="add_node", color="primary", className="btn-block col-12",),
    ]
)



@app.callback(
    Output('asset_list', 'options'),
    #Output('change_output', 'children'),
    Input('select_asset', 'value'))
def set_asset_options(selected_asset):
    with open('pan_assets/type_config.json', 'r') as f:
        type_config = json.load(f)
    return [{'label': i, 'value': i} for i in type_config[selected_asset].keys()]
    #return type_config[selected_asset].keys()



@app.callback(Output("tab_content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return change_tab
    elif at == "tab-2":
        return analyze_tab
    return html.P("This shouldn't ever be displayed...")


#### #### #### #### #### #### #### #### #### ####


game_overview= html.Div(
    [
        html.H3("Spielübersicht",style={
            "font-size": "1.5rem"
        }),
        html.Hr(),
        dbc.Alert(
            [
                html.I(className="fa-solid fa-coin fa-2x"),
                "Current money: 5 Gold pieces",
            ],
            color="warning",
            className="d-flex align-items-center",
        ),
        dbc.Alert(
            [
                html.I(className="far fa-clock fa-2x"),
                "Game time: 04:30:00/08:00:00",
            ],
            color="info",
            className="d-flex align-items-center",
        ),
        dbc.Alert(
            [
                html.I(className="fas fa-box fa-2x"),
                "Finished parts: 10/20",
            ],
            color="success",
            className="d-flex align-items-center",
        ),
        html.Hr(),
        dbc.Button(
            [
                 html.I(className="fa fa-directions"), "Next Round"
            ],
            color="danger",
            className="btn-block col-12",           
        ),
        html.Hr(),
        tabs
    ]
)

cytoscape = html.Div([
    dbc.Row([
        dbc.Col(
            cyto.Cytoscape(
                id="pan",
                zoom=2,
                minZoom=0.8,
                maxZoom=3,
                pan = { "x": 0, "y": 0 },
                layout={
                    'name': "preset",
                    "fit":False
                },
                style={
                    'width': '100%', 
                    "height": "100%",
                    "background-color":"#f8f9fa"},      
                stylesheet=pan_stylesheet,
                elements=   products+
                            processes+
                            resources+
                            relations
        ),
        width=10
        ),
        dbc.Col(
            html.Div([
                game_overview,
                html.P(),   
            ]),   
        width=2)
    ])
])

#################### Sidebar ####################

sidebar = html.Div(
    [
        html.H3("David's Toolbox", className="display-5"),
        html.Hr(),
        html.P(
            "Navigation for current prototypes", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact", class_name="page-link"),
                dbc.NavLink("Element reference", href="/page-1", active="exact", class_name="page-link"),
                dbc.NavLink("Button reference", href="/page-2", active="exact", class_name="page-link"),                
                dbc.NavLink("AML Transformer", href="/aml-json", active="exact", class_name="page-link"),
                dbc.NavLink("Create PAN", href="/create-pan", active="exact", class_name="page-link"),
                dbc.NavLink("Simulate PAN", href="/simulate-pan", active="exact", disabled=True, class_name="page-link"),
            ],
            vertical=True,
            pills=True
        ),
        html.Hr(),
        dbc.Button('Update PAN', id="update_pan", color="primary"),
        html.Div(id='output-state'),
        html.Hr(),
        dbc.Button('Update Style', id="update_style", color="primary"),
        html.Hr(),
        dbc.Button('Connect Nodes', id="connect_nodes", color="primary"),
        html.Div(id="hidden-div", style={"display":"none"})
    ],
    style=SIDEBAR_STYLE,
)

@app.callback(
    Output('hidden-div', 'children'),
    Input("connect_nodes","n_clicks"),
    State('pan', 'selectedNodeData'),
)
def connect_nodes(n_clicks, data):
    with open(r'pan_assets/relations.json', 'r') as f:
        relations = json.load(f)
    new_relation= {"data": {"source": data[0]["id"], "target":data[1]["id"]}}
    relations.append(new_relation)
    
    with open(r'pan_assets/relations.json', "w" ) as write:
        json.dump(relations , write, indent=1 )

#Update Pan
@app.callback(
    Output("pan", "elements"),
    Output("output-state", "children"),
    [Input("update_pan", "n_clicks")]
)
def update_pan(n_clicks):
    with open('pan_assets/products.json', 'r') as f:
        products = json.load(f)

    with open('pan_assets/processes.json', 'r') as f:
        processes = json.load(f)

    with open('pan_assets/resources.json', 'r') as f:
        resources = json.load(f)

    with open('pan_assets/relations.json', 'r') as f:
        relations = json.load(f)
    
    pan_elements=products + processes + resources + relations
    text = f"Button has been clicked {n_clicks} times"

    return pan_elements, text

#Update Style
@app.callback(
    Output("pan", "stylesheet"),
    [Input("update_style", "n_clicks")]
)
def update_style(n_clicks):
    with open('pan_assets/pan_stylesheet.json', 'r') as f:
        pan_stylesheet = json.load(f)

    return pan_stylesheet


#########################################################


buttons = html.Div(
    [
        dbc.Button("Primary", outline=True, color="primary", className="me-1"),
        dbc.Button("Secondary", color="secondary", className="me-1"),
        dbc.Button("Success", color="success", className="me-1"),
        dbc.Button("Warning", color="warning", className="me-1"),
        dbc.Button("Danger", color="danger", className="me-1"),
        dbc.Button("Info", color="info", className="me-1"),
        dbc.Button("Light", color="light", className="me-1"),
        dbc.Button("Dark", color="dark", className="me-1"),
        dbc.Button("Link", color="link"),
    ]
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

app.validation_layout= html.Div([
    cytoscape,
    sidebar,
    buttons,
    game_overview,
    change_tab,
    tabs,
    content
])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P("This is the content of the home page!")
    elif pathname == "/page-1":
        return html.P("This is the content of page 1. Yay!")
    elif pathname == "/page-2":
        return buttons
    elif pathname == "/aml-json":
        return aml_transformer
    elif pathname == "/create-pan":
        return cytoscape
    elif pathname == "/simulate-pan":
        return cytoscape
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(debug=True, port=8050)