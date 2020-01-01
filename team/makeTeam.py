from trueskill import Rating, quality, BETA, global_env, setup
import itertools
import math
import random

def win_probability(team1, team2):
    delta_mu = sum(r.mu for r in team1) - sum(r.mu for r in team2)
    sum_sigma = sum(r.sigma ** 2 for r in itertools.chain(team1, team2))
    size = len(team1) + len(team2)
    denom = math.sqrt(size * (BETA * BETA) + sum_sigma)
    ts = global_env()
    return ts.cdf(delta_mu / denom)

class MakeTeam:
  def __init__(self):
    self.player_name = []
    self.player_rate = []
    self.player_d = {} 

    self.c_team1 = []
    self.c_team2 = []

    self.possible_team1 = []
    self.possible_team2 = []
    self.possible_team1_win_rate = []

    self.random_team_number = 0

    self.t1_player = []
    self.t2_player = []
    self.t1_win_rate = ""

    self.t1_total_rate = 0
    self.t2_total_rate = 0

  def make_player_dict(self):
    self.player_d = dict(zip(self.player_name, self.player_rate))
  
  def make_combinations_of_team(self):
    """
    8人を4:4のチームに分ける場合の全組み合わせ作成
    """
    self.c_team1 = list(itertools.combinations(self.player_name, 4))
    self.c_team2 = []

    for v in itertools.combinations(self.player_name, 4):
      team2 = set(self.player_name) ^ set(v) 
      self.c_team2.append(team2)

  def extract_team_from_combinations_of_team(self):
    """
    4:4チームの全組み合わせのうち、team1の勝率が3-7割のものを抽出
    """
    for t1, t2 in zip(self.c_team1, self.c_team2):
      t1_rate=[]
      t2_rate=[]
      for name1, name2 in zip(t1, t2):
        t1_rate.append(Rating(self.player_d[name1]))
        t2_rate.append(Rating(self.player_d[name2]))

        win_rate = float(win_probability(t1_rate, t2_rate))
        draw_rate = float(quality([(t1_rate), (t2_rate)]))

        if (win_rate >= 0.3) & (win_rate <= 0.7):
          self.possible_team1.append(list(t1))
          self.possible_team2.append(list(t2))
          self.possible_team1_win_rate.append(win_rate)

  def choose_a_random_team(self):
    """
    team1の勝率が3-7割である4:4の組み合わせのうち、ランダムで1つの組み合わせを選択
    """
    num_of_possible_team = len(self.possible_team1)
    self.random_team_number = math.floor(random.uniform(0, num_of_possible_team))
  
  def extract_player_name(self):
    """
    ランダムで選択した4:4チームの1つの組み合わせから、team1,team2所属のプレイヤー名とteam1の勝率を抽出
    """
    for t1, t2 in zip(self.possible_team1[self.random_team_number], self.possible_team2[self.random_team_number]):
      self.t1_player.append(t1)
      self.t2_player.append(t2)
    self.t1_win_rate = "{:.1%}".format(self.possible_team1_win_rate[self.random_team_number])

  def calculate_total_rate(self):
    """
    ランダムで選択した4:4チームの1つの組み合わせから、team1,team2の合計レートを抽出
    """
    for t1, t2 in zip(self.t1_player, self.t2_player):
      self.t1_total_rate += self.player_d[t1]
      self.t2_total_rate += self.player_d[t2]