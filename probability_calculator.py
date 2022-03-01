from blackjack import Card, Deck, Player

#Will calculate probability of busting and of dealer's scores based on cards on table and remaining in deck
def calculate_probability(current_deck, current_hand_value):
    score_probabilities = {}
    for i in range(current_hand_value, 22):
        score_probabilities[i] = 0.0
    score_probabilities["Bust"] = 0.0
    print(score_probabilities)
    
    for single_card in current_deck.active_cards:
        new_value = current_hand_value + single_card.value
        if new_value > 21:
            score_probabilities["Bust"] += 1 / len(current_deck.active_cards)
        else:
            score_probabilities[new_value] += 1 / len(current_deck.active_cards)

    print(score_probabilities)

test_deck = Deck()

print(calculate_probability(test_deck, 10))
