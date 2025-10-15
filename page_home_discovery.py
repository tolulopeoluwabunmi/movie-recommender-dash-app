import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html, dcc, Input, Output, State, ctx
from movie_data_loader import load_movie_full
from utils import render_movie_cards

# Registers this page as the home page
dash.register_page(__name__, path='/', name="Home")

# Loads and processes the movie dataset
movie_df = load_movie_full()
movie_df['year'] = movie_df['title'].str.extract(r'\((\d{4})\)').astype(float)  # Extracts movie year
movie_df['tmdbId'] = movie_df['tmdbId'].astype('Int64')   # Ensures TMDB ID is an integer
movie_df.drop_duplicates(subset='title', inplace=True)     # Removes duplicate titles
PER_PAGE = 8

genres_list = sorted(set(g for genre_str in movie_df['genres'].dropna() for g in genre_str.split('|')))

# Layout of the home page
layout = dbc.Container([
    dcc.Store(id="current-page", data=0),   # Stores the current page number for pagination
    # Page header with a gradient background
    html.Div(className="text-center p-4 mb-4", style={"background": "linear-gradient(to right, #007bff, #00c6ff)", "color": "white", "borderRadius": "12px"}, children=[
        html.H1("🎬 Movie Recommender", className="fw-bold"),
        html.P("Discover movies by tag, genre, or title", className="lead fst-italic")
    ]),

    # Search and filter section
    dbc.Row([
        dbc.Col(dcc.Input(id='tag-input', type='text', placeholder='Search by tag, genre, or title...', className='form-control'), md=5),
        dbc.Col(dcc.Dropdown(id='genre-filter', options=[{'label': g, 'value': g} for g in genres_list], placeholder='Filter by genre...', className='form-control'), md=3),
        dbc.Col(dcc.Dropdown(id='sort-select', options=[{'label': 'Sort by Rating', 'value': 'rating'}, {'label': 'Sort by Year', 'value': 'year'}], value='rating', clearable=False, className='form-control'), md=3),
        dbc.Col(dbc.Button("Search", id='search-btn', color='primary', className='w-100 fw-bold'), md=2)
    ], className='my-3'),
    dcc.Loading(id="loading-results", type="default", children=html.Div(id='result-area')), # Loading spinner and result area for movie cards
    # Pagination controls (Previous and Next buttons)
    dbc.Row([
        dbc.Col(dbc.Button("⏪ Previous", id='prev-page', color='info', className='fw-bold'), width='auto'),
        dbc.Col(dbc.Button("Next ⏩", id='next-page', color='info', className='fw-bold'), width='auto')
    ], className='justify-content-center my-2'),
    html.Hr(),
# Top 10 most common genres chart
    html.H4(" Top 10 Most Common Genres", className="mt-4 text-success fw-bold"),
    dcc.Graph(id='top-genres-chart'),
    html.Hr()
], fluid=True)
# Callback to filter and recommend movies
@dash.callback(
    Output('result-area', 'children'),
    [Input('search-btn', 'n_clicks'), Input('current-page', 'data'), Input('top-genres-chart', 'clickData')],
    [State('tag-input', 'value'), State('sort-select', 'value'), State('genre-filter', 'value')]
)
def recommend_movies(n_clicks, current_page, click_data, tag, sort_by, genre_filter):
    try:
        selected_genre = click_data['points'][0]['x'] if click_data else genre_filter
        filtered = movie_df
        # Filters by selected genre
        if selected_genre:
            filtered = filtered[filtered['genres'].str.contains(selected_genre, case=False, na=False)]

        if tag:
            filtered = filtered[
                filtered['tag'].str.contains(tag, case=False, na=False) |
                filtered['genres'].str.contains(tag, case=False, na=False) |
                filtered['title'].str.contains(tag, case=False, na=False)
            ]

        filtered = filtered.drop_duplicates(subset='title').sort_values(by=sort_by, ascending=False)
        page_data = filtered.iloc[current_page * PER_PAGE:(current_page + 1) * PER_PAGE]
        return render_movie_cards(page_data) if not page_data.empty else html.Div("No matching movies found.")
    except Exception as e:
        return html.Div(f"⚠ Error occurred: {e}")
# Callback to update the current page number for pagination
@dash.callback(Output("current-page", "data"), [Input("next-page", "n_clicks"), Input("prev-page", "n_clicks")], State("current-page", "data"))
def update_page(next_clicks, prev_clicks, current_page):
    if ctx.triggered_id == "next-page":
        return current_page + 1
    elif ctx.triggered_id == "prev-page" and current_page > 0:
        return current_page - 1
    return current_page
# Callback to generate the Top 10 genres chart
@dash.callback(Output('top-genres-chart', 'figure'), Input('result-area', 'children'))
def update_top_genres_chart(_):
    genre_series = movie_df['genres'].dropna().str.split('|').explode().str.strip()
    genre_counts = genre_series.value_counts().nlargest(10)
    fig = px.bar(x=genre_counts.index, y=genre_counts.values, labels={'x': 'Genre', 'y': 'Count'}, title='Top 10 Most Common Genres')
    fig.update_layout(title_x=0.5)
    return fig