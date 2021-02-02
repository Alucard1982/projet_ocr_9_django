from django import forms
from litBlog.models import Ticket, Review


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("title", "description", "image")


class ReviewForm(forms.ModelForm):
    CHOICES = [(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]
    rating = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect(attrs={"id": "test2"})
    )

    class Meta:
        model = Review
        fields = ("headline", "rating", "body")


class FollowForm(forms.Form):
    username = forms.CharField(
        max_length=200, widget=forms.TextInput(attrs={"placeholder": "INPUT USER "})
    )
