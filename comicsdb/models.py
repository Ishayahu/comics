# -*- coding: utf-8 -*-

from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Human(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    patronymic = models.CharField(max_length=200, blank=True)
    comment = models.TextField(blank=True)
    aliases = models.TextField(blank=True)
    link = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ["surname"]

    def __str__(self):
        return "{} {} {}".format(self.surname, self.name, self.patronymic)


class Series(models.Model):
    name = models.CharField(max_length=200)
    start_year = models.DateField(null=True, blank=True)
    first_issue = models.ForeignKey('Issue', related_name='first_issue', on_delete=models.PROTECT, null=True,
                                    blank=True)
    end_year = models.DateField(null=True, blank=True)
    end_issue = models.ForeignKey('Issue', related_name='end_issue', on_delete=models.PROTECT, null=True, blank=True)
    publisher = models.ForeignKey('Publisher', on_delete=models.PROTECT)

    def __str__(self):
        return "{} @{}".format(self.name, self.publisher.name)


class Issue(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    comment = models.TextField(blank=True)
    series = models.ForeignKey('Series', on_delete=models.PROTECT)
    cover_artist = models.ForeignKey('Human', on_delete=models.PROTECT, blank = True, null = True)

    def __str__(self):
        return "{} @{} / {}".format(self.name, self.date, self.series)

class StoryArc(models.Model):
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}: {self.comment}"


class Story(models.Model):
    name = models.CharField(max_length=200)
    annotation = models.TextField(blank = True)
    plot = models.TextField(blank=True)
    rating = models.IntegerField(null=True, blank=True)
    # issue = models.ForeignKey('Issue', on_delete=models.PROTECT)
    scriptwriters = models.ManyToManyField('Human', related_name='screenwriter', blank = True, null = True)
    artists = models.ManyToManyField('Human', related_name='artist', blank = True, null = True)
    inker = models.ManyToManyField('Human', related_name='inker', blank = True, null = True)
    letterer = models.ManyToManyField('Human', related_name='letterer', blank = True, null = True)
    colorist = models.ManyToManyField('Human', related_name='colorist', blank = True, null = True)
    editor = models.ManyToManyField('Human', related_name='editor', blank = True, null = True)
    issues = models.ManyToManyField('Issue')
    story_arc = models.ManyToManyField('StoryArc', related_name='stories', blank=True, null=True)
    characters = models.ManyToManyField('Character', blank=True)
    video_url = models.URLField(blank=True)

    def first_issue_date(self):
        return sorted(self.issues.all(), key=lambda x: x.date)[0].date

    def __str__(self):
        return "[{}] {} 🖊 {} 🖌 {} @{}".format(str(self.rating),
                                                self.name,
                                                ",".join(map(str, self.scriptwriters.all())),
                                                ",".join(map(str, self.artists.all())),
                                                ",".join(map(str, self.issues.all()))
                                                )

    def safe_plot(self):
        return self.plot.replace('\n','<p>')

# class StoryScripwriters(models.Model):
#     story = models.ForeignKey("Story", on_delete=models.PROTECT)
#     scriptwriter = models.ForeignKey('Human', related_name='Сценарист', on_delete=models.PROTECT)
#
#     def __str__(self):
#         return "{} 🖊 {}".format(self.scriptwriter.surname, self.story.name)


# class StoryArtists(models.Model):
#     story = models.ForeignKey("Story", on_delete=models.PROTECT)
#     artist = models.ForeignKey('Human', related_name='Художник', on_delete=models.PROTECT)
#
#     def __str__(self):
#         return "{} 🖌 {}".format(self.artist.surname, self.story.name)


# class StoryIssue(models.Model):
#     story = models.ForeignKey("Story", on_delete=models.PROTECT)
#     issue = models.ForeignKey('Issue', on_delete=models.PROTECT)
#
#     def __str__(self):
#         return "{} @{}".format(self.story.name, self.issue.name)


class Character(models.Model):
    name = models.CharField(max_length=200)
    key_events = models.TextField(blank = True)
    powers = models.TextField(blank=True)
    weaknesses = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Opponents(models.Model):
    good = models.ForeignKey('Character', related_name='Hero', on_delete=models.PROTECT)
    bad = models.ForeignKey('Character', related_name='Enemy', on_delete=models.PROTECT)
    story = models.ForeignKey('Story', on_delete=models.PROTECT)

    def __str__(self):
        return "{} vs {} @{}".format(self.good.name, self.bad.name, self.story.name)


class Command(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class CommandIssue(models.Model):
    command = models.ForeignKey('Command', on_delete=models.PROTECT)
    issue = models.ForeignKey('Issue', on_delete=models.PROTECT)

    def __str__(self):
        return "{} @{}".format(self.command.name, self.issue.name)


class CharacterCommand(models.Model):
    character = models.ForeignKey('Character', on_delete=models.PROTECT)
    command = models.ForeignKey('Command', on_delete=models.PROTECT)
    comment = models.TextField()

    def __str__(self):
        return "{} @{}".format(self.character.name, self.command.name)


# class CharacterStory(models.Model):
#     character = models.ForeignKey('Character', on_delete=models.PROTECT)
#     story = models.ForeignKey('Story', on_delete=models.PROTECT)
#     comment = models.TextField(blank=True)
#
#     def __str__(self):
#         return "{} @{}".format(self.character.name, self.story.name)
