import tkinter as tk


def solved_screen():
    solved_window = tk.Tk()
    solved_window.title("Sudoku Solved")

    label = tk.Label(solved_window, text="Sudoku successfully solved!")
    label.pack()

    play_again = tk.BooleanVar(value=False)
    play_again_yes = tk.Radiobutton(
        solved_window, text="Play again", variable=play_again, value=True
    )
    play_again_yes.pack()

    play_again_no = tk.Radiobutton(
        solved_window, text="Quit", variable=play_again, value=False
    )
    play_again_no.pack()

    submit_button = tk.Button(
        solved_window, text="Submit", command=solved_window.destroy
    )
    submit_button.pack()

    solved_window.mainloop()
    return play_again.get()


def invalid_screen():
    invalid_window = tk.Tk()
    invalid_window.title("Invalid Sudoku")

    label = tk.Label(invalid_window, text="Invalid Sudoku! Please try again.")
    label.pack()

    try_again = tk.BooleanVar(value=False)
    try_again_yes = tk.Radiobutton(
        invalid_window, text="Try again", variable=try_again, value=True
    )
    try_again_yes.pack()

    try_again_no = tk.Radiobutton(
        invalid_window, text="Quit", variable=try_again, value=False
    )
    try_again_no.pack()

    submit_button = tk.Button(
        invalid_window, text="Submit", command=invalid_window.destroy
    )
    submit_button.pack()

    invalid_window.mainloop()
    return try_again.get()
