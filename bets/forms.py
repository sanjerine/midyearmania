# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from .models import CustomUser, Team, Bet, Match

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email", "points")

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email", "points")

class PlaceBetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PlaceBetForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Bet
        fields = ['choice', 'amount', 'match']
    
    def clean(self):
        cleaned_data = super(PlaceBetForm, self).clean()
        if self.cleaned_data['amount'] > getattr(self.user, 'points'):
            raise ValidationError("Error! You cannot bet more points than you have!")
        if self.cleaned_data['amount'] < 0:
            raise ValidationError("You can't bet negative points!")
        # can't bet on yourself
        if getattr(self.user, 'team') == self.cleaned_data['choice']:
            raise ValidationError("You can't bet on your own team!")
        # cant bet on a team in a match you're in
        match = self.cleaned_data['match']
        match = Match.objects.filter(id=getattr(match,'id'))
        teams = list(match.values_list('teams__name', flat=True))
        if str(getattr(self.user, 'team')) in teams:
            raise ValidationError("You can't bet on a match you're in!")
        # cant bet on team if youve already bet on a different team for the same match
        # first, get all bets for this match placed by this player
        placed_bets = Bet.objects.filter(match=self.cleaned_data['match']) # all bets for this match
        placed_bets = placed_bets.filter(player=self.user) # just by this player
        # check the team of the 1st one
        if len(placed_bets) > 0:
            print(self.cleaned_data)
            team_choice = getattr(placed_bets[0], "choice")
            if self.cleaned_data['choice'] != team_choice:
                raise ValidationError("You can't bet for a different team! You've already placed a bet!")
        return self.cleaned_data