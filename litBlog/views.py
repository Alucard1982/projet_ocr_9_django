from itertools import chain

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import CharField, Value

from litBlog.form import TicketForm, ReviewForm
from litBlog.models import Ticket, Review, UserFollows


@login_required(login_url='login_blog')
def flux(request):
    try:
        all_ticket = Ticket.objects.all()
    except Ticket.DoesNotExist:
        raise Http404('Ticket does not exist')
    all_ticket = all_ticket.annotate(content_type=Value('TICKET', CharField()))
    try:
        all_review = Review.objects.all()
    except Review.DoesNotExist:
        raise Http404('Ticket does not exist')
    all_review = all_review.annotate(content_type=Value('REVIEW', CharField()))
    posts = sorted(chain(all_ticket, all_review), key=lambda post: post.time_created, reverse=True)
    context = {'posts': posts}
    return render(request, 'flux.html', context)


@login_required(login_url='login_blog')
def post(request):
    try:
        own_ticket = Ticket.objects.filter(user=request.user)
    except Ticket.DoesNotExist:
        raise Http404('Ticket does not exist')
    sorted_all_ticket = sorted(own_ticket, key=lambda ticket: ticket.time_created, reverse=True)
    context = {'own_ticket': sorted_all_ticket}
    return render(request, 'post.html', context)


@login_required(login_url='login_blog')
def ticket(request, id_ticket=None):
    instance_ticket = get_object_or_404(Ticket, pk=id_ticket) if id_ticket is not None else None
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=instance_ticket)
        if form.is_valid():
            form.save()
            return redirect('flux')
    else:
        form = TicketForm(instance=instance_ticket)
    context = {'form': form}
    return render(request, 'ticket.html', context)


def delete_ticket(request, id_ticket):
    ticket = get_object_or_404(Ticket, pk=id_ticket)
    ticket.delete()
    return redirect('flux')


def review(request, id_ticket=None):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('flux')
    else:
        form = ReviewForm()
    instance_ticket = get_object_or_404(Ticket, pk=id_ticket)
    context = {'form': form, 'ticket': instance_ticket}
    return render(request, 'review.html', context)
