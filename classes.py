"""
 Python Scrabble
"""

def documentation():
    """
    documentation()
    ----------------
    Πληροφορίες τεκμηρίωσης:
    1. Κλάσεις: Game, SakClass, Player, Human, Computer
    2. Κληρονομικότητα: Human και Computer κληρονομούν από Player
    3. Επέκταση play(): Στις Human και Computer
    4. Δεν χρησιμοποιήθηκε υπερφόρτωση τελεστών ή decorators
    5. Δομή λέξεων: set για ταχύτητα αναζήτησης O(1)
    6. Αλγόριθμος Computer: Επιλογή Min, Max ή Smart
    7. Πρότυπο Mediator: Η Game ελέγχει την επικοινωνία Human-Computer
    """

import random
from itertools import permutations

# Κλάση που διαχειρίζεται τα γράμματα (SakClass)

class SakClass:
    def __init__(self):
        self.letters = {
            'Α': 12, 'Β': 1, 'Γ': 2, 'Δ': 2, 'Ε': 8, 'Ζ': 1, 'Η': 7, 'Θ': 1,
            'Ι': 8, 'Κ': 4, 'Λ': 3, 'Μ': 3, 'Ν': 6, 'Ξ': 1, 'Ο': 9, 'Π': 4,
            'Ρ': 5, 'Σ': 7, 'Τ': 8, 'Υ': 4, 'Φ': 1, 'Χ': 1, 'Ψ': 1, 'Ω': 3
        }

    def get_letters(self, num):
        result = []
        available_letters = [ltr for ltr, count in self.letters.items() for _ in range(count)]
        random.shuffle(available_letters)
        for _ in range(min(num, len(available_letters))):
            letter = available_letters.pop()
            result.append(letter)
            self.letters[letter] -= 1
            if self.letters[letter] == 0:
                del self.letters[letter]
        return result

# Βοηθητική συνάρτηση για βαθμολογία λέξης (απλό μέτρο)

def calculate_word_points(word):
    return len(word)

# Βασική κλάση παίκτη (Player)
class Player:
    def __init__(self, name):
        self.name = name
        self.letters = []
        self.score = 0

    def refill_letters(self, sak, num=7):
        while len(self.letters) < num and sak.letters:
            self.letters.append(sak.get_letters(1)[0])

# ----------------------------------------------------------
# Κλάση Human
# ----------------------------------------------------------
class Human(Player):
    def play_turn(self, greek_words, sak):
        print("**************************************************")
        print(f"*** Παίκτης: {self.name}   *** Σκόρ: {self.score}")
        print(f">>> Γράμματα: {self.letters}")

        word = input("\nΛέξη (ή 'P' για αλλαγή, 'Q' για παραίτηση): ").strip().upper()

        if word == "Q":
            return "quit"
        elif word == "P":
            for ltr in self.letters:
                sak.letters[ltr] = sak.letters.get(ltr, 0) + 1
            self.letters = sak.get_letters(7)
            print("Αλλάχθηκαν τα γράμματα. Χάνετε τη σειρά σας.")
            return "pass"

        if word in greek_words and all(word.count(l) <= self.letters.count(l) for l in word):
            points = calculate_word_points(word)
            self.score += points
            print(f"Πόντοι λέξης: {points}")
            for l in word:
                self.letters.remove(l)
            self.refill_letters(sak)
            print("**************************************************")
            return "ok"
        else:
            print("Η λέξη δεν είναι αποδεκτή ή δεν έχεις τα απαραίτητα γράμματα.")
            print("**************************************************")
            return "retry"

# ----------------------------------------------------------
# Κλάση Computer
# ----------------------------------------------------------
class Computer(Player):
    def __init__(self, name, strategy='Min'):
        super().__init__(name)
        self.strategy = strategy

    def play_turn(self, greek_words, sak):
        print(f"*** Υπολογιστής παίζει με στρατηγική {self.strategy} ***")

        candidates = [w for w in greek_words if all(w.count(l) <= self.letters.count(l) for l in w)]
        if not candidates:
            sak.letters.update({ltr: sak.letters.get(ltr, 0) + self.letters.count(ltr) for ltr in set(self.letters)})
            self.letters = sak.get_letters(7)
            print("Υπολογιστής άλλαξε τα γράμματα.")
            return "pass"

        if self.strategy == "Min":
            chosen_word = min(candidates, key=len)
        elif self.strategy == "Max":
            chosen_word = max(candidates, key=len)
        else:  # Smart
            chosen_word = candidates[0]

        points = calculate_word_points(chosen_word)
        self.score += points
        print(f"Υπολογιστής παίζει λέξη: {chosen_word} ({points} πόντοι)")

        for l in chosen_word:
            self.letters.remove(l)
        self.refill_letters(sak)

        return "ok"

# ----------------------------------------------------------
# Κλάση Game
# ----------------------------------------------------------
class Game:
    def __init__(self):
        self.sak = SakClass()
        # Ζήτηση ονόματος παίκτη
        human_name = input("Δώσε το όνομά σου: ").strip() or "Παίκτης"
        self.human = Human(human_name)
        self.computer = Computer("Υπολογιστής")
        self.load_words()

    def load_words(self):
        self.words = set()
        try:
            with open("greek7.txt", "r", encoding="utf-8") as f:
                for line in f:
                    self.words.add(line.strip().upper())
            print(f"Λεξικό φορτώθηκε με {len(self.words)} λέξεις.")
        except FileNotFoundError:
            print("Το αρχείο greek7.txt δεν βρέθηκε. Παιχνίδι χωρίς έλεγχο λέξεων.")
            self.words = set()

    def start(self):
        self.human.refill_letters(self.sak)
        self.computer.refill_letters(self.sak)

        turn = 0
        while True:
            player = self.human if turn % 2 == 0 else self.computer

            if isinstance(player, Human):
                while True:
                    result = player.play_turn(self.words, self.sak)
                    if result in ("ok", "pass", "quit"):
                        break
            else:
                result = player.play_turn(self.words, self.sak)

            if result == "quit":
                print(f"{player.name} παραιτήθηκε! Τέλος παιχνιδιού.")
                break

            if not self.sak.letters and not player.letters:
                print("\nΤέλος παιχνιδιού! Τελείωσαν όλα τα γράμματα.")
                break

            turn += 1

        print("\n***** ΤΕΛΙΚΟ ΣΚΟΡ *****")
        print(f"{self.human.name}: {self.human.score}")
        print(f"{self.computer.name}: {self.computer.score}")
        if self.human.score > self.computer.score:
            print(">>> Νίκησες!")
        elif self.human.score < self.computer.score:
            print(">>> Έχασε!")
        else:
            print(">>> Ισοπαλία!")
