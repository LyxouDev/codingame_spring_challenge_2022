"""
    Version : 1.0.0
    Ligue : Wood 1
    Tactique :
        Idem Wood 2.
"""

# To debug: print("Debug messages...", file=sys.stderr, flush=True)

############## IMPORTATION ##############

import sys, math
import random

#########################################

class Const:
    MONSTER = 0
    MY_HERO = 1
    OPP_HERO = 2

    ATTACKING = 1

    ATTACK_MY_BASE = 1
    ATTACK_OPP_BASE = 2

class IO:
    # Initial Turn
    def __init__(self):
        base_x, base_y = [int(i) for i in input().split()]
        
        self.heroes_per_player = int(input())

        self.my_base = Coordonnee(base_x, base_y)
        self.opp_base = Coordonnee(17630-base_x, 9000-base_y)

    def read_round(self):
        health = [0, 0]
        mana = [0, 0]

        for i in range(2):
            health[i], mana[i] = [int(j) for j in input().split()]

        game = Game(health, mana)

        p1 = game.Players[0]
        p2 = game.Players[1]

        entity_count = int(input())

        for i in range(entity_count):
            _id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [int(j) for j in input().split()]

            if _type == Const.MONSTER:
                game.monsters.append(Entite(_id, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for))
            elif _type == Const.MY_HERO:
                p1.heroes.append(Entite(_id, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for))
            elif _type == Const.OPP_HERO:
                p2.heroes.append(Entite(_id, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for))

        return game

class ReactAgent:
    def __init__(self, io, game):
        self.io = io
        self.game = game
        self.p1 = game.Players[0]
        self.p2 = game.Players[1]

    def think(self, idx):
        best_action = "WAIT WAIT"

        dist = 17630
        
        for i in range(len(game.monsters)):
            if game.get_base_distance(io.my_base, i)<dist and game.monsters[i].target==Const.ATTACK_MY_BASE:
                dist = game.get_base_distance(io.my_base, i)
                best_action = "MOVE " + str(game.monsters[i].position) + " ATTACK"
        
        return best_action

class Player:
    Opponent = None

    def __init__(self, health, mana):
        self.health = health
        self.mana = mana
        self.heroes = list()

class Entite:
    def __init__(self, id, x, y, shield, control, health, vx, vy, attack, target):
        self.id = id
        self.position = Coordonnee(x, y)
        self.shield = shield
        self.control = control
        self.health = health
        self.direction = Coordonnee(vx, vy)
        self.attack = attack
        self.target = target

class Game:
    Players = [None, None]

    def __init__(self, health, mana):
        self.Players[0] = Player(health[0], mana[0])
        self.Players[1] = Player(health[1], mana[1])

        self.Players[0].Opponent = self.Players[1]
        self.Players[1].Opponent = self.Players[0]

        self.monsters = list()

    def get_distance(self, hero_idx,target_idx):
        return math.sqrt((self.Players[0].heroes[hero_idx].position.x-self.monsters[target_idx].position.x)**2 + (self.Players[0].heroes[hero_idx].position.y-self.monsters[target_idx].position.y)**2)

    def get_base_distance(self, base,target_idx):
        return math.sqrt((base.x-self.monsters[target_idx].position.x)**2 + (base.y-self.monsters[target_idx].position.y)**2)
    

class Coordonnee:    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.x) + " " + str(self.y)


#############################
##         SCRIPT          ##
#############################

# Initialisation
io = IO()

# Boucle de jeu
while True:
    game = io.read_round()
    result = ReactAgent(io, game)   
    for i in range(io.heroes_per_player):
        print(result.think(i))
