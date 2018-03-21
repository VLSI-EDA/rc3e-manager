from django.shortcuts import render


def welcome(request):
    return render(request, "../templates/welcome.html")
