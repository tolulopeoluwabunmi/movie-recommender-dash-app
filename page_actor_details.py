import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from utils import fetch_actor_bio_and_photo, fetch_actor_movies

dash.register_page(__name__, path_template="/actor/<actor_name>") # Registers this page as an actor details page using the path template
# Defines the layout for the actor details page
def layout(actor_name=None):
    display_name = actor_name.replace('%20', ' ')
    bio, profile_url = fetch_actor_bio_and_photo(display_name)
    movies = fetch_actor_movies(display_name)

    if not movies:
        return html.Div([
            html.Button("⬅ Back", id="actor-back", className="btn btn-secondary my-3"), # Back button
            dcc.ConfirmDialogProvider(children=[], id="js-trigger"),   # Trigger for JS back navigation
            html.H4(f"No TMDB results found for {display_name}.", className="text-danger")
        ])
    # Creates a list of movie cards (up to 10) for the actor
    cards = []
    for movie in movies[:10]:
        link = f"/movie/tmdb/{movie['id']}"
        poster_path = movie.get("poster_path")
        poster = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/300x450?text=No+Image"
        cards.append(
            dbc.Card([
                dcc.Link([
                    dbc.CardImg(src=poster, top=True),
                    dbc.CardBody(html.H5(f"{movie['title']} ({movie.get('release_date', '')[:4]})", className='card-title'))
                ], href=link, style={"textDecoration": "none", "color": "inherit"})
            ], className='m-2', style={'width': '18rem'})
        )
    # Main layout of the actor details page
    return dbc.Container([
        dcc.Location(id="url"),
        html.Button("⬅ Back", id="actor-back", className="btn btn-secondary my-3"),
        dcc.ConfirmDialogProvider(
            children=html.Div(),
            id="js-trigger"
        ),
        html.Div([
            html.Img(src=profile_url, style={"height": "200px", "border-radius": "15px"}),
            html.H3(display_name, className="mt-2"),
            html.P(bio or "No biography available.", className="text-muted")
        ], className="text-center my-3"),
        html.H2(f"Movies featuring {display_name}", className="text-primary my-4"),
        dbc.Row(cards, className='d-flex flex-wrap justify-content-center')
    ], fluid=True)