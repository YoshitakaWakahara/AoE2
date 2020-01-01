from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Player 
from . import makeTeam 

def index(request):
  return HttpResponse("Test")

def player(request):
  context = {
    "players": Player.objects.all(),
  }
  return render(request, "team/player.html", context)

#チーム分け
def make_team(request):
  if request.method == "POST":
    player1 = Player.objects.get(pk=int(request.POST["player1"])) 
    player2 = Player.objects.get(pk=int(request.POST["player2"])) 
    player3 = Player.objects.get(pk=int(request.POST["player3"])) 
    player4 = Player.objects.get(pk=int(request.POST["player4"])) 
    player5 = Player.objects.get(pk=int(request.POST["player5"])) 
    player6 = Player.objects.get(pk=int(request.POST["player6"])) 
    player7 = Player.objects.get(pk=int(request.POST["player7"])) 
    player8 = Player.objects.get(pk=int(request.POST["player8"])) 

  player_name = [player1.name, player2.name, player3.name, player4.name, player5.name, player6.name, player7.name, player8.name]
  player_rate = [player1.rate, player2.rate, player3.rate, player4.rate, player5.rate, player6.rate, player7.rate, player8.rate]
  four_vs_four_team = makeTeam.MakeTeam()
  four_vs_four_team.player_name = player_name
  four_vs_four_team.player_rate = player_rate
  four_vs_four_team.make_player_dict()
  four_vs_four_team.make_combinations_of_team()
  four_vs_four_team.extract_team_from_combinations_of_team()
  four_vs_four_team.choose_a_random_team()
  four_vs_four_team.extract_player_name()
  four_vs_four_team.calculate_total_rate()

  context = {
    "t1_player1": four_vs_four_team.t1_player[0],
    "t1_player2": four_vs_four_team.t1_player[1],
    "t1_player3": four_vs_four_team.t1_player[2],
    "t1_player4": four_vs_four_team.t1_player[3],
    "t2_player1": four_vs_four_team.t2_player[0],
    "t2_player2": four_vs_four_team.t2_player[1],
    "t2_player3": four_vs_four_team.t2_player[2],
    "t2_player4": four_vs_four_team.t2_player[3],
    "t1_win_rate": four_vs_four_team.t1_win_rate,
    "t1_total_rate": four_vs_four_team.t1_total_rate,
    "t2_total_rate": four_vs_four_team.t2_total_rate,
  }
  
  return render(request, "team/team.html", context)

#チーム勝利後のレート確定処理
def which_team_won(request):

  if request.method == "POST":
    won_team = request.POST.getlist("won_team")
  if won_team == 1:

    context = {
      "won_team": won_team 
    }
  return render(request, "team/result.html", context)

    #TODO
    #total_rateとwin_rateの修正 done
    #各処理関数化 done
    #クラス作成、モジュール化 done
    #Team1 or Team2勝利のSubmitボタンとレート処理作成
    #post data処理時の例外処理作成
    #勝率3-7割のチームが見つからない場合の例外処理作成
    #selectボタンで同一のプレイヤーを選択させないようにする処理作成
    #汎用処理のView化
    #UnitTest作成
    #勝率ではなく合計レートの間がいくつまで、とかにしてみる？
    #その場合acceptable rate differenceの処理が必要