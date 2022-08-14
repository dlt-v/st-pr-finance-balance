from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Entry
from django.contrib.auth.decorators import login_required


@login_required(redirect_field_name='')
def index(request):
    # if not request.user.is_authenticated:
    #     return redirect('login:login')
    entries = Entry.objects.all()
    context = {
        'entries': entries
    }
    return render(request, 'savings/index.html', context)


def detail(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)
    return render(request, 'savings/detail.html', {'entry': entry})
