import dash
from dash import Dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html, ctx
from dash import ClientsideFunction

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
app.title = "Movie Recommender"
server = app.server

# Main app layout with URL and state storage
app.layout = html.Div([
    dcc.Location(id="url"),   # Tracks the current URL for page navigation
    dcc.Store(id="actor-movie-page", data=0),  # Stores the actor's page state
    dcc.Store(id="search-history", data=[]),   # Stores search history
    dcc.Store(id="previous-page", data="/"),   # Stores the last visited page
    dash.page_container
])
# Callback to track and update the previous page
@app.callback(
    Output("previous-page", "data"),
    Input("url", "pathname"),
    State("previous-page", "data")
)
def update_previous_page(current_path, previous_page):
    if ctx.triggered_id == "url" and previous_page != current_path:
        return previous_page  # Don’t update if refresh
    return current_path

# Client-side callback for the "Back" button using JavaScript
app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="goBack"),
    Output("js-trigger", "message"),
    Input("actor-back", "n_clicks")
)
if __name__ == '__main__':
    app.run(debug=True)
