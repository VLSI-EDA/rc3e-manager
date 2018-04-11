"""
This file contains custom views which serve specific purposes that do not fit into the usual pattern.
"""

from django.shortcuts import render


def welcome(request):
    return render(request, "../templates/welcome.html")


def blank(request):
    return render(request, "../templates/blank.html")
