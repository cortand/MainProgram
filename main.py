from persistence_client import PersistenceClient


class Watchlist:

    def __init__(self):
        try:
            # create connection to persistence microservice
            self.persistence_client = PersistenceClient()

            # attempt to load existing data
            watchlist_data = self.persistence_client.load_watchlist()

            if watchlist_data is not None:
                # if service connection was successful, load data
                self._watchlist = watchlist_data
                self.service_available = True
            else:
                raise Exception("Service not responding")
        except:
            # use memory-only mode if persistence service unavailable
            self.persistence_client = None
            self._watchlist = []
            self.service_available = False

    def add(self, movie_title):
        """Adds a movie to the watchlist"""
        cleanted_title = movie_title.strip()
        if cleanted_title == "":
            print("Movie title cannot be blank.")
            return
        cleanted_title = cleanted_title.title()
        if cleanted_title.lower() in [m.lower() for m in self._watchlist]:
            print(f"{cleanted_title} is already in your watchlist.")
        else:
            self._watchlist.append(cleanted_title)
            print(f'"{cleanted_title}" has been successfully added to your watchlist.')
            self._persist()

    def remove(self, movie_title):
        """Removes a movie from the watchlist"""
        if len(self._watchlist) == 0:
            print("There are no movies to remove. Your watchlist is empty.")
            return

        for item in self._watchlist:
            if item.lower() == movie_title.lower():
                self._watchlist.remove(item)
                print(f'"{item}" was succefully removed from your watchlist.')
                self._persist()
                return True

        print(f'"{movie_title}" not found in your watchlist.')
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

    def _persist(self):
        """
        Saves the current watchlist to the persistence service if available.
        If unavailable, displayes a message indicating that it is only saving in the current session.
        """
        if self.service_available:
            success = self.persistence_client.save_watchlist(self._watchlist)
            if not success:
                print("Note: Not connected to persistence service. Your changes were saved only within this session.\n")


class UI:
    def __init__(self):
        self._watchlist = Watchlist()

    def border(self):
        """Displays a border for text"""
        for i in range(70):
            print("~", end="")
        print("")

    def print_header(self, title):
        """Displays a header for the section"""
        self.border()
        print(f'You selected: {title}')
        self.border()

    def display_steps(self, action_name):
        """Shows step-by-step instructions for add and delete actions before starting the first step."""
        if action_name == "add":
            print("You have chosen to add a movie to your watchlist.\n"
                  "Steps:\n"
                  "1. Enter the movie title\n"
                  "2. Confirm the title has been added.\n"
                  "3. Choose to add another movie or return to the main menu selection.")
        elif action_name == "remove_by_num":
            print("You have chosen to remove a movie by list number.\n"
                  "Steps:\n"
                  "1. View your watchlist\n"
                  "2. Enter the corresponding number of the movie title to remove\n"
                  "3. Confirm deletion\n"
                  "4. Choose to remove another movie or return to the main menu selection.")
        elif action_name == "remove_by_title":
            print("You have chosen to remove a movie by title.\n"
                  "Steps:\n"
                  "1. View your watchlist\n"
                  "2. Enter the full movie title\n"
                  "3. Confirm deletion\n"
                  "4. Choose to remove another movie or return to the main menu selection.")
        self.border()
        input("Press Enter to continue...\n")

    def return_to_menu(self):
        """Returns to the main menu selection"""
        while True:
            menu_return = input("\nReturn to main menu... (Press Enter to continue) ")
            if menu_return == "":
                return self.main_menu()
            else:
                print("Invalid input")

    def add_prompt(self, show_instructions=True):
        """Prompts the user to add a movie title to the watchlist"""
        if show_instructions:
            self.display_steps("add")

        while True:
            movie_title_to_add = str(input("Enter the movie title to add to your watchlist:\n>"))
            if movie_title_to_add == "":
                print("Invalid Input: Movie title cannot be blank. Please enter a valid title.")
            else:
                self._watchlist.add(movie_title_to_add)
                break

        while True:
            addAgain = input("Press 1 to add another movie, or hit Enter to return to main menu...\n")
            if addAgain == '1':
                return self.add_prompt(show_instructions=False)
            elif addAgain == "":
                return self.main_menu()
            else:
                print("Invalid input")

    def get_menu_choice(self):
        """Returns the correpsonding menu choice for the main menu"""
        menu_choice = None
        while menu_choice not in [1, 2, 3, 4]:
            try:
                menu_choice = int(input())
                if menu_choice not in [1, 2, 3, 4]:
                    print("Invalid input: Please enter a number 1-4.")
            except ValueError:
                print("Invalid input: Please enter a number 1-4.")
        return menu_choice

    def confirm_and_delete(self, title):
        """Prompts the user for removal confirmation and deletes the movie selected if it exists"""
        print(f'Are you sure you want to remove "{title}" from your watchlist?\n'
              "Any associated data will also be removed and cannot be undone.")
        confirm_delete = str(input("Enter 'Y' to confirm deletion\n"))
        if confirm_delete.strip().upper() == "Y":
            self._watchlist.remove(title)
            if self._watchlist.get_size() == 0:
                print("Your watchlist is now empty.")
                return self.return_to_menu()
        else:
            print(f'Invalid Input: "{title}" not removed')

    def main_menu(self):
        """Action menu loop"""
        # status indicator showing persistence service avaiability
        if self._watchlist.service_available:
            print("[Saving: ON]")
        else:
            print("[Memory Mode]")

        intro = "Welcome to Your Watchlist"
        print(intro.center(65, '~'))

        print("Track your movies so you never forget what to watch next.\nView, add, or remove"
              " movies with just a few simple commands.\n")

        print("Please choose an option:"
              "\n1. View Watchlist"
              "\n2. Add Movie"
              "\n3. Remove Movie"
              "\n4. Exit"
              "\nEnter your choice (1-4):")

        menu_choice = self.get_menu_choice()

        if menu_choice == 1:
            self.print_header('View Watchlist')
            self._watchlist.view()
            self.return_to_menu()

        elif menu_choice == 2:
            self.print_header('Add Movie')
            self.add_prompt(show_instructions=True)

        elif menu_choice == 3:
            self.print_header('Remove Movie')
            print("Your Watchlist:")
            self._watchlist.view()

            print("\nHow would you like to remove a movie?\n"
                  "1. By list number\n"
                  "2. By movie title\n"
                  "3. Cancel and return to main menu\n"
                  "\n"
                  "Enter your choice (1-3):")

            remove_choice = None
            while remove_choice not in [1, 2, 3]:
                try:
                    remove_choice = int(input())
                    if remove_choice not in [1, 2, 3]:
                        print("Invalid input: Please choose from options 1-3.")
                except ValueError:
                    print("Invalid input: Please enter a valid number.")

                if remove_choice == 1:
                    show_instructions = True
                    while True:
                        if self._watchlist.get_size() == 0:
                            print("There are no movies to remove. Your watchlist is empty.")
                            return self.return_to_menu()

                        self.print_header('Remove Movie by List Number')

                        if show_instructions:
                            self.display_steps("remove_by_num")
                            show_instructions = False

                        print("Your Watchlist:")
                        self._watchlist.view()

                        movie_to_remove = None
                        while movie_to_remove is None:
                            remove_input = input("\nEnter the corresponding number of the movie to remove"
                                                " (or hit Enter to cancel):\n>")
                            if remove_input.strip() == "":
                                return self.return_to_menu()
                            try:
                                remove_num = int(remove_input)
                                if 0 < remove_num <= self._watchlist.get_size():
                                    movie_to_remove = self._watchlist.get_at_index(remove_num - 1)
                                else:
                                    print("Invalid input: No movie with that number exists.")
                            except ValueError:
                                print("Invalid Input: Please enter a valid number or hit Enter to cancel.")

                        self.confirm_and_delete(movie_to_remove)

                        while True:
                            remove_more = input("Would you like to remove a movie? Press 1 to remove, or hit "
                                               "Enter to return to Main Menu\n")
                            if remove_more == "1":
                                break
                            elif remove_more == "":
                                return self.return_to_menu()
                            else:
                                print(f'Invalid input: Press 1 to remove another movie or Enter to return to '
                                      f'Main Menu')

                if remove_choice == 2:
                    show_instructions = True
                    while True:
                        if self._watchlist.get_size() == 0:
                            print("There are no movies to remove. Your watchlist is empty.")
                            return self.return_to_menu()

                        self.print_header('Remove Movie by Title')
                        if show_instructions:
                            self.display_steps("remove_by_title")
                            show_instructions = False

                        print("Your Watchlist:")
                        self._watchlist.view()

                        remove_title = input("\nEnter the full title of the movie to remove"
                                            " (or hit Enter to cancel):\n").strip().title()
                        if remove_title.strip() == "":
                            return self.return_to_menu()

                        if not self._watchlist.contains(remove_title):
                            print(f'No movie titled "{remove_title}" was found in your watchlist.')
                            continue

                        self.confirm_and_delete(remove_title)

                        while True:
                            remove_more = input("Would you like to remove a movie? Press 1 to remove, or hit "
                                               "Enter to return to Main Menu\n")
                            if remove_more == "1":
                                break
                            elif remove_more == "":
                                return self.return_to_menu()
                            else:
                                print(f'Invalid input: Press 1 to remove another movie or Enter to return to Main Menu')

                if remove_choice == 3:
                    self.main_menu()

        elif menu_choice == 4:
            exit()

        else:
            print("*Invalid Option. Please select from options 1-4.*")


def main():
    try:
        ui = UI()
        ui.main_menu()
    except KeyboardInterrupt:
        print("Exiting")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
