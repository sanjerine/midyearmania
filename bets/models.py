# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.db.models import Sum
from django.db.models import Q

class Team(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    points = models.PositiveIntegerField(default=100)

    team = models.ForeignKey('Team', on_delete=models.RESTRICT, null=True, blank=True)
    # add additional fields in here

    def __str__(self):
        return self.username

    def get_points(self):
        return self.points

    def get_team(self):
        return self.team

    class Meta:
        ordering = ['-points']

class Match(models.Model):
    """Model representing a singular match."""
    name = models.CharField(max_length=500)
    start_time =  models.DateTimeField()
    points_awarded = models.CharField(default='', max_length=500, help_text='Int array of length 2, string separated by commas') # string separated by commas
    betpool_points = models.PositiveIntegerField(default=20)
    teams = models.ManyToManyField('Team', related_name='teams', blank=True,)
    winner = models.ForeignKey('Team', on_delete=models.RESTRICT, related_name='winner', null=True, blank=True,)
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('match-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super(Match, self).save(*args, **kwargs)
        if self.winner is not None:
            # Adding pure points to each member of every team
            awarded = self.points_awarded.split(',')
            winners = CustomUser.objects.filter(team=self.winner)
            win_amt = int(awarded[0])/winners.count()    
            for person in winners:
                person.points += win_amt
                person.save()
            for team in self.teams.all():
                if team == self.winner:
                    continue
                losers = CustomUser.objects.filter(team=team)
                lose_amt = int(awarded[1])/losers.count() 
                for person in losers:
                    person.points += lose_amt
                    person.save()
            # Now, logic and database updates for betting.
            # Formula for betting is per person is:
            # sum_of_bets (incl betpool points)
            # ratio = person_pool/sum_of_winning_bets
            # per person is: sum_of_bets * person_pool/sum_of_winning_bets
            bets_models = Bet.objects.filter(match=self)

            sum_of_bets = bets_models.aggregate(Sum('amount'))['amount__sum'] # sum of all bets
            sum_of_bets += self.betpool_points
            sum_of_winning_bets = bets_models.filter(choice=self.winner).aggregate(Sum('amount'))['amount__sum'] # sum of winning bets
            
            for person in bets_models.filter(choice=self.winner).order_by().values_list('player').distinct(): # for each person who chose the winning team
                person_pool = bets_models.filter(player=person).aggregate(Sum('amount'))['amount__sum'] # how much they bet on the match
                person_ratio = person_pool/sum_of_winning_bets
                person_payout = round(person_ratio*sum_of_bets) # payout = ratio * total sum
                # now, update the db record for the person
                peep = CustomUser.objects.get(id=person[0])
                peep.points += person_payout
                peep.save()

            


class Bet(models.Model):
    player = models.ForeignKey(CustomUser, on_delete=models.RESTRICT) # should this be AbstractUser or User
    match = models.ForeignKey("Match", on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    choice = models.ForeignKey('Team', on_delete=models.RESTRICT, related_name='choice', null=True)

    def __str__(self):
        """String for representing the Model object."""
        return 'A bet'
        
    class Meta:
        ordering = ['-amount']