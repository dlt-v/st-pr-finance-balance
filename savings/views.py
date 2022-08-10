from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import Entry


def index(request):
    entries = Entry.objects.all()
    context = {
        'entries': entries
    }
    return render(request, 'savings/index.html', context)


def detail(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)
    return render(request, 'savings/detail.html', {'entry': entry})
