from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django.db import DatabaseError

from main.models import Link
from main.models import Tag

import re


def index(request):
    # Request the context of the request
    # The context contains information such as the client's machine details,
    # for example.
    context = RequestContext(request)

    # Get all links
    links = Link.objects.all()

    return render_to_response('main/index.html', {'links': links}, context)


def tags(request):
    context = RequestContext(request)

    # Get all tags
    tags = Tag.objects.all()

    return render_to_response('main/tags.html', {'tags': tags}, context)


def tag(request, tag_name):
    context = RequestContext(request)
    the_tag = Tag.objects.get(name=tag_name)
    links = the_tag.link_set.all()
    return render_to_response('main/index.html', {'links': links, 'tag_name':
                              '#' + tag_name}, context)


def add_link(request):
    context = RequestContext(request)
    if request.method == 'POST':
        url = request.POST.get('url', '')
        tags = request.POST.get('tags', '')
        title = request.POST.get('title', '')

        try:
            link = Link.objects.create(url=url, title=title)
        except DatabaseError:
            # link already exists
            return redirect(index)

        tag_array = tags.split(r'; |, ')

        for t in tag_array:
            # Add the tags to the tag_array.
            # Create a new tag if it does not exist.
            try:
                tag = Tag.objects.get(name=t)
            except Tag.DoesNotExist:
                tag = Tag.objects.create(name=t)
            link.tags.add(tag)

    return redirect(index)
