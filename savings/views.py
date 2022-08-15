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
            'id': entry.id,
            'title': entry.title,
            'value': entry.value,
            'created_at': entry.created_at,
            'leftover': leftover_sum
        }
        context_entries.append(new_context_entry)
    dataset = []
    for i in range(12):
        val_by_month = Entry.objects.filter(created_at__month=i + 1).filter(owner=request.user).aggregate(Sum('value'))[
            'value__sum']
        if val_by_month is None:
            dataset.append(0)
            continue
        dataset.append(val_by_month)
    print(dataset)
    context = {
        'entries': context_entries,
        'value_sum': value_sum,
        'dataset': dataset
    }
    return render(request, 'savings/index.html', context)


def edit(request, entry_id):
    if not request.user.is_authenticated:
        return redirect('login:login')
    entry = get_object_or_404(Entry, pk=entry_id)
    if entry.owner == request.user:
        if request.method == "POST":
            entry.title = request.POST['title']
            entry.value = request.POST['value']
            entry.save()
            return redirect('savings:index')
        return render(request, 'savings/edit.html', {"entry": entry})
    else:
        return redirect('login:login')


def delete(request, entry_id):
    # Check if user is logged in at all.
    if not request.user.is_authenticated:
        return redirect('login:login')
    # Check if entry of this id exists and the user is the owner
    try:
        entry = Entry.objects.get(pk=entry_id)
        if entry.owner == request.user:
            entry.delete()
        else:

            return redirect('savings:index')
    except Entry.DoesNotExist:

        return redirect('savings:index')

    return redirect('savings:index')
