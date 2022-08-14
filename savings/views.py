from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Entry
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

@login_required(redirect_field_name='')
def index(request):
    # if not request.user.is_authenticated:
    #     return redirect('login:login')
    if request.method == 'POST':
        title = request.POST['title']
        value = request.POST['value']
        entry = Entry(title=title, value=value, owner=request.user)
        entry.save()

    entries = Entry.objects.filter(owner=request.user).order_by('-created_at')
    value_sum = Entry.objects.filter(owner=request.user).aggregate(Sum('value'))
    context = {
        'entries': entries,
        'value_sum': value_sum['value__sum'],
    }
    return render(request, 'savings/index.html', context)


def detail(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)
    return render(request, 'savings/detail.html', {'entry': entry})
