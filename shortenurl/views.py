import json
import re

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Links
from .serializers import LinksSerializer
import string
import random


def home(request):
    links = Links.objects.get_active()
    short_links = []
    for link in links:
        short_links.append(request.build_absolute_uri(reverse('navigate_url', kwargs={'surl': link.short_url})))
    context = {"links": short_links}
    return render(request, 'shortenurl/index.html', context)
    # return HttpResponse('My first view.')


def generate_short_code():
    chars = string.ascii_letters+string.digits
    base = len(chars)
    code = ''
    for i in range(6):
        code += chars[random.randint(0, base-1)]
    try:
        Links.objects.get(short_url=code)
        generate_short_code()
    except Links.DoesNotExist:
        return code


@api_view(['GET', 'DELETE'])
def get_delete_link(request, surl):
    link = get_object_or_404(Links, short_url=surl)

    # get details of a single link
    if request.method == 'GET':
        serializer = LinksSerializer(link)
        return Response(serializer.data)

    # delete a record
    elif request.method == 'DELETE':
        link.active = False
        link.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def get_post_link(request):
    # get all links
    if request.method == 'GET':
        links = Links.objects.get_active()
        serializer = LinksSerializer(links, many=True)
        # serializer.data["short_url"] = request.build_absolute_uri(reverse('navigate_url', kwargs={'surl': links.short_url}))
        return Response(serializer.data)

    # insert a new record
    elif request.method == 'POST':
        main_url = re.sub(r"^(http[s]?://)?(www.)?", "http://", request.data.get('main_url'))
        try:
            link = Links.objects.get(main_url=main_url)
            if not link.active:
                link.active = True
                link.save()
                print(link.active)
            return redirect(reverse("get_delete_link", kwargs={'surl': link.short_url}))
        except Links.DoesNotExist:
            short_code = generate_short_code()
            data = {'main_url': main_url,
                    'short_url': short_code}
            serializer = LinksSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                # shortened_url = request.build_absolute_uri(reverse('navigate_url', kwargs={'surl': short_code}))
                # context = serializer.data
                # context["shortened_url"] = shortened_url
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def navigate_url(request, surl):
    """Redirects url with short url code to the original url"""

    main_url = get_object_or_404(Links, short_url=surl).main_url
    return redirect(main_url, permanent=True)
