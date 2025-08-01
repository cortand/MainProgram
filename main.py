class Watchlist:

    def __init__(self):
        self._watchlist = []  # initialize to an empty watchlist

    def add(self, movieTitle):
        """Adds a movie to the watchlist"""
        cleanedTitle = movieTitle.strip()
        if cleanedTitle == "":
            print("Movie title cannot be blank.")
            return
        cleanedTitle = cleanedTitle.title()
        if cleanedTitle.lower() in [m.lower() for m in self._watchlist]:
            print(f"{cleanedTitle} is already in your watchlist.")
        else:
            self._watchlist.append(cleanedTitle)
            print(f'"{cleanedTitle}" has been successfully added to your watchlist.')
        # remove later; test
        # print(self._watchlist)

    def remove(self, movieTitle):
        """Removes a movie from the watchlist"""
        if len(self._watchlist) == 0:
            print("There are no movies to remove. Your watchlist is empty.")
            return

        for item in self._watchlist:
            if item.lower() == movieTitle.lower():
                self._watchlist.remove(item)
                print(f'"{item}" was succefully removed from your watchlist.')
                return True

        print(f'"{movieTitle}" not found in your watchlist.')
        return False

    def view(self):
        """Displays the watchlist as a numbered list"""
        if len(self._watchlist) == 0:
            print("Your Watchlist is currently empty.")
        else:
            for index, item in enumerate(self._watchlist, start=1):
                print(f"{index}. {item}")

    def get_at_index(self, index):
        """Returns the value at an index in the watchlist"""
        if 0 <= index < len(self._watchlist):
            return self._watchlist[index]
        else:
            print("Invalid index.")

    def get_size(self):
        """Returns the size of the watchlist"""
        return len(self._watchlist)

    def contains(self, title):
        """Returns whether a movie title exists in the watchlist as a boolean, True/False"""
        return any(title.lower() == movie.lower() for movie in self._watchlist)


class UI:
    def __init__(self):
        self._watchlist = Watchlist()

    def border(self):
        """Displays a border for text"""
        for i in range(65):
            print("~", end="")
        print("")

    def print_header(self, title):
        """Displays a header for the section"""
        self.border()
        print(f'You selected: {title}')
        self.border()

    def return_to_menu(self):
        """Returns to the main menu selection"""
        while True:
            menuReturn = input("\nReturn to main menu... (Press Enter to continue) ")
            if menuReturn == "":
                return self.main_menu()
            else:
                print("Invalid input")

    def add_prompt(self):
        """Prompts the user to add a movie title to the watchlist"""
        while True:
            movieTitleToAdd = str(input("Enter the movie title to add to your watchlist:\n>"))
            if movieTitleToAdd == "":
                print("Invalid Input: Movie title cannot be blank. Please enter a valid title.")
            else:
                self._watchlist.add(movieTitleToAdd)
                break

        while True:
            addAgain = input("Press 1 to add another movie, or hit Enter to return to main menu...\n")
            if addAgain == '1':
                return self.add_prompt()
            elif addAgain == "":
                return self.main_menu()
            else:
                print("Invalid input")

    def get_menu_choice(self):
        """Rerurns the correpsonding menu choice for the main menu"""
        menuChoice = None
        while menuChoice not in [1, 2, 3, 4]:
            try:
                menuChoice = int(input())
                if menuChoice not in [1, 2, 3, 4]:
                    print("Invalid input: Please enter a number 1-4.")
            except ValueError:
                print("Invalid input: Please enter a number 1-4.")
        return menuChoice

    def confirm_and_delete(self, title):
        """Prompts the user for removal confirmation and deletes the movie selected if it exists"""
        print(f'Are you sure you want to remove "{title}" from your watchlist?\n'
              "Any associated data will also be removed and cannot be undone.")
        confirmDelete = str(input("Enter 'Y' to confirm deletion\n"))
        if confirmDelete.strip().upper() == "Y":
            self._watchlist.remove(title)
            if self._watchlist.get_size() == 0:
                print("Your watchlist is now empty.")
                return self.return_to_menu()
        else:
            print(f'Invalid Input: "{title}" not removed')

    def main_menu(self):
        """Action menu loop"""
        intro = "Welcome to Your Watchlist"
        print(intro.center(65, '~'))
        print("Track your movies so you never forget what to watch next.\nView, add, or remove"
              " movies with just a few simple commands.")

        print("Please choose an option:"
              "\n1. View Watchlist"
              "\n2. Add Movie"
              "\n3. Remove Movie"
              "\n4. Exit"
              "\nEnter your choice (1-4):")

        menuChoice = self.get_menu_choice()

        if menuChoice == 1:
            self.print_header('View Watchlist')
            self._watchlist.view()
            self.return_to_menu()

        elif menuChoice == 2:
            self.print_header('Add Movie')
            self.add_prompt()

        elif menuChoice == 3:
            self.print_header('Remove Movie')
            print("Your Watchlist:")
            self._watchlist.view()

            print("\nHow would you like to remove a movie?\n"
                  "1. By list number\n"
                  "2. By movie title\n"
                  "3. Cancel and return to main menu\n"
                  "\n"
                  "Enter your choice (1-3):")

            removeChoice = None
            while removeChoice not in [1, 2, 3]:
                try:
                    removeChoice = int(input())
                    if removeChoice not in [1, 2, 3]:
                        print("Invalid input: Please choose from options 1-3.")
                except ValueError:
                    print("Invalid input: Please enter a valid number.")

                if removeChoice == 1:
                    while True:
                        if self._watchlist.get_size() == 0:
                            print("There are no movies to remove. Your watchlist is empty.")
                            return self.return_to_menu()

                        self.print_header('Remove Movie by List Number')
                        print("Your Watchlist:")
                        self._watchlist.view()

                        movieToRemove = None
                        while movieToRemove is None:
                            removeInput = input("\nEnter the corresponding number of the movie to remove"
                                                " (or hit Enter to cancel):\n>")
                            if removeInput.strip() == "":
                                return self.return_to_menu()
                            try:
                                removeNum = int(removeInput)
                                if 0 < removeNum <= self._watchlist.get_size():
                                    movieToRemove = self._watchlist.get_at_index(removeNum - 1)
                                else:
                                    print("Invalid input: No movie with that number exists.")
                            except ValueError:
                                print("Invalid Input: Please enter a valid numer or hit Enter to cancel.")

                        self.confirm_and_delete(movieToRemove)

                        while True:
                            removeMore = input("Would you like to remove a movie? Press 1 to remove, or hit "
                                               "Enter to return to Main Menu\n")
                            if removeMore == "1":
                                break
                            elif removeMore == "":
                                return self.return_to_menu()
                            else:
                                print(f'Invalid input: Press 1 to remove another movie or Enter to return to '
                                      f'Main Menu')

                if removeChoice == 2:
                    while True:
                        if self._watchlist.get_size() == 0:
                            print("There are no movies to remove. Your watchlist is empty.")
                            return self.return_to_menu()

                        self.print_header('Remove Movie by Title')
                        print("Your Watchlist:")
                        self._watchlist.view()

                        removeTitle = input("\nEnter the full title of the movie to remove"
                                            " (or hit Enter to cancel):\n").strip().title()
                        if removeTitle.strip() == "":
                            return self.return_to_menu()

                        if not self._watchlist.contains(removeTitle):
                            print(f'No movie titled "{removeTitle}" was found in your watchlist.')
                            continue

                        self.confirm_and_delete(removeTitle)

                        while True:
                            removeMore = input("Would you like to remove a movie? Press 1 to remove, or hit "
                                               "Enter to return to Main Menu\n")
                            if removeMore == "1":
                                break
                            elif removeMore == "":
                                return self.return_to_menu()
                            else:
                                print(f'Invalid input: Press 1 to remove another movie or Enter to return to Main Menu')

                if removeChoice == 3:
                    self.main_menu()

        elif menuChoice == 4:
            exit()

        else:
            print("*Invalid Option. Please select from options 1-4.*")


def main():
    ui = UI()
    ui.main_menu()


if __name__ == "__main__":
    main()
