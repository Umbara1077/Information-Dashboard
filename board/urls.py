from django.urls import path
from .views import (
    DashboardView,
    GameListView,
    GameDetailView,
    MovieListView,
    MovieDetailView,
    TechNewsListView,
    GeneralNewsListView,
)

urlpatterns = [
    # Main Dashboard
    path('', DashboardView.as_view(), name='dashboard'),

    # Games
    path('games/', GameListView.as_view(), name='games-list'),
    path('games/<int:game_id>/', GameDetailView.as_view(), name='games-detail'),

    # Movies
    path('movies/', MovieListView.as_view(), name='movies-list'),
    path('movies/<int:movie_id>/', MovieDetailView.as_view(), name='movies-detail'),

    # News
    path('news/tech/', TechNewsListView.as_view(), name='tech-news'),
    path('news/general/', GeneralNewsListView.as_view(), name='general-news'),
]
