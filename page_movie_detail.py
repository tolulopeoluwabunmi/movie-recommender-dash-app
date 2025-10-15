import dash
import dash_bootstrap_components as dbc
from utils import fetch_movie_details
from dash import html, dcc, callback, Input, Output, State
# Registers this page as the movie details page using the path template
dash.register_page(__name__, path_template="/movie/tmdb/<tmdb_id>")
# Layout function for the movie details page
def layout(tmdb_id=None):
    details = fetch_movie_details(tmdb_id)
    if not details:
        return html.Div("Could not fetch movie from TMDB.")
    # Embeds YouTube trailer if available
    trailer_embed = html.Div([
        html.H5("🎞 Watch Trailer", className="text-primary"),
        html.Iframe(
            src=f"https://www.youtube.com/embed/{details['trailer']}",
            width="100%", height="400px",
            allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
        )
    ]) if details.get("trailer") else html.Div("No trailer available.", className="text-muted fst-italic")
    # Main layout of the movie details page
    return dbc.Container([
        dcc.Location(id="url"),
        html.Button("⬅ Back", id="actor-back", className="btn btn-secondary my-3"),
        dcc.ConfirmDialogProvider(
            children=html.Div(),
            id="js-trigger"
        ),
        #dcc.Link("⬅ Back", href="/", id="movie-back", className="btn btn-secondary my-3"),
        dbc.Card([
            dbc.Row([
                dbc.Col(html.Img(src=details["poster"], style={"width": "250px"}), md=4),
                dbc.Col([
                    html.H2(details["title"]),
                    html.P(f"📅 Release Date: {details['release_date']}"),
                    html.P(f"⏱ Runtime: {details['runtime']} minutes"),
                    html.P(f"🎭 Genres: {details['genres']}"),
                    html.P(f"⭐ Rating: {details['rating']} ({details['vote_count']} votes)"),
                    html.P(["🔗 Homepage: ", html.A("Visit", href=details["homepage"], target="_blank") if details["homepage"] else "Not available"]),
                    html.P(f"🏢 Production: {details.get('companies', 'N/A')}"),
                    html.P(f"🗣 Languages: {details.get('languages', 'N/A')}"),
                    html.Div([
                        html.H5("🎬 Top Cast", className="text-primary mt-3"),
                        dbc.Row([
                            dbc.Col([
                                html.A([
                                    html.Img(src=img, style={"width": "100px", "border-radius": "10px"}) if img else html.Div("No image"),
                                    html.P(name, className="text-center small")
                                ], href=f"/actor/{name.replace(' ', '%20')}", style={"textDecoration": "none", "color": "inherit"})
                            ], width="auto", className="mx-2 my-2") for name, img in zip(details['cast_names'], details['cast_imgs'])
                        ]) if details['cast_names'] else html.Div("No cast info.", className="text-muted")
                    ]),
                    html.P(details["overview"])
                ], md=8)
            ], className="p-3")
        ]),
        html.Div(className="my-4", children=trailer_embed)
    ], fluid=True)
# Callback for the smart back functionality
@callback(
    Output("movie-back", "href"),
    Input("url", "pathname"),
    State("previous-page", "data"),
    prevent_initial_call=True
)
def update_back_href(_, previous_page):
    return previous_page or "/"