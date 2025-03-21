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
        print(f"Length of words left list: {len(words_left)}")
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

        print(f"Filtered words from {len(words_left)} to {len(new_words_left_list)} based on feedback {feedback}")
        return new_words_left_list
    
    
    def does_word_match(self, word, guess, feedback):
        word_freq = {char: word.count(char) for char in set(word)}
        for i in range(len(feedback)):
            if feedback[i] == "✓":
                if word[i] != guess[i]:
                    return False
                word_freq[guess[i]] -= 1
            elif feedback[i] == "~":
                if guess[i] not in word or word[i] == guess[i] or word_freq[guess[i]] == 0:
                    return False
                word_freq[guess[i]] -= 1
            elif feedback[i] == "X":
                if guess[i] in word and word_freq[guess[i]] > 0:
                    return False

        return True


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
        feedback = []
        for i in range(len(potential_guess)):
            if potential_guess[i] == word[i]:
                feedback.append("✓")
            elif potential_guess[i] in word:
                feedback.append("~")
            else:
                feedback.append("X")
        return "".join(feedback)