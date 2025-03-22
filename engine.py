class Engine:
    def __init__(self, word_list):
        self.possible_words = word_list

    def find_best_guess(self, attempts, feedbacks):
        """Greedy algorithm. Finds the best guess based on feedback from earlier guesses and the highest expected entropy of remaining possible words."""
        if len(attempts) == 0: # If it is the first guess, it finds the best first guess.
            return "raise"
        words_left = self.filter_words(attempts, feedbacks) # Provides a new list of possible words left based on feedback from previous guesses.
        self.possible_words = words_left # Replaces the original list with the new list.
        
        # Finds the word with the highest entropy among the remaining possible words based on the score_guess method.
        words_scores = lambda word: self.score_guess(word, words_left) 
        #print(f"Length of words left list: {len(words_left)}")
        best_guess = max(words_left, key=words_scores)
        return best_guess
    
    def find_first_best_guess(self):
        """Finds the best first guess. Similar to the find_best_guess method."""
        best_guess = max(self.game.word_list, key=lambda word: self.score_guess(word, self.game.word_list)) # Finds the word with the highest entropy among all the words in the dictionary based on the score_guess method.
        return best_guess
    
    def filter_words(self, attempts, feedbacks):
        words_left = self.possible_words
        guess, feedback = attempts[-1], feedbacks[-1]  # Ensure feedback is not nested
        new_words_left_list = []

        for word in words_left:
            if self.does_word_match(word, guess, feedback):
                new_words_left_list.append(word)

        #print(f"Filtered words from {len(words_left)} to {len(new_words_left_list)} based on feedback {feedback}")
        return new_words_left_list
    
    def does_word_match(self, word, guess, feedback):
        """Checks if a word would produce the same feedback when guessed."""
        simulated = self.simulate_feedback(word, guess)
        return simulated == ''.join(feedback)

    def score_guess(self, potential_guess, words_left):
        """Calculates the entropy of a word based on the remaining possible words."""
        feedback_counts = {}
        for word in words_left:
            feedback = self.simulate_feedback(word, potential_guess)
            # Adds the feedback count to the dictionary
            if feedback in feedback_counts:
                feedback_counts[feedback] += 1
            else:
                feedback_counts[feedback] = 1
        # Calculates the entropy
        number_of_words_left = len(words_left)
        entropy = 0
        for count in feedback_counts.values():
            probability = count / number_of_words_left
            entropy -= count * probability
        return entropy
    
    def simulate_feedback(self, word, potential_guess):
        """Simulates feedback like Wordle, with correct handling of duplicate letters."""
        feedback = ['X'] * len(potential_guess)
        secret_counts = {}

        # First pass: mark correct letters
        for i in range(len(potential_guess)):
            if potential_guess[i] == word[i]:
                feedback[i] = '✓'
            else:
                if word[i] in secret_counts:
                    secret_counts[word[i]] += 1
                else:
                    secret_counts[word[i]] = 1

        # Second pass: mark misplaced letters
        for i in range(len(potential_guess)):
            if feedback[i] == 'X' and potential_guess[i] in secret_counts and secret_counts[potential_guess[i]] > 0:
                feedback[i] = '~'
                secret_counts[potential_guess[i]] -= 1

        return ''.join(feedback)