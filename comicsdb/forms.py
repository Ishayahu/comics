# -*- coding: utf-8 -*-

from django import forms
from comicsdb.models import *


class StoryForm(forms.Form):
    name = forms.CharField(label='Название', max_length=200)
    plot = forms.CharField(label='Краткое содержание', widget = forms.Textarea)
    rating = forms.IntegerField(label='Рейтинг', min_value=-1, max_value=11, widget = forms.NumberInput)
    artists = forms.ModelMultipleChoiceField(label='Художник(и)',queryset=Human.objects.all())
    scriptwriters = forms.ModelMultipleChoiceField(label='Сценаристы(и)',queryset=Human.objects.all())
    issues = forms.ModelMultipleChoiceField(label='Выпуск(и)',queryset=Issue.objects.all())
    characters = forms.ModelMultipleChoiceField(label='Герой(и)',queryset=Character.objects.all())
