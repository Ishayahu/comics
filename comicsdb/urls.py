# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('latest/feed/', views.LatestEntriesFeed(), name='stories_feed'),
    path('add_story/', views.add_story, name='add_story'),
    path('show_story/<int:story_id>/', views.show_story, name='show_story'),
    path('list_stories/', views.list_stories, name='list_stories'),
    path('search_for_character/<int:character_id>/', views.search_for_character, name='search_for_character'),
]