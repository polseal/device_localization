import tkinter as tk

from location import calculate_estimated_position

root = tk.Tk()
root.title("Device localization solution")

def get_and_plot_coordinates():
    position = calculate_estimated_position()
    if position is not None:
        x, y = position
        canvas.delete("all")
        canvas.create_oval(x*100-5, y*100-5, x*100+5, y*100+5, fill="blue")
        coordinates_label.config(text=f"Coordinates: ({x:.2f}, {y:.2f})")
        print(f"Plotted point at: ({x:.2f}, {y:.2f})")

canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.pack()

canvas.create_line(0, 0, 600, 0, fill="black", width=2)
canvas.create_line(0, 0, 0, 600, fill="black", width=2)
canvas.create_line(600, 0, 600, 600, fill="black", width=2)
canvas.create_line(0, 600, 600, 600, fill="black", width=2)

button = tk.Button(root, text="Get Coordinates", command=get_and_plot_coordinates)
button.pack()

coordinates_label = tk.Label(root, text="Coordinates: (0.00, 0.00)")
coordinates_label.pack()

root.mainloop()
