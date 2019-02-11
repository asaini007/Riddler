# Akshay Saini
# asaini007@gmail.com
# 02/10/2019
from itertools import combinations
import time

NUM_CARDS = 9
GOAL = 15


# P1 is max, P2 is min
class Player:
    P1 = 1
    P2 = 2


# A value of 1 means that P1 wins. A value of -1 means P2 wins. A value of 0 means it's a draw.
class Node:
    # create root node if parent is None, else creates a child of the given parent node
    def __init__(self, parent, move):
        if parent is None:
            self.turn = Player.P1
            self.prev_move = None
            self.parent = None
            self.children = []
            self.p1_cards = []
            self.p2_cards = []
            self.remaining_cards = range(1, NUM_CARDS + 1)
            self.value = None
        else:
            self.turn = Player.P1 if parent.turn == Player.P2 else Player.P2
            self.prev_move = move
            self.parent = parent
            self.children = []

            # these could easily be calculated by checking the path to root
            # but we store them instead for convenience
            self.p1_cards = parent.p1_cards[:]  # copy value
            self.p2_cards = parent.p2_cards[:]  # copy value
            if parent.turn == Player.P1:
                self.p1_cards.append(move)
            else:
                self.p2_cards.append(move)
            self.remaining_cards = parent.remaining_cards[:]  # copy value
            self.remaining_cards.remove(move)

            # try to compute value for completed game
            self.value = self.value_for_finished_game()

    # return value of game if game is finished
    # return None if the game is not finished
    def value_for_finished_game(self):
        prev_move_by_p1 = self.parent.turn == Player.P1
        cards_to_check = self.p1_cards if prev_move_by_p1 else self.p2_cards
        sums = [sum(triplet) for triplet in combinations(cards_to_check, 3)]
        if GOAL in sums:
            return 1 if prev_move_by_p1 else -1
        else:
            return 0 if len(self.remaining_cards) == 0 else None

    # recursively create children to construct a tree of all possible games
    def build_tree(self):
        # if this node has a value, then it is a leaf (a finished game)
        # build_tree must be called before minimax_value to guarantee this
        if self.value is None:
            for card in self.remaining_cards:
                child = Node(parent=self, move=card)
                self.children.append(child)
                child.build_tree()

    # recursively calculates (and returns) the minimax value of this node
    def minimax_value(self):
        if self.value is None:
            child_values = [child.minimax_value() for child in self.children]
            self.value = max(child_values) if self.turn == Player.P1 else min(child_values)
        return self.value

    # return a node that represents the optimal play from this node
    def optimal_move(self):
        best = max if self.turn == Player.P1 else min
        child_values = [child.value for child in self.children]
        best_index = child_values.index(best(child_values))
        return self.children[best_index]

    # might be buggy
    def count_nodes(self):
        total_descendents = 0
        for child in self.children:
            total_descendents += child.count_nodes()
        return 1 + total_descendents


if __name__ == "__main__":
    start = time.time()
    root = Node(parent=None, move=None)
    root.build_tree()
    print "Value:", str(root.minimax_value())
    end = time.time()
    print "Time: ", str(end - start)

    node = root
    remaining_cards = node.remaining_cards
    p1_cards = node.p1_cards
    p2_cards = node.p2_cards
    turn = 1
    users_turn = True if input("Which Player would you like to be, 1 or 2? ") == 1 else False
    while len(node.children) > 0:
        print "\nTurn", turn
        print "Remaining cards: ", node.remaining_cards
        print "Player 1's cards:", node.p1_cards
        print "Player 2's cards:", node.p2_cards
        if users_turn:
            move = input("Which card would you like to pick? ")
            possible_moves = [child.prev_move for child in node.children]
            move_index = possible_moves.index(move)
            node = node.children[move_index]
            users_turn = False
        else:
            node = node.optimal_move()
            print "I choose", node.prev_move
            users_turn = True
        turn += 1
    print "\nGame over"
    print "Remaining cards: ", node.remaining_cards
    print "Player 1's cards:", node.p1_cards
    print "Player 2's cards:", node.p2_cards
    if node.value == 0:
        print "It's a draw."
    elif users_turn:
        print "I win."
    else:
        # should be unreachable
        print "You win."
