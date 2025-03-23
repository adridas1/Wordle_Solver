from engine import Engine
import wordle

scores = []
filtered_out_count = 0

word_list = wordle.load_word_list("dictionary_wordle.txt")

for iter in range(1,501):

    if iter % 100 == 0:
        print(f"Iteration {iter}")

    game_engine = Engine(word_list)
    secret_word = wordle.pick_random_word(word_list)
    #print("Secret word:", secret_word)

    attempts = []
    feedbacks = []

    for i in range(1, 7):
        guess = game_engine.find_best_guess(attempts, feedbacks)
        #print("Guess:", guess)
        feedback = wordle.evaluate_guess(guess, secret_word)
        #print("Feedback:", feedback)
        if all(f == "✓" for f in feedback):
            scores.append(i)
            break
        feedbacks.append(feedback)
        attempts.append(guess)

average = sum(scores) / len(scores)
print("The average number of needed guesses was:", average)
#print("Secret word was filtered out", filtered_out_count, "times")