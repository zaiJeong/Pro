import random

# Function to roll the dice with optional rerolls
def roll_dice(dices, keep_indices):
    for i in range(len(dices)):
        if i not in keep_indices:  # Skip rolling for kept dice
            dices[i] = random.randint(1, 6)

# Function to display the score sheet
def display_score_sheet(scores):
    current_score = sum(score for score in scores.values() if score != -1)
    print("+------------------------+-------+")
    print("| Category               | Score |")
    print("+------------------------+-------+")
    for category, score in scores.items():
        score_display = score if score != -1 else "-"
        print(f"| {category:<22} | {score_display:<5} |")
    print("+------------------------+-------+")
    print("Current Score : ", current_score)


# Function to calculate score for a given category
def calculate_score(dices, category):
    counts = {i: dices.count(i) for i in range(1, 7)}

    if category == "Aces":
        return counts[1] * 1
    elif category == "Twos":
        return counts[2] * 2
    elif category == "Threes":
        return counts[3] * 3
    elif category == "Fours":
        return counts[4] * 4
    elif category == "Fives":
        return counts[5] * 5
    elif category == "Sixes":
        return counts[6] * 6
    elif category == "Three of a Kind":
        if any(count >= 3 for count in counts.values()):
            return sum(dices)
        return 0
    elif category == "Four of a Kind":
        if any(count >= 4 for count in counts.values()):
            return sum(dices)
        return 0
    elif category == "Full House":
        if 3 in counts.values() and 2 in counts.values():
            return 25
        return 0
    elif category == "Small Straight":
        if {1, 2, 3, 4}.issubset(dices) or {2, 3, 4, 5}.issubset(dices) or {3, 4, 5, 6}.issubset(dices):
            return 30
        return 0
    elif category == "Large Straight":
        if set([1, 2, 3, 4, 5]) == set(dices) or set([2, 3, 4, 5, 6]) == set(dices):
            return 40
        return 0
    elif category == "Yahtzee":
        if len(set(dices)) == 1:
            return 50
        return 0
    elif category == "Chance":
        return sum(dices)
    return 0

# Function to display possible scores in table format
def display_possible_scores(dices, scores):
    print("\n+------------------------+-------+")
    print("| Category               | Score |")
    print("+------------------------+-------+")
    for category, score in scores.items():
        if score == -1:
            possible_score = calculate_score(dices, category)
            print(f"| {category:<22} | {possible_score:<5} |")
        else:
            print(f"| {category:<22} | -     |")
    print("+------------------------+-------+")

# Main game logic
def yahtzee_game():
    dices = [random.randint(1, 6) for _ in range(5)]
    reroll_limit = 2
    reroll_count = 0
    scores = {
        "Aces": -1, "Twos": -1, "Threes": -1, "Fours": -1, "Fives": -1, "Sixes": -1, "Chance": -1,
        "Three of a Kind": -1, "Four of a Kind": -1, "Full House": -1, "Small Straight": -1,
        "Large Straight": -1, "Yahtzee": -1
    }

    current_score = 0
    round_number = 1

    while round_number <= 13:
        print(f"\nRound {round_number}")
        print("Choose the option.")
        print("1. Roll the dice")
        print("2. Check the score sheet")
        print("3. Quit the game")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "3":
            print("Game over...")
            return
        elif choice == "2":
            display_score_sheet(scores)
            continue
        elif choice == "1":
            roll_dice(dices, [])
            print(f"Result of dice\n{dices}")

            # Allow rerolling
            while reroll_count < reroll_limit:
                reroll = input("Reroll the dice? [Y/N] : ").lower()
                if reroll not in ['y', 'n']:
                    print("Invalid input! Please enter 'Y' or 'N'.")
                    continue
                if reroll == "n":
                    break

                # Check if reroll limit is reached
                if reroll_count >= reroll_limit:
                    print("You have used all your rerolls.")
                    break

                # Updated instruction
                keep_input = input("Choose all of the dice that you want to keep. Separate numbers with spaces.\nIf you want to change all of the dice, then input '0'\n")
                try:
                    if keep_input.strip() == '0':      # No dice will be kept, all will be rerolled
                        keep_indices = []  
                    elif keep_input.strip():
                        keep_indices = list(map(int, keep_input.split()))
                        if any(index < 1 or index > 5 for index in keep_indices):
                            raise ValueError("Invalid dice index! Enter numbers between 1 and 5.")
                    else:
                        keep_indices = []
                except ValueError as e:
                    print(e)
                    continue

                keep_indices = [index - 1 for index in keep_indices]
                roll_dice(dices, keep_indices)
                print(f"Result of dice\n{dices}")
                reroll_count += 1
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            continue

        # Display possible scores in table format
        display_possible_scores(dices, scores)

        # Choose a category to score
        available_categories = [cat for cat, score in scores.items() if score == -1]
        category_choice = input(f"Choose a category to record the score: ")

        while category_choice not in available_categories:
            print("Invalid category. Please choose a valid category.")
            category_choice = input(f"Choose a category to record the score: ")

        selected_category = category_choice

        # Calculate and update the score
        score = calculate_score(dices, selected_category)
        scores[selected_category] = score
        current_score += score

        print(f"Scored {score} points in {selected_category}.")
        print(f"Current score: {current_score}")

        # Reset for the next round
        reroll_count = 0
        round_number += 1

    # Game over, display final score
    print("\nFinal Score Sheet:")
    display_score_sheet(scores)
    print(f"Final score: {current_score}")

# Start the game
yahtzee_game()