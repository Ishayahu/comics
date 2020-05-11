# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('latest/feed/', views.LatestEntriesFeed(), name='stories_feed'),
    path('story/add/', views.add_story, name='add_story'),
    path('story/show/<int:story_id>/', views.show_story, name='show_story'),
    path('arc/show/<int:arc_id>/', views.show_arc, name='show_arc'),
    path('stories/list/', views.list_stories, name='list_stories'),
    path('character/search_for/<int:character_id>/', views.search_for_character, name='search_for_character'),
]