import random
from utils import RPS_CHOICES, RPS_OUTCOMES, ALPHA, GAMMA, EPSILON

class RPS:
    """
    Implements the Rock Paper Scissors game logic.
    Supports player moves and AI moves (naive, biased, Q-learning).
    """
    def __init__(self, qtable):
        self.history = []     # Stores history of (player_choice, ai_choice)
        self.state = 'start,start'  # Current state for Q-learning (last two player choices as string)
        self.score = [0, 0]   # [Player Score, AI Score]
        self.q = qtable       # Q-table for RL agent

    def reset(self):
        """Resets the game history and score for a new game."""
        self.history = []
        self.state = 'start,start'
        self.score = [0, 0]

    def play(self, player_choice, mode):
        """
        Processes a round of Rock Paper Scissors.
        Args:
            player_choice (str): The player's choice ('rock', 'paper', 'scissors').
            mode (str): The AI difficulty mode ('naive', 'biased', 'rl').
        Returns:
            tuple: (ai_choice, outcome) where outcome is 1 (AI wins), 0 (tie), -1 (player wins).
        """
        if player_choice not in RPS_CHOICES:
            return None, None  # Invalid player choice

        ai_choice = None
        if mode == 'naive':
            ai_choice = random.choice(RPS_CHOICES)  # Random AI
        elif mode == 'biased':
            # Naive Bayes prediction based on player's previous choice
            if len(self.history) < 1:  # No history, use original biased weights
                ai_choice = random.choices(RPS_CHOICES, [0.5, 0.25, 0.25])[0]
            else:
                # Initialize transition counts
                transitions = {c: {next_c: 0 for next_c in RPS_CHOICES} for c in RPS_CHOICES}
                for i in range(len(self.history) - 1):
                    prev_choice = self.history[i][0]
                    next_choice = self.history[i + 1][0]
                    transitions[prev_choice][next_choice] += 1

                # Get the last player choice
                last_choice = self.history[-1][0]

                # Calculate probabilities with Laplace smoothing
                probs = {}
                total_transitions = sum(transitions[last_choice].values()) + len(RPS_CHOICES)
                for next_choice in RPS_CHOICES:
                    count = transitions[last_choice][next_choice] + 1  # Laplace smoothing
                    probs[next_choice] = count / total_transitions

                # Predict the player's most likely next choice
                predicted_choice = max(probs, key=probs.get)

                # Choose AI move to beat the predicted choice
                if predicted_choice == 'rock':
                    ai_choice = 'paper'
                elif predicted_choice == 'paper':
                    ai_choice = 'scissors'
                else:  # predicted_choice == 'scissors'
                    ai_choice = 'rock'
        else:  # 'rl' mode (Q-learning agent)
            # Ensure the current state exists in the Q-table, initialize if not
            table = self.q.setdefault(self.state, {c: 0 for c in RPS_CHOICES})

            # Epsilon-greedy strategy for AI's choice
            if random.random() < EPSILON:
                ai_choice = random.choice(RPS_CHOICES)  # Explore
            else:
                # Exploit: choose the action with the highest Q-value
                max_q = -float('inf')
                best_ai_choices = []
                for choice_ai, q_value in table.items():
                    if q_value > max_q:
                        max_q = q_value
                        best_ai_choices = [choice_ai]
                    elif q_value == max_q:
                        best_ai_choices.append(choice_ai)
                ai_choice = random.choice(best_ai_choices) if best_ai_choices else random.choice(RPS_CHOICES)

            # Determine the outcome from the AI's perspective
            player_outcome_value = RPS_OUTCOMES[(player_choice, ai_choice)]
            ai_reward = -player_outcome_value

            # Compute the next state (last two player choices as string)
            if self.state == 'start,start':
                next_state = f"start,{player_choice}"
            else:
                next_state = f"{self.state.split(',')[1]},{player_choice}"

            # Ensure Q-values for the next state are initialized
            next_state_q_values = self.q.setdefault(next_state, {c: 0 for c in RPS_CHOICES})

            # Q-learning update
            table[ai_choice] += ALPHA * (ai_reward + GAMMA * max(next_state_q_values.values()) - table[ai_choice])

            # Update the current state
            self.state = next_state

        outcome = RPS_OUTCOMES[(player_choice, ai_choice)]  # Outcome from player's perspective
        self.history.append((player_choice, ai_choice))

        # Update scores based on outcome (player's perspective)
        if outcome == 1:  # Player wins
            self.score[0] += 1
        elif outcome == -1:  # AI wins
            self.score[1] += 1

        return ai_choice, outcome