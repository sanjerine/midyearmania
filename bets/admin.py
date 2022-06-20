from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Match, Bet, Team

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["username", "points", "team"]
    fieldsets = (
        (None, {
            'fields': ('username', 'points', 'team')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    pass

@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = ["match", "player", "amount", "choice"]

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass