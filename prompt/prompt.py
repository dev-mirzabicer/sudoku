import tkinter as tk

# Spaghetti yazmak zorundayim cunku tkinter kullanirken moduller olusturmak isi zorlastiriyor

puzzl = None
difficulty = None
selected_choices = None


def prompt():
    def get_user_choices(root):
        choices_window = tk.Toplevel(root)
        choices_window.title("AI Solver Settings")
        choices_window.attributes("-topmost", True)

        user_choices = {
            "Variable selection": tk.StringVar(value="first_unassigned_variable"),
            "Value ordering": tk.StringVar(value="unordered_domain_values"),
            "Inference": tk.StringVar(value="no_inference"),
            "Delay": tk.IntVar(value=0),
        }

        var_order_label = tk.Label(choices_window, text="Variable selection:")
        var_order_label.pack()
        var_order_default = tk.Radiobutton(
            choices_window,
            text="Default variable order",
            variable=user_choices["Variable selection"],
            value="first_unassigned_variable",
        )
        var_order_default.pack()
        var_order_min_remaining = tk.Radiobutton(
            choices_window,
            text="Minimum remaining values heuristic",
            variable=user_choices["Variable selection"],
            value="mrv",
        )
        var_order_min_remaining.pack()

        value_order_label = tk.Label(choices_window, text="Value ordering:")
        value_order_label.pack()
        value_order_default = tk.Radiobutton(
            choices_window,
            text="Default value order (unordered)",
            variable=user_choices["Value ordering"],
            value="unordered_domain_values",
        )
        value_order_default.pack()
        value_order_least_constraining = tk.Radiobutton(
            choices_window,
            text="Least-constraining-values heuristic",
            variable=user_choices["Value ordering"],
            value="lcv",
        )
        value_order_least_constraining.pack()

        inference_label = tk.Label(choices_window, text="Inference:")
        inference_label.pack()
        inference_none = tk.Radiobutton(
            choices_window,
            text="No inference",
            variable=user_choices["Inference"],
            value="no_inference",
        )
        inference_none.pack()
        inference_forward_checking = tk.Radiobutton(
            choices_window,
            text="Forward checking",
            variable=user_choices["Inference"],
            value="forward_checking",
        )
        inference_forward_checking.pack()
        inference_arc_consistency = tk.Radiobutton(
            choices_window,
            text="Arc consistency checking",
            variable=user_choices["Inference"],
            value="mac",
        )
        inference_arc_consistency.pack()

        delay_label = tk.Label(
            choices_window, text="Delay between each cell (in milliseconds):"
        )
        delay_label.pack()
        delay_entry = tk.Entry(choices_window, textvariable=user_choices["Delay"])
        delay_entry.pack()

        def get_selected_values():
            global selected_choices
            selected_choices = {
                "Variable selection": user_choices["Variable selection"].get(),
                "Value ordering": user_choices["Value ordering"].get(),
                "Inference": user_choices["Inference"].get(),
                "Delay": user_choices["Delay"].get(),
            }
            choices_window.destroy()
            root.destroy()

        submit_button = tk.Button(
            choices_window, text="Submit", command=get_selected_values
        )
        submit_button.pack()

    def solve_preset_difficulty(root):
        # Function to handle solving a pre-set sudoku puzzle based on difficulty
        difficulty_window = tk.Toplevel(root)
        difficulty_window.attributes("-topmost", True)
        difficulty_window.title("Choose Difficulty")

        def solve_puzzle(diff):
            global difficulty
            difficulty = diff
            difficulty_window.destroy()
            get_choices(root)

        label_difficulty = tk.Label(difficulty_window, text="Choose difficulty:")
        label_difficulty.grid(row=0, column=0, columnspan=5)

        easy_button = tk.Button(
            difficulty_window, text="Easy", command=lambda: solve_puzzle("Easy")
        )
        easy_button.grid(row=1, column=0)

        medium_button = tk.Button(
            difficulty_window, text="Medium", command=lambda: solve_puzzle("Medium")
        )
        medium_button.grid(row=1, column=1)

        hard_button = tk.Button(
            difficulty_window, text="Hard", command=lambda: solve_puzzle("Hard")
        )
        hard_button.grid(row=1, column=2)

        master_button = tk.Button(
            difficulty_window, text="Master", command=lambda: solve_puzzle("Master")
        )
        master_button.grid(row=1, column=3)

        expert_button = tk.Button(
            difficulty_window, text="Expert", command=lambda: solve_puzzle("Expert")
        )
        expert_button.grid(row=1, column=4)

    def create_custom_puzzle(root):
        custom_window = tk.Toplevel(root)
        custom_window.attributes("-topmost", True)
        custom_window.title("Create Custom Puzzle")

        def get_custom_puzzle():
            puzzle = ""
            for i in range(9):
                for j in range(9):
                    value = entry_boxes[i][j].get() or "."
                    if value != "." and int(value) > 9 and int(value) < 1:
                        raise ValueError("Invalid value")
                    puzzle += value
            global puzzl
            puzzl = puzzle
            get_user_choices(root)

        label_custom = tk.Label(
            custom_window, text="Enter numbers (leave empty for blank cells):"
        )
        label_custom.grid(row=0, column=0, columnspan=9)

        entry_boxes = []
        for i in range(9):
            row_entries = []
            for j in range(9):
                entry = tk.Entry(custom_window, width=3)
                entry.grid(row=i + 1, column=j)
                row_entries.append(entry)
            entry_boxes.append(row_entries)

        submit_button = tk.Button(
            custom_window, text="Submit", command=get_custom_puzzle
        )
        submit_button.grid(row=10, column=0, columnspan=9)

    def ask_user(root):
        # Function to ask user for their choice
        answer = var.get()
        if answer == "preset":
            solve_preset_difficulty(root)
        else:
            create_custom_puzzle(root)

    def get_choices(root):
        get_user_choices(root)

    root = tk.Tk()
    root.title("Sudoku Solver")

    label = tk.Label(
        root, text="Do you want to use a pre-set sudoku puzzle or make your own?"
    )
    label.pack()

    var = tk.StringVar(value="preset")
    preset_button = tk.Radiobutton(root, text="Pre-set", variable=var, value="preset")
    preset_button.pack()

    custom_button = tk.Radiobutton(
        root, text="Make your own", variable=var, value="custom"
    )
    custom_button.pack()

    submit_choice_button = tk.Button(
        root, text="Submit", command=lambda: ask_user(root)
    )
    submit_choice_button.pack()

    root.mainloop()
    return {"puzzle": puzzl, "difficulty": difficulty, "args": selected_choices}
