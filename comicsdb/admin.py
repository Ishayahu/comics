# -*- coding: utf-8 -*-

from django.contrib import admin
from comicsdb.models import *

admin.site.register(Publisher)
admin.site.register(Human)
admin.site.register(Series)
admin.site.register(Issue)
admin.site.register(Story)
# admin.site.register(StoryArtists)
# admin.site.register(StoryScripwriters)
admin.site.register(Character)
admin.site.register(CharacterCommand)
admin.site.register(Opponents)
admin.site.register(Command)
admin.site.register(CommandIssue)
admin.site.register(StoryArc)
# admin.site.register(StoryIssue)