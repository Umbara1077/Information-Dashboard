from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.core.paginator import Paginator
from .services import (
    fetch_recent_games,
    fetch_now_playing_movies,
    fetch_upcoming_movies,
    fetch_now_in_theaters,
    fetch_tech_news,
    fetch_general_news,
    fetch_recent_games,
    fetch_game_detail,
    fetch_movie_detail,
)

class DashboardView(TemplateView):
    template_name = 'board/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['games']          = fetch_recent_games(limit=6, days=30)
        ctx['movies_now']     = fetch_now_playing_movies(limit=8)
        ctx['movies_upcoming']= fetch_upcoming_movies(limit=8)
        ctx['movies_theaters']= fetch_now_in_theaters(limit=8)
        ctx['tech_news']       = fetch_tech_news(limit=6)
        ctx['general_news']    = fetch_general_news(limit=6)
        return ctx
    
ITEMS_PER_PAGE = 30

# ── Games ──
class GameListView(View):
    def get(self, request):
        page = request.GET.get('page', 1)
        games = fetch_recent_games(limit=100, days=90)
        paginator = Paginator(games, ITEMS_PER_PAGE)
        pg = paginator.get_page(page)
        return render(request, 'board/games_list.html', {'page_obj': pg})

class GameDetailView(TemplateView):
    template_name = 'board/games_detail.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['game'] = fetch_game_detail(kwargs['game_id'])
        return ctx

# ── Movies ──
class MovieListView(View):
    def get(self, request):
        page = request.GET.get('page', 1)
        movies = fetch_now_playing_movies(limit=100)
        paginator = Paginator(movies, ITEMS_PER_PAGE)
        pg = paginator.get_page(page)
        return render(request, 'board/movies_list.html', {'page_obj': pg})

class MovieDetailView(TemplateView):
    template_name = 'board/movies_detail.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['movie'] = fetch_movie_detail(kwargs['movie_id'])
        return ctx

# ── News ──
class TechNewsListView(View):
    def get(self, request):
        page = request.GET.get('page', 1)
        articles = fetch_tech_news(limit=100)
        paginator = Paginator(articles, ITEMS_PER_PAGE)
        pg = paginator.get_page(page)
        return render(request, 'board/news_list.html', {
            'page_obj': pg,
            'title': 'Tech News',
        })

class GeneralNewsListView(View):
    def get(self, request):
        page = request.GET.get('page', 1)
        articles = fetch_general_news(limit=100)
        paginator = Paginator(articles, ITEMS_PER_PAGE)
        pg = paginator.get_page(page)
        return render(request, 'board/news_list.html', {
            'page_obj': pg,
            'title': 'Top News',
        })