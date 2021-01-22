from django import forms
from litBlog.models import Ticket, Review


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')


class ReviewtForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
