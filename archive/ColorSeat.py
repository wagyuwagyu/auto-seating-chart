import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Button

# Initialize lists A, B, and C with sample values
A = list(range(1, 21))  # 20 members
B = list(range(21, 51))  # 30 members
C = list(range(51, 91))  # 40 members

# Create an empty 2D list D with 12 rows and 10 columns
D = [[None for _ in range(10)] for _ in range(12)]

# Combine lists A, B, and C into one list
max = 120
col_A = len(A) // 12 + 1
index = 0

# Fill D with elements from A
for col in range(col_A):
    if col % 2 == 0:
        for row in range(max // 10):
            if index < len(A):
                D[row][col] = A[index]
                index += 1
            else:
                break
    if col % 2 != 0:
        for row in range(11, -1, -1):
            if index < len(A):
                D[row][col] = A[index]
                index += 1
            else:
                break

index = 0
for col in range(col_A, len(B) // 12 + 1 + col_A, 1):
    if col % 2 == 0:
        for row in range(max // 10):
            if index < len(B):
                D[row][col] = B[index]
                index += 1
            else:
                break
    if col % 2 != 0:
        for row in range(11, -1, -1):
            if index < len(B):
                D[row][col] = B[index]
                index += 1
            else:
                break

index = 0
col_B = len(B) // 12 + 1 + col_A
for col in range(col_B, len(C) // 12 + 1 + col_B, 1):
    if col % 2 == 0:
        for row in range(max // 10):
            if index < len(C):
                D[row][col] = C[index]
                index += 1
            else:
                break
    if col % 2 != 0:
        for row in range(11, -1, -1):
            if index < len(C):
                D[row][col] = C[index]
                index += 1
            else:
                break

# Function to display the seats in Tkinter with ttkbootstrap
def display_seats(root, seats, style):
    """Display seats in a grid using ttkbootstrap."""
    for row_index, row in enumerate(seats):
        for col_index, seat in enumerate(row):
            if seat is not None:
                # Determine the button style based on which list the seat came from
                if seat in A:
                    button_style = "A.TButton"  # Seats from list A
                elif seat in B:
                    button_style = "B.TButton"  # Seats from list B
                elif seat in C:
                    button_style = "C.TButton"  # Seats from list C
                else:
                    button_style = "default.TButton"

                # Create a button for each seat
                button = Button(root, text=f"{seat}", width=5, style=button_style)
                button.grid(row=row_index, column=col_index, padx=5, pady=5)

# Tkinter main function to create the window and display seats
def main():
    root = tk.Tk()
    root.title("Seat Layout")

    # Initialize ttkbootstrap style
    style = Style(theme='superhero')

    # Define custom styles for each type of seat
    style.configure("A.TButton", background="#4CAF50", foreground="white")  # Green
    style.configure("B.TButton", background="#2196F3", foreground="white")  # Blue
    style.configure("C.TButton", background="#FF9800", foreground="white")  # Orange

    # Display the seats
    display_seats(root, D, style)

    # Start the Tkinter main loop
    root.mainloop()

# Run the program
if __name__ == "__main__":
    main()
