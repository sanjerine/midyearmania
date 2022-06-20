from django.shortcuts import render
from django.db.models import Sum
from django.views import generic
import datetime
# Create your views here.
from .models import CustomUser, Match, Bet, Team
from django.views.generic.edit import FormView, CreateView
from bets.forms import PlaceBetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from django.contrib.auth.forms import PasswordChangeForm

def index(request):
    """View function for home page of site."""

    names = Team.objects.all()[:4]
    counts = []
    for i in range(4):
        team_lst = CustomUser.objects.all().filter(team__name=str(names[i]))
        if team_lst.count() == 0:
            counts.append(0)
            continue 
        sum = team_lst.aggregate(Sum('points'))['points__sum'] 
        avg = sum/team_lst.count() 
        counts.append(round(avg,1))
    names = [str(x) for x in names]
    standings = list(zip(names, counts))
    sorted_standings=sorted(standings, key = lambda x: x[1], reverse=True)

    t1 = {
        'name': sorted_standings[0][0],
        'count': sorted_standings[0][1] 
    }
    t2 = {
        'name': sorted_standings[1][0],
        'count': sorted_standings[1][1] 
    }
    t3 = {
        'name': sorted_standings[2][0],
        'count': sorted_standings[2][1] 
    }
    t4 = {
        'name': sorted_standings[3][0],
        'count': sorted_standings[3][1] 
    }
    
    # match information
    
    time = timezone.now()
    matches = Match.objects.filter(start_time__gte=time)
    matches_past = Match.objects.filter(start_time__lte=time)
    matches_pool = []
    matches_past_pool = []
    for match in matches:
        amt = Bet.objects.filter(match=match).aggregate(Sum('amount'))['amount__sum'] or int(0)
        amt += match.betpool_points
        matches_pool.append(amt)    
    for match in matches_past:
        amt = Bet.objects.filter(match=match).aggregate(Sum('amount'))['amount__sum'] or int(0)
        amt += match.betpool_points
        matches_past_pool.append(amt) 

    context = {
        't1': t1,
        't2': t2,
        't3': t3,
        't4': t4,
        'matches_len': matches_pool,
        'matches_past_len': matches_past_pool,
        'matches_pool': zip(matches,matches_pool),
        'matches_past_pool': zip(matches_past,matches_past_pool)
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class PlaceBetView(LoginRequiredMixin, CreateView):
    model = Bet
    #fields = ['choice', 'amount']
    form_class = PlaceBetForm
    template_name = 'bets.html'
    success_url ="/"

    def get_form_kwargs(self):
        kwargs = super(PlaceBetView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.instance.player = self.request.user
        form.instance.match = Match.objects.get(id=self.kwargs['pk'])
        new_points = getattr(CustomUser.objects.get(username=self.request.user.username), 'points')
        new_points -= form.instance.amount
        CustomUser.objects.filter(username=self.request.user.username).update(points=new_points)
        return super().form_valid(form)

    def get_initial(self):
        match = Match.objects.get(id=self.kwargs['pk'])
        return {
            'match':match,
        }

class MatchDetailView(generic.DetailView):
    model = Match

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MatchDetailView, self).get_context_data(**kwargs)
        # https://docs.djangoproject.com/en/dev/ref/templates/api/#variables-and-lookups

        bets_list = Bet.objects.filter(match__id=self.kwargs['pk']).values_list('player__username', 'choice__name', 'amount')
        context['bets_list'] = list(bets_list)
        is_Done = getattr(context['match'],'start_time')<timezone.now()
        context['is_Done'] = is_Done
        total_pool = Bet.objects.filter(match=context['match']).aggregate(Sum('amount'))['amount__sum'] or 0
        total_pool += getattr(context['match'], 'betpool_points')
        context['total_pool'] = total_pool
        odds = []
        # how to calculate odds?
        # basically, what is expected return if you bet 1?
        # for each team, if they won, how much would you get back if you bet 1?
        bets_models = Bet.objects.filter(match=context['match']) # all bets for this match
        sum_of_bets = bets_models.aggregate(Sum('amount'))['amount__sum'] or 0
        sum_of_bets += 1 # sum of all bets
        sum_of_bets += context['match'].betpool_points
        for team in list(Match.objects.filter(id=getattr(context['match'],'id')).values_list('teams__id', flat=True)):

            sum_of_winning_bets = bets_models.filter(choice=team).aggregate(Sum('amount'))['amount__sum'] or 0
            sum_of_winning_bets += 1
            ratio = 1/sum_of_winning_bets
            odds.append(round(ratio*sum_of_bets,5)) 
        context['odds'] = odds
        return context

class BetsListView(LoginRequiredMixin, generic.ListView):
    model = Bet
    def get_queryset(self):
        return Bet.objects.filter(player=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(BetsListView, self).get_context_data(**kwargs)
        bet_list = context['bet_list']
        status = []
        for bet in bet_list:
            match = getattr(bet, 'match')
            winner = getattr(match, 'winner')
            if winner is not None:
                # if they picked right
                if winner == getattr(bet,'choice'):
                    bets_models = Bet.objects.filter(match=match)
                    sum_of_bets = bets_models.aggregate(Sum('amount'))['amount__sum'] # sum of all bets
                    sum_of_bets += match.betpool_points
                    sum_of_winning_bets = bets_models.filter(choice=match.winner).aggregate(Sum('amount'))['amount__sum'] # sum of winning bets
                    person_pool = getattr(bet, 'amount')
                    person_ratio = person_pool/sum_of_winning_bets
                    person_payout = round(person_ratio*sum_of_bets) # payout = ratio * total sum
                    # now, update the db record for the person
                    status.append(person_payout)
                else:
                    status.append(0)
            else:
                status.append('PENDING')
        bet_list = zip(bet_list, status)
        context['bet_list'] = bet_list
        context['net_points'] = getattr(self.request.user, 'points')
        return context

class CustomUserListView(generic.ListView):
    model = CustomUser
    queryset = CustomUser.objects.exclude(username='admin')

def information(request):
    context = {}
    return render(request, 'information.html', context=context)

class PasswordChangeView(LoginRequiredMixin, FormView):
    model = CustomUser
    form_class = PasswordChangeForm
    template_name = 'password_change.html'

    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        if self.request.method == 'POST':
            kwargs['data'] = self.request.POST
        return kwargs

    def form_valid(self, form):
        self.success_url: 'index.html'
        form.save()
        update_session_auth_hash(self.request, form.user)        
        return super(PasswordChangeView, self).form_valid(form)
