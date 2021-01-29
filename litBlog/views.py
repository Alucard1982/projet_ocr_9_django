from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.db.models import CharField, Value

from litBlog.form import TicketForm, ReviewForm, FollowForm
from litBlog.models import Ticket, Review, UserFollows, User


@login_required(login_url='login_blog')
def flux(request):
    ticket_button_hide = []
    try:
        all_ticket = Ticket.objects.filter(boolean=False)
    except Ticket.DoesNotExist:
        raise Http404('Ticket does not exist')
    try:
        all_review = Review.objects.all()
    except Review.DoesNotExist:
        raise Http404('Review does not exist')
    all_ticket = all_ticket.annotate(content_type=Value('TICKET', CharField()))
    all_review = all_review.annotate(content_type=Value('REVIEW', CharField()))
    posts = sorted(chain(all_ticket, all_review), key=lambda post: post.time_created, reverse=True)
    for review in all_review:
        if request.user == review.user:
            ticket_button_hide.append(review.ticket.id)
    context = {'posts': posts, 'ticket_button_hide': ticket_button_hide}
    return render(request, 'flux.html', context)


@login_required(login_url='login_blog')
def post(request):
    try:
        own_ticket = Ticket.objects.filter(user=request.user)
    except Ticket.DoesNotExist:
        raise Http404('Ticket does not exist')
    try:
        own_review = Review.objects.filter(user=request.user)
    except Review.DoesNotExist:
        raise Http404('Review does not exist')
    own_ticket = own_ticket.annotate(content_type=Value('TICKET', CharField()))
    own_review = own_review.annotate(content_type=Value('REVIEW', CharField()))
    posts = sorted(chain(own_ticket, own_review), key=lambda post: post.time_created, reverse=True)
    context = {'posts': posts}
    return render(request, 'post.html', context)


@login_required(login_url='login_blog')
def post_user_following(request):
    ticket_button_hide = []
    form = FollowForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            users_following_ticket = Ticket.objects.filter(user__followed_by__user=request.user).filter(user__username=username)
        except Ticket.DoesNotExist:
            raise Http404('ticket does not exist')
        try:
            followed_review = Review.objects.filter(user__followed_by__user=request.user).filter(user__username=username)
        except Review.DoesNotExist:
            raise Http404('Review does not exist')
        followed_ticket = users_following_ticket.annotate(content_type=Value('TICKET', CharField()))
        followed_review = followed_review.annotate(content_type=Value('REVIEW', CharField()))
        posts = sorted(chain(followed_ticket, followed_review), key=lambda post: post.time_created, reverse=True)
    else:
        try:
            users_following_ticket = Ticket.objects.filter(user__followed_by__user=request.user)
        except Ticket.DoesNotExist:
            raise Http404('ticket does not exist')
        try:
            followed_review = Review.objects.filter(user__followed_by__user=request.user)
        except Review.DoesNotExist:
            raise Http404('ticket does not exist')
        followed_ticket = users_following_ticket.annotate(content_type=Value('TICKET', CharField()))
        followed_review = followed_review.annotate(content_type=Value('REVIEW', CharField()))
        posts = sorted(chain(followed_ticket, followed_review), key=lambda post: post.time_created, reverse=True)
    all_review = Review.objects.all()
    for review in all_review:
        if request.user == review.user:
            ticket_button_hide.append(review.ticket.id)
    context = {'posts': posts, 'ticket_button_hide': ticket_button_hide, 'form': form}
    return render(request, 'post_following_user.html', context)


@login_required(login_url='login_blog')
def ticket(request, id_ticket=None):
    instance_ticket = get_object_or_404(Ticket, pk=id_ticket) if id_ticket is not None else None
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=instance_ticket)
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


@login_required(login_url='login_blog')
def review(request, id_ticket=None, id_review=None):
    instance_ticket = get_object_or_404(Ticket, pk=id_ticket)
    instance_review = get_object_or_404(Review, pk=id_review) if id_review is not None else None
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=instance_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = instance_ticket
            review.save()
            return redirect('flux')
    else:
        form = ReviewForm(instance=instance_review)
    context = {'form': form, 'ticket': instance_ticket}
    return render(request, 'review.html', context)


def delete_review(request, id_review):
    review = get_object_or_404(Review, pk=id_review)
    review.delete()
    return redirect('flux')


@login_required(login_url='login_blog')
def own_review(request):
    if request.method == 'POST':
        form_ticket = TicketForm(request.POST, request.FILES)
        form_review = ReviewForm(request.POST)
        if form_ticket.is_valid():
            ticket = form_ticket.save(commit=False)
            ticket.boolean = True
            ticket.save()
            return redirect('own_review')
        if form_review.is_valid():
            try:
                instance_ticket = Ticket.objects.filter(user=request.user)
            except Ticket.DoesNotExist:
                raise Http404('Ticket does not exist')
            sorted_instance_ticket = sorted(instance_ticket, key=lambda ticket: ticket.pk, reverse=True)
            review = form_review.save(commit=False)
            review.ticket = sorted_instance_ticket[0]
            review.save()
            return redirect('flux')
    else:
        form_ticket = TicketForm()
        form_review = ReviewForm()
    context = {'form_ticket': form_ticket, 'form_review': form_review}
    return render(request, 'own_review.html', context)


@login_required(login_url='login_blog')
def follow(request):
    try:
        users = User.objects.all()
    except User.DoesNotExist:
        raise Http404("User does not exist")
    if request.method == "POST":
        username = request.POST.get('username')
        for user in users:
            if user.username == username:
                if user.username == request.user.username:
                    messages.info(request, 'Cant following you')
                else:
                    user_follow = UserFollows(user=request.user, followed_user=user)
                    user_follow.save()
                return redirect('abonnements')
        else:
            messages.info(request, 'Username does not exist')
    form = FollowForm()
    try:
        users_following = UserFollows.objects.filter(user=request.user)
        users_follower = UserFollows.objects.filter(followed_user=request.user)
    except UserFollows.DoesNotExist:
        raise Http404("UserFollows does not exist")
    context = {'form': form, 'users_following': users_following, 'users_follower': users_follower}
    return render(request, 'abonnements.html', context)


def delete_follow(request, id_follow):
    follow_user = get_object_or_404(UserFollows, pk=id_follow)
    follow_user.delete()
    return redirect('abonnements')
