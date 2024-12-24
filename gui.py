from tkinter import Tk, Label, StringVar, OptionMenu, Button, Toplevel, Entry, Frame, PhotoImage, messagebox

# Main window setup remains the same
window = Tk()
window.geometry("1000x600")
window.title("OS CPU")

# Set window icon
icon = PhotoImage(file="image.png")
window.iconphoto(True, icon)

# Add title label
Label(window, text="CPU Scheduling Algorithms", font=("Verdana", 35)).pack(pady=20)

# Dropdown menu
selected_option = StringVar()
selected_option.set("Select an Algorithm")  # Default value

options = [
    "First Come First Served (FCFS)",
    "Non-Preemptive Shortest Job First (SJF)",
    "Preemptive Shortest Job First (SJF)",
    "Round Robin (RR)",
    "Preemptive Priority Scheduling",
    "Non-Preemptive Priority Scheduling"
]

dropdown = OptionMenu(window, selected_option, *options)
dropdown.pack(pady=20)

# Quantum Frame for Round Robin
quantum_frame = Frame(window)
quantum_label = Label(quantum_frame, text="Time Quantum:", font=("Verdana", 10))
quantum_entry = Entry(quantum_frame, width=10, justify='center')

# Header frame
header_frame = Frame(window)
header_frame.pack()

# Header labels - Centered text with consistent width
Label(header_frame, text="Process", width=10, font=("Verdana", 10), anchor="w").grid(row=0, column=0, padx=5)
Label(header_frame, text="Burst Time", width=15, font=("Verdana", 10), anchor="center").grid(row=0, column=1, padx=5)
Label(header_frame, text="Arrival Time", width=15, font=("Verdana", 10), anchor="w").grid(row=0, column=2, padx=5)
priority_label = Label(header_frame, text="Priority", width=15, font=("Verdana", 10), anchor="w")

# Container for process rows
process_frame = Frame(window)
process_frame.pack(pady=10)

# Track process rows
process_rows = []

def validate_integer_input(value):
    """Validate if the input is a positive integer"""
    if value == "": # Allow empty field for user to type
        return True
    try:
        num = int(value)
        return num > 0
    except ValueError:
        return False

def create_entry():
    """Create a standardized Entry widget with validation"""
    vcmd = (window.register(validate_integer_input), '%P')
    entry = Entry(process_frame, width=15, justify='center', validate='key', validatecommand=vcmd)
    return entry

def create_hidden_button():
    """Create a truly invisible button that maintains spacing but can't be interacted with"""
    button = Label(process_frame, width=4)  # Using Label instead of Button
    button.grid_remove()  # Initially hidden
    return button

def update_process_labels():
    """Update process labels to ensure they're in numerical order"""
    for i, row in enumerate(process_rows):
        row[0].config(text=f"P{i + 1}")

def update_rows(*args):
    is_priority = "Priority" in selected_option.get()
    is_round_robin = "Round Robin" in selected_option.get()

    # Show or hide the Priority header
    if is_priority:
        priority_label.grid(row=0, column=3, padx=5)
    else:
        priority_label.grid_forget()

    # Show or hide the Quantum input
    if is_round_robin:
        quantum_frame.pack(after=dropdown, pady=10)
        quantum_label.pack(side='left', padx=5)
        quantum_entry.pack(side='left', padx=5)
    else:
        quantum_frame.pack_forget()

    # Update existing rows
    for row_index, row in enumerate(process_rows):
        if is_priority and (len(row) == 5 or len(row) == 4):
            priority_entry = create_entry()
            priority_entry.grid(row=row_index + 1, column=3, padx=5, pady=5)
            
            button_index = -2 if len(row) == 5 else -1
            row.insert(3, priority_entry)
            
            row[button_index].grid(row=row_index + 1, column=4, padx=5, pady=5)
            if len(row) > 5:
                row[-1].grid(row=row_index + 1, column=5, padx=5, pady=5)
                
        elif not is_priority and (len(row) == 7 or len(row) == 6):
            row[3].grid_forget()
            row.pop(3)
            
            button_index = -2 if len(row) == 5 else -1
            row[button_index].grid(row=row_index + 1, column=3, padx=5, pady=5)
            if len(row) > 4:
                row[-1].grid(row=row_index + 1, column=4, padx=5, pady=5)

def remove_process_row(row):
    for widget in row:
        widget.grid_forget()
    process_rows.remove(row)

    # Re-align remaining rows
    is_priority = "Priority" in selected_option.get()
    for row_index, row in enumerate(process_rows):
        for col_index, widget in enumerate(row):
            widget.grid(row=row_index + 1, column=col_index, padx=5, pady=5)
    
    update_process_labels()

def add_process_row():
    process_index = len(process_rows) + 1
    is_priority = "Priority" in selected_option.get()

    # Process label - Centered text
    process_label = Label(process_frame, text=f"P{process_index}", width=15, font=("Verdana", 12), anchor="center")
    process_label.grid(row=process_index, column=0, padx=5, pady=5)

    # Entry fields with centered text
    burst_entry = create_entry()
    burst_entry.grid(row=process_index, column=1, padx=5, pady=5)

    arrival_entry = create_entry()
    arrival_entry.grid(row=process_index, column=2, padx=5, pady=5)

    row = [process_label, burst_entry, arrival_entry]
    
    next_column = 3
    if is_priority:
        priority_entry = create_entry()
        priority_entry.grid(row=process_index, column=next_column, padx=5, pady=5)
        row.append(priority_entry)
        next_column += 1

    # Add and remove buttons with consistent width
    add_button = Button(process_frame, text="+", width=3)
    add_button.configure(command=add_process_row)
    add_button.grid(row=process_index, column=next_column, padx=5, pady=5)
    row.append(add_button)

    if process_index > 1:
        remove_button = Button(process_frame, text="-", width=3)
        remove_button.configure(command=lambda: remove_process_row(row))
        remove_button.grid(row=process_index, column=next_column + 1, padx=5, pady=5)
        row.append(remove_button)
    else:
        # Add hidden button for the first row to maintain spacing
        hidden_button = create_hidden_button()
        hidden_button.grid(row=process_index, column=next_column + 1, padx=5, pady=5)
        row.append(hidden_button)

    process_rows.append(row)

def validate_inputs():
    if selected_option.get() == "Select an Algorithm":
        messagebox.showerror("Error", "Please select an algorithm first!")
        return False
    
    is_priority = "Priority" in selected_option.get()
    is_round_robin = "Round Robin" in selected_option.get()

    # Validate quantum for Round Robin
    if is_round_robin:
        if not quantum_entry.get():
            messagebox.showerror("Error", "Please enter a Time Quantum value!")
            return False
        try:
            quantum = int(quantum_entry.get())
            if quantum <= 0:
                messagebox.showerror("Error", "Time Quantum must be a positive integer!")
                return False
        except ValueError:
            messagebox.showerror("Error", "Time Quantum must be a positive integer!")
            return False

    # Validate process inputs
    for row in process_rows:
        if not row[1].get() or not row[2].get():
            messagebox.showerror("Error", "Please fill all Burst Time and Arrival Time fields!")
            return False
        if is_priority and len(row) >= 4 and not row[3].get():
            messagebox.showerror("Error", "Please fill all Priority fields!")
            return False
        
        try:
            # Validate each field is a positive integer
            burst_time = int(row[1].get())
            arrival_time = int(row[2].get())
            
            if burst_time <= 0:
                messagebox.showerror("Error", "Burst Time must be a positive integer!")
                return False
            if arrival_time < 0:
                messagebox.showerror("Error", "Arrival Time must be a non-negative integer!")
                return False
                
            if is_priority and len(row) >= 4:
                priority = int(row[3].get())
                if priority <= 0:
                    messagebox.showerror("Error", "Priority must be a positive integer!")
                    return False
        except ValueError:
            messagebox.showerror("Error", "All input fields must be positive integers!")
            return False

    return True

def create_window():
    if validate_inputs():
        new_window = Toplevel(window)
        new_window.geometry("600x400")
        new_window.title("New Window")
        Label(new_window, text="Selected Algorithm:", font=("Verdana", 20)).pack(pady=20)
        Label(new_window, text=selected_option.get(), font=("Verdana", 18)).pack(pady=10)

# Setup quantum entry validation
quantum_vcmd = (window.register(validate_integer_input), '%P')
quantum_entry.configure(validate='key', validatecommand=quantum_vcmd)

# Add the first process row
add_process_row()

# Bind dropdown changes to update rows
selected_option.trace_add("write", update_rows)

# Add Next button
btn = Button(window, text="Next", command=create_window)
btn.pack(pady=20)

# Run the application
window.mainloop()

print(process_rows)