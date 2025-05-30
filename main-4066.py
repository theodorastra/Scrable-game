from classes import Game

def show_main_menu(game):
    while True:
        print("\n***** SCRABBLE *****")
        print("--------------------")
        print("1: Σκόρ")
        print("2: Ρυθμίσεις")
        print("3: Παιχνίδι")
        print("q: Έξοδος")
        print("--------------------")

        choice = input("Δώσε επιλογή: ").strip().lower()

        if choice == "1":
            show_score(game)
        elif choice == "2":
            settings(game)
        elif choice == "3":
            game.start()
        elif choice == "q":
            print("Έξοδος από το παιχνίδι. Αντίο!")
            break
        else:
            print("Μη έγκυρη επιλογή. Προσπάθησε ξανά.")

def show_score(game):
    print("\nΣΚΟΡ:")
    print(f"{game.human.name}: {game.human.score}")
    print(f"{game.computer.name}: {game.computer.score}")

def settings(game):
    print("\nΡυθμίσεις παιχνιδιού:")
    print("------------------------")
    print("Επιλογή στρατηγικής υπολογιστή:")
    print("1: Min")
    print("2: Max")
    print("3: Smart")

    algo_choice = input("Δώσε επιλογή στρατηγικής (1/2/3): ").strip()

    if algo_choice == "1":
        game.computer.strategy = "Min"
    elif algo_choice == "2":
        game.computer.strategy = "Max"
    elif algo_choice == "3":
        game.computer.strategy = "Smart"
    else:
        print("Μη έγκυρη επιλογή. Ορίστηκε η προεπιλεγμένη στρατηγική (Min).")
        game.computer.strategy = "Min"

    print(f"Η στρατηγική του υπολογιστή είναι: {game.computer.strategy}")

if __name__ == "__main__":
    game = Game()
    show_main_menu(game)
