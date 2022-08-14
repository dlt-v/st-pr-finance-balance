from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Entry
from django.contrib.auth.decorators import login_required
from django.db.models import Sum


# @login_required(redirect_field_name='')
def index(request):
    if not request.user.is_authenticated:
        return redirect('login:login')
    if request.method == 'POST':
        title = request.POST['title']
        value = request.POST['value']
        entry = Entry(title=title, value=value, owner=request.user)
        entry.save()

    entries = Entry.objects.filter(owner=request.user).order_by('-id')
    value_sum = Entry.objects.filter(owner=request.user).aggregate(Sum('value'))['value__sum']
    leftover_sum: int = value_sum
    context_entries = []
    for entry in entries:
        leftover_sum -= entry.value
        new_context_entry = {
            'title': entry.title,
            'value': entry.value,
            'created_at': entry.created_at,
            'leftover': leftover_sum
        }
        context_entries.append(new_context_entry)

    context = {
        'entries': context_entries,
        'value_sum': value_sum,
    }
    return render(request, 'savings/index.html', context)


def detail(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)
    return render(request, 'savings/detail.html', {'entry': entry})
