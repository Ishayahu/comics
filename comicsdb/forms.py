# -*- coding: utf-8 -*-

from django import forms
from comicsdb.models import *


class StoryForm(forms.Form):
    name = forms.CharField(label='Название', max_length=200)
    annotation = forms.CharField(label='Аннтотация', widget = forms.Textarea)
    plot = forms.CharField(label='Краткое содержание', widget = forms.Textarea)
    rating = forms.IntegerField(label='Рейтинг', min_value=-1, max_value=11, widget = forms.NumberInput)
    artists = forms.ModelMultipleChoiceField(label='Художник(и)',queryset=Human.objects.all().order_by('surname'), required=False)
    scriptwriters = forms.ModelMultipleChoiceField(label='Сценарист(ы)',queryset=Human.objects.all().order_by('surname'), required=False)
    inkers = forms.ModelMultipleChoiceField(label='Инкер(ы)',queryset=Human.objects.all().order_by('surname'), required=False)
    letterers = forms.ModelMultipleChoiceField(label='Летерер(ы)',queryset=Human.objects.all().order_by('surname'), required=False)
    colorists = forms.ModelMultipleChoiceField(label='Колорист(ы)',queryset=Human.objects.all().order_by('surname'), required=False)
    editors = forms.ModelMultipleChoiceField(label='Редактор(ы)',queryset=Human.objects.all().order_by('surname'), required=False)
    issues = forms.ModelMultipleChoiceField(label='Выпуск(и)',queryset=Issue.objects.all())
    characters = forms.ModelMultipleChoiceField(label='Герой(и)',queryset=Character.objects.all())
