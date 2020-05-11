# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from comicsdb.models import Story, Character, StoryArc
from django.contrib.syndication.views import Feed


# Create your views here.
@login_required
def add_story(request):
    from comicsdb.forms import StoryForm
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StoryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            cd = form.cleaned_data
            # process the data in form.cleaned_data as required
            s = Story(name = cd['name'], plot = cd['plot'], rating = cd['rating'], annotation = cd['annotation'])
            s.save()
            for a in cd['artists']:
                # tmp = StoryArtists(story = s, artist = a)
                # tmp.save()
                s.artists.add(a)
            for a in cd['scriptwriters']:
                # tmp = StoryScripwriters(story = s, scriptwriter = a)
                # tmp.save()
                s.scriptwriters.add(a)
            for a in cd['inkers']:
                s.inker.add(a)
            for a in cd['letterers']:
                s.letterer.add(a)
            for a in cd['colorists']:
                s.colorist.add(a)
            for a in cd['editors']:
                s.editor.add(a)
            for a in cd['issues']:
                # tmp = StoryIssue(story = s, issue = a)
                # tmp.save()
                s.issues.add(a)
            for a in cd['characters']:
                # tmp = CharacterStory(story = s, character = a)
                # tmp.save()
                s.characters.add(a)
            s.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('add_story'))

        # if a GET (or any other method) we'll create a blank form
    else:
        form = StoryForm()

    return render(request, 'add_story.html', {'form': form})

def show_story(request, story_id):
    story = Story.objects.get(id = int(story_id))
    story.plot = story.plot.replace('\n','<p>')
    storyartists = story.artists.all()
    storyscriptwriters = story.scriptwriters.all()
    storyissues = story.issues.all()
    storycharacters = story.characters.all()
    inker = story.inker.all()
    letterer = story.letterer.all()
    colorist = story.colorist.all()
    editor = story.editor.all()
    print(storycharacters)
    # storyartists = StoryArtists.objects.filter(story = story)
    # storyscriptwriters = StoryScripwriters.objects.filter(story = story)
    # storyissues = StoryIssue.objects.filter(story = story)
    # storycharacters = CharacterStory.objects.filter(story = story)
    return render(request, 'show_story.html',
                  {'story': story,
                   'storyartists':storyartists,
                   'storyscriptwriters':storyscriptwriters,
                   'storyissues':storyissues,
                   'storycharacters':storycharacters,
                   'inkers':inker,
                   'letterers':letterer,
                   'colorists':colorist,
                   'editors':editor,
                   })
def get_story_by_name(request, publisher, series, story_name: str):
    story_name = story_name.replace('_',' ')
    story_name = story_name.lower()
    story = Story.objects.filter(name__iexact = story_name)

    if not story:
        return HttpResponseNotFound('Нет истории с таким названием :(')
    if len(story)>1:
        raise NotImplementedError('Реализовать выбор истории из списка')
    story = story[0]
    storyissues = story.issues.all()
    issue = storyissues[0]
    if issue.series.name.lower() != series.lower():
        return HttpResponseNotFound('Нет истории с таким названием и такой серией:(')
    if issue.series.publisher.name.lower() != publisher.lower():
        return HttpResponseNotFound('Нет истории с таким названием и такой серией и таким издательством:(')

    story.plot = story.plot.replace('\n','<p>')
    storyartists = story.artists.all()
    storyscriptwriters = story.scriptwriters.all()

    storycharacters = story.characters.all()
    inker = story.inker.all()
    letterer = story.letterer.all()
    colorist = story.colorist.all()
    editor = story.editor.all()
    print(storycharacters)
    # storyartists = StoryArtists.objects.filter(story = story)
    # storyscriptwriters = StoryScripwriters.objects.filter(story = story)
    # storyissues = StoryIssue.objects.filter(story = story)
    # storycharacters = CharacterStory.objects.filter(story = story)
    return render(request, 'show_story.html',
                  {'story': story,
                   'storyartists':storyartists,
                   'storyscriptwriters':storyscriptwriters,
                   'storyissues':storyissues,
                   'storycharacters':storycharacters,
                   'inkers':inker,
                   'letterers':letterer,
                   'colorists':colorist,
                   'editors':editor,
                   })

def list_stories(request):
    stories = sorted(Story.objects.all(),key = lambda x: x.id, reverse=True)
    arcs = StoryArc.objects.all()
    return render(request, 'list_stories.html', {'stories': stories, 'arcs': arcs})

def show_arc(request, arc_id):
    stories = sorted(Story.objects.filter(story_arc__id = arc_id), key = lambda x: x.first_issue_date(), reverse=True)
    # for s in stories:
    #     print (s)
    arcs = StoryArc.objects.all()
    return render(request, 'list_stories.html', {'stories': stories, 'arcs': arcs})

def search_for_character(request, character_id):
    character = Character.objects.get(id = character_id)
    stories = sorted(character.story_set.all(), key=lambda x: x.first_issue_date())
    return render(request, 'search_for_character.html', {'stories': stories, 'character':character})

class LatestEntriesFeed(Feed):
    title = "Краткое содержание комиксов"
    link = "/comicsdb/"
    description = "Пересказ сюжетов комиксов, чтобы быстро вспомнить"

    def items(self):
        return Story.objects.order_by('-pk')[:5]

    def item_title(self, item: Story):
        return item.name

    def item_description(self, item: Story):
        return item.plot

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item: Story):
        return reverse('show_story', args=[item.pk])