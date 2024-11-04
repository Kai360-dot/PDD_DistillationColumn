import tkinter as tk
from tkinter import messagebox
from column import Column  # Importing the Column class

def calculate_temperature():
    # Get user input for distillate and bottoms
    distillate_input = entry_distillate.get().strip()
    bottoms_input = entry_bottoms.get().strip()

    # Process the input into lists of aliases
    distillate_aliases = [alias.strip() for alias in distillate_input.split(',') if alias.strip()]
    bottoms_aliases = [alias.strip() for alias in bottoms_input.split(',') if alias.strip()]

    if not distillate_aliases or not bottoms_aliases:
        messagebox.showerror("Input Error", "Please enter valid component aliases for both distillate and bottoms.")
        return

    try:
        # Create a Column instance using the provided aliases
        column = Column(distillate_aliases, bottoms_aliases)

        # Display the temperatures, heats of vaporization, keys, and R_min
        result_text = (
            f"The Temperature of the Distillate (top) is: {column.Temperature_top:.3f} K\n"
            f"The Temperature of the Bottoms (bottom) is: {column.Temperature_bottom:.3f} K\n\n"
            f"Heats of Vaporization at the Top:\n"
            + "\n".join(f"{comp}: {value:.2f} kJ/mol" for comp, value in column.heats_of_vaporization_top.items()) +
            f"\n\nHeats of Vaporization at the Bottom:\n"
            + "\n".join(f"{comp}: {value:.2f} kJ/mol" for comp, value in column.heats_of_vaporization_bottom.items()) +
            f"\n\nLight Key: {column.light_key}\n"
            f"Heavy Key: {column.heavy_key}\n"
            f"Average Relative Volatility w.r.t. Heavy Key:\n"
            + "\n".join(f"{comp}: {value:.2f}" for comp, value in column.avg_relative_volatility.items()) +
            f"\n\nR_min = {column.R_min:.3f}\n"
            f"R_act (1.2 * R_min) = {column.R_min * 1.2:.3f}"
        )

        result_label.config(text=result_text)

    except KeyError:
        messagebox.showerror("Error", "One or more component aliases are invalid. Please enter valid aliases.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Initialize the main window
root = tk.Tk()
root.title("Column Section Temperature Calculator")

# Distillate input
tk.Label(root, text="Enter distillate component aliases (e.g., A):").pack(pady=5)
entry_distillate = tk.Entry(root, width=50)
entry_distillate.pack(pady=5)

# Bottoms input
tk.Label(root, text="Enter bottoms component aliases (e.g., B, C, D):").pack(pady=5)
entry_bottoms = tk.Entry(root, width=50)
entry_bottoms.pack(pady=5)

# Create a button to calculate temperatures
calc_button = tk.Button(root, text="Calculate Temperatures", command=calculate_temperature)
calc_button.pack(pady=10)

# Label to display the results
result_label = tk.Label(root, text="", justify="left")
result_label.pack(pady=5)

# Run the main loop
root.mainloop()
