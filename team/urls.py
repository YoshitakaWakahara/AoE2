from django.urls import path

from . import views

app_name='team'
urlpatterns = [
  path('', views.index, name='index'),
  path('player', views.player, name='player'),
  path('make_team', views.make_team, name='make_team'),
  path('which_team_won', views.which_team_won, name='which_team_won')
]