import string
import tkinter as tk
import random
import re


class PasswordGen:
    __app_width = 300
    __app_height = 300

    def __init__(self):
        """Constructor"""

        # Widget attributes
        self.__generate = None
        self.__password_length = None
        self.__checkbox_special = None
        self.__checkbox_numbers = None
        self.__checkbox_uppercase = None
        self.__checkbox_lowercase = None
        self.__options_label = None
        self.__reset = None
        self.__password_destination = None
        self.__title_label = None
        self.__checkbox_states = {}

        # Creating the GUI using methods
        self.__window = tk.Tk()
        self.__window.title('Password generator')
        self.__position()
        self.__callback_config()

    def __position(self):
        """Positions the GUI in the middle of the screen"""

        # Get screen dimension
        screen_width = self.__window.winfo_screenwidth()
        screen_height = self.__window.winfo_screenheight()

        # Calculate the position of the middle of the screen
        x = (screen_width // 2) - (self.__app_width // 2)
        y = (screen_height // 2) - (self.__app_height // 2)

        # Place the window in the middle of the screen
        self.__window.geometry(f'{self.__app_width}x{self.__app_height}+{x}+{y}')

    def __callback_config(self):
        """Creating and configuring the checkbox callback values"""

        # Storing checkbox states in a dictionary
        checkbox_options = ['lowercase', 'uppercase', 'numbers', 'special']
        for element in checkbox_options:
            self.__checkbox_states[element] = tk.IntVar()

    def build(self):
        """Generating all the components of the GUI"""

        # Main section
        self.__title_label = tk.Label(self.__window,
                                      text="Random password generator",
                                      font='Roboto')
        self.__password_destination = tk.Entry(self.__window,
                                               width=30)

        # Options section
        self.__options_label = tk.Label(self.__window,
                                        text="Options:",
                                        font='Roboto')
        self.__checkbox_lowercase = tk.Checkbutton(self.__window,
                                                   text='Lowercase characters (a-z)',
                                                   variable=self.__checkbox_states['lowercase'])
        self.__checkbox_uppercase = tk.Checkbutton(self.__window,
                                                   text='Uppercase characters (A-Z)',
                                                   variable=self.__checkbox_states['uppercase'])
        self.__checkbox_numbers = tk.Checkbutton(self.__window,
                                                 text='Numbers (0-9)',
                                                 variable=self.__checkbox_states['numbers'])
        self.__checkbox_special = tk.Checkbutton(self.__window,
                                                 text='Special characters (@, #, % ...)',
                                                 variable=self.__checkbox_states['special'])
        self.__password_length = tk.Scale(self.__window,
                                          from_=8, to=24,
                                          orient='horizontal',
                                          label='Length:')

        # Buttons
        self.__generate = tk.Button(self.__window,
                                    text='Generate password',
                                    width=20,
                                    command=self.generate_password)
        self.__reset = tk.Button(self.__window,
                                 text='Reset to default settings',
                                 width=20,
                                 command=self.__default_settings)

        # Generate the GUI
        self.__place_widgets()
        self.__default_settings()
        self.__window.mainloop()

    def __default_settings(self):
        """Default settings of the GUI"""

        self.__password_destination.delete(0, 'end')
        self.__checkbox_lowercase.select()
        self.__checkbox_uppercase.deselect()
        self.__checkbox_numbers.select()
        self.__checkbox_special.deselect()
        self.__password_length.set(16)

    def generate_password(self):
        """Based on the selection made by the user, this will randomly generate
            a password and display it in the text box"""

        # This is where we will store our password
        password = []

        # generate a pool of characters based on the checked boxes
        characters = '' + self.__checkbox_states['lowercase'].get() * string.ascii_lowercase \
                     + self.__checkbox_states['uppercase'].get() * string.ascii_uppercase \
                     + self.__checkbox_states['numbers'].get() * string.digits \
                     + self.__checkbox_states['special'].get() * '!@#$%^&*()'

        # String to list conversion for shuffling
        pool = self.convert_string_to_list(characters)
        random.shuffle(pool)

        # Get the slider value and pick a random character from the pool that many times
        try:
            for i in range(int(self.__password_length.get())):
                password.append(random.choice(pool))
        except IndexError:
            password.extend(list('ERROR'))

        # Clear the old password and add the new one
        self.__password_destination.delete(0, 'end')
        self.__password_destination.insert(0, ''.join(password))

    def __place_widgets(self):
        """positioning the widgets on the gui"""

        # Title and output
        self.__title_label.place(relx=0.5, rely=0.1, anchor='center')
        self.__password_destination.place(relx=0.5, rely=0.2, anchor='center')

        # Checkbox group
        self.__options_label.place(relx=0.05, rely=0.3, anchor='nw')
        self.__checkbox_lowercase.place(relx=0.05, rely=0.4, anchor='nw')
        self.__checkbox_uppercase.place(relx=0.05, rely=0.5, anchor='nw')
        self.__checkbox_numbers.place(relx=0.05, rely=0.6, anchor='nw')
        self.__checkbox_special.place(relx=0.05, rely=0.7, anchor='nw')

        # Password length options
        self.__password_length.place(relx=0.2, rely=0.9, anchor='center')

        # Button placement
        self.__generate.place(relx=0.7, rely=0.85, anchor='center')
        self.__reset.place(relx=0.7, rely=0.95, anchor='center')

    @staticmethod
    def convert_string_to_list(string_to_convert):
        return re.findall(r'.', string_to_convert)
