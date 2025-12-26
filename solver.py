import math
from collections import Counter
from tqdm import tqdm

class WordleSolver:
    def __init__(self, word_file, max_guesses=6):
        # Config
        self.max_guesses = max_guesses
        self.first_guess = "SALET"
        
        # State tracking
        self.guess_count = 0
        self.is_solved = False
        self.possible_words = self._load_words(word_file)
        self. total_initial_words = len(self.possible_words)
    
    def _load_words(self, filename):
        with open(filename, "r") as f:
            return [line.strip().upper() for line in f.readlines()]
        
    @staticmethod
        
    def get_feedback(guess, secret):
        result = [0] * 5
        secret_list = list(secret)
        guess_list = list(guess)
        
        # Pass 1, find greens
        for i in range(5):
            if guess_list[i] == secret_list[i]:
                result[i] = 2
                secret_list[i] = None
                guess_list[i] = None
        
        # Pass 2, find yellows
        for i in range (5):
            if guess_list[i] is not None and guess_list[i] in secret_list:
                result[i] = 1
                secret_list.remove(guess_list[i])
        
        return "".join(map(str, result))

    def filter_words(self, guess, pattern):
        self.possible_words = [
            w for w in self.possible_words
            if self.get_feedback(guess, w) == pattern
        ]
        if pattern == "22222":
            self.is_solved = True

    def calculate_entropy(self, guess):
        """Calculates how many bits of information a guess provides"""
        # Get pattern for every possible word 
        patterns = [self.get_feedback(guess, word) for word in self.possible_words]
        
        # Count how many words fall into each pattern
        counts = Counter(patterns).values()
        entropy = 0
        for count in counts:
            # Calculate the probabulty of this pattern occuring
            p = count / len(self.possible_words)
            # Shannon Entropy formula
            entropy -= p * math.log2(p)
        
        return entropy
    
    def get_best_guess(self):
        if self.guess_count ==0 and len(self.possible_words) == self.total_initial_words:
            return self.first_guess, 3.42
        
        best_word = ""
        max_entropy = -1
        for w in tqdm(self.possible_words, desc="Calculating Entropy", leave =False):
            score = self.calculate_entropy(w)
            if score > max_entropy:
                max_entropy = score
                best_word = w
        return best_word, max_entropy
    
if __name__ == "__main__":
    print("1. Wordle")
    print("2. Dordle")
    
    while True:
        mode = input("Select mode (1 or 2): ").strip()
        if mode in ['1', '2']:
            break
        print("Invalid Selection")
        
    bots = []
    if mode == '1':
        max_guesses = 6
        bots.append(WordleSolver("words.txt", max_guesses=6))
        print("Starting Wordle Solver: \n")
    if mode == '2':
        max_guesses = 7
        bots.append(WordleSolver("words.txt", max_guesses=7))
        bots.append(WordleSolver("words.txt", max_guesses=7))
        print("Starting Dordle Solver: \n")
        
    current_guess_num = 0
    
    while any(not b.is_solved for b in bots) and current_guess_num < max_guesses:
        current_guess_num += 1
        print(f"\n{'='*30}")
        print(f"\n--- Guess {current_guess_num}/{max_guesses} ---")
        
        for i, b in enumerate(bots):
            status = "SOLVED" if b.is_solved else f"{len(b.possible_words)} words left"
            name = "Wordle" if mode == '1' else f"Board {i+1}"
            print(f"{name}: {status}")
            
        print(f"\n{'='*30}")
        
        if current_guess_num == 1:
            best_word = "SALET"
        else:
            all_candidates = set()
            for b in bots:
                if not b.is_solved:
                    all_candidates.update(b.possible_words)
                    
            best_word = ""
            max_joint_entropy = -1
            
            # Progress bar for the calculation
            for w in tqdm(list(all_candidates), desc="Finding Best Guess", leave=False):
                joint_entropy = sum(b.calculate_entropy(w) for b in bots if not b.is_solved)
                if joint_entropy > max_joint_entropy:
                    max_joint_entropy = joint_entropy
                    best_word = w
                    
            
        print(f"RECOMMENDED GUESS: {best_word}")
        
        for i, b in enumerate(bots):
            if b.is_solved:
                continue
        
            prompt = "Enter pattern: " if mode == '1' else f"Enter pattern for Board {i+1}: "
            while True:
                pattern = input(prompt).strip()
                if len(pattern) == 5 and all(c in "012" for c in pattern):
                    b.filter_words(best_word, pattern)
                    break
                print("Invalid Input")
            
    print("\n" + "#"*30)
    for i, b in enumerate(bots):
        name = "Wordle" if mode == '1' else f"Board {i+1}"
        if b.is_solved:
            print(f"{name}: SUCCESS! (Word: {b.possible_words[0]})")
        else:
            print(f"{name}: FAILED. Possible words: {b.possible_words[:3]}")
    print("#"*30)