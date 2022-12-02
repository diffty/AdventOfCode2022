import os
from enum import Enum, auto


class EMove(Enum):
    ROCK = auto() 
    PAPER = auto() 
    SCISSOR = auto() 

class ERoundOutcome(Enum):
    DRAW = auto() 
    WIN = auto() 
    LOSE = auto()


MOVE_WIN_TABLE = {
    EMove.ROCK: EMove.SCISSOR,
    EMove.SCISSOR: EMove.PAPER,
    EMove.PAPER: EMove.ROCK,
}

MOVE_LOSE_TABLE = dict(map(lambda it: (it[1], it[0]), MOVE_WIN_TABLE.items()))


def get_move_from_letter(move_letter):
    return {
        "A": EMove.ROCK,
        "X": EMove.ROCK,
        "B": EMove.PAPER,
        "Y": EMove.PAPER,
        "C": EMove.SCISSOR,
        "Z": EMove.SCISSOR,
    }.get(move_letter, None)

def get_round_winner(p1_move: EMove, p2_move: EMove):
    if p1_move == p2_move:
        return 0
    
    if MOVE_WIN_TABLE[p1_move] == p2_move:
        return 1
    else:
        return 2

def get_player_round_score(move: EMove, outcome: ERoundOutcome):
    shape_score = {
        EMove.ROCK: 1,
        EMove.PAPER: 2,
        EMove.SCISSOR: 3,
    }[move]

    outcome_score = {
        ERoundOutcome.DRAW: 3,
        ERoundOutcome.WIN: 6,
        ERoundOutcome.LOSE: 0,
    }[outcome]

    return shape_score + outcome_score
    

# Part 0
file_path = os.path.dirname(__file__) + "/input.txt"

fp = open(file_path)
data = fp.readlines()
fp.close()


# Part 1
opponent_score = player_score = 0

for round_data_raw in data:
    round_data_raw = round_data_raw.strip()
    round_data = round_data_raw.split(" ")

    if round_data:
        p1_move = get_move_from_letter(round_data[0])
        p2_move = get_move_from_letter(round_data[1])

        round_winner = get_round_winner(p1_move, p2_move)

        if round_winner == 0:
            p1_outcome = p2_outcome = ERoundOutcome.DRAW
        elif round_winner == 1:
            p1_outcome = ERoundOutcome.WIN
            p2_outcome = ERoundOutcome.LOSE
        else:
            p1_outcome = ERoundOutcome.LOSE
            p2_outcome = ERoundOutcome.WIN

        opponent_score += get_player_round_score(p1_move, p1_outcome)
        player_score += get_player_round_score(p2_move, p2_outcome)

print(f"[PART1] Your score according to the strategy guide: {player_score}")


# Part 02
def get_needed_outcome_from_letter(outcome_letter):
    return {
        "X": ERoundOutcome.LOSE,
        "Y": ERoundOutcome.DRAW,
        "Z": ERoundOutcome.WIN,
    }.get(outcome_letter, None)

player_score = 0

for round_data_raw in data:
    round_data_raw = round_data_raw.strip()
    round_data = round_data_raw.split(" ")

    if round_data:
        p1_move = get_move_from_letter(round_data[0])
        needed_outcome = get_needed_outcome_from_letter(round_data[1])
        
        if needed_outcome == ERoundOutcome.WIN:
            p2_move = MOVE_LOSE_TABLE[p1_move]
        elif needed_outcome == ERoundOutcome.LOSE:
            p2_move = MOVE_WIN_TABLE[p1_move]
        else:
            p2_move = p1_move

        player_score += get_player_round_score(p2_move, needed_outcome)

print(f"[PART2] Your score according to the strategy guide: {player_score}")
