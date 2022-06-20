from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/bet', views.PlaceBetView.as_view(), name='place-bet'),
    path('<int:pk>', views.MatchDetailView.as_view(), name='match-detail'),
    path('mybets', views.BetsListView.as_view(), name='my-bets'),
    path('leaderboard', views.CustomUserListView.as_view(), name='leaderboard'),
    path('info', views.information, name='information'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)