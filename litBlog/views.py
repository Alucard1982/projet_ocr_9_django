from django.shortcuts import render, redirect, get_object_or_404

from litBlog.form import TicketForm, ReviewtForm
from litBlog.models import Ticket, Review, UserFollows

from django.contrib.auth.decorators import login_required


@login_required(login_url='login_blog')
def flux(request):
    all_ticket = Ticket.objects.all()
    sorted_all_ticket = sorted(all_ticket, key=lambda ticket: ticket.time_created, reverse=True)
    context = {'all_ticket': sorted_all_ticket}
    return render(request, 'flux.html', context)


@login_required(login_url='login_blog')
def post(request):
    own_ticket = Ticket.objects.filter(user=request.user)
    sorted_all_ticket = sorted(own_ticket, key=lambda ticket: ticket.time_created, reverse=True)
    context = {'own_ticket': sorted_all_ticket}
    return render(request, 'post.html', context)


@login_required(login_url='login_blog')
def ticket(request, id_ticket=None):
    instance_ticket = Ticket.objects.get(pk=id_ticket) if id_ticket is not None else None
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

def review(request):

