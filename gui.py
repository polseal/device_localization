import tkinter as tk
from location import calculate_estimated_position  # Assuming this function exists

root = tk.Tk()
root.title("Device Localization Solution")

real_x = None
real_y = None

def plot_real_point():
    global real_x, real_y
    real_x = float(real_x_entry.get())
    real_y = float(real_y_entry.get())
    canvas.delete("all")
    draw_triangle()
    canvas.create_oval(real_x*100-5, 600-real_y*100-5, real_x*100+5, 600-real_y*100+5, fill="red")
    coordinates_label.config(text=f"Real Coordinates: ({real_x:.2f}, {real_y:.2f})")
    print(f"Real point at: ({real_x:.2f}, {real_y:.2f})")

def get_and_plot_coordinates():
    position = calculate_estimated_position()
    if position is not None:
        x, y = position
        canvas.create_oval(x*100-5, 600-y*100-5, x*100+5, 600-y*100+5, fill="blue")
        coordinates_label.config(text=f"Estimated Coordinates: ({x:.2f}, {y:.2f})")
        print(f"Plotted estimated point at: ({x:.2f}, {y:.2f})")

def draw_triangle():
    points = [0, 0, 3, 0, 3, 3]
    scaled_points = [x * 100 for x in points]
    scaled_points[1] = 600 - scaled_points[1]
    scaled_points[3] = 600 - scaled_points[3]
    scaled_points[5] = 600 - scaled_points[5]
    canvas.create_polygon(scaled_points, outline="black", fill="", width=2)

canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.pack()

draw_triangle()

real_x_label = tk.Label(root, text="Enter real X coordinate (0 to 3):")
real_x_label.pack()
real_x_entry = tk.Entry(root)
real_x_entry.pack()

real_y_label = tk.Label(root, text="Enter real Y coordinate (0 to 3):")
real_y_label.pack()
real_y_entry = tk.Entry(root)
real_y_entry.pack()

plot_button = tk.Button(root, text="Plot Real Point", command=plot_real_point)
plot_button.pack()

button = tk.Button(root, text="Get Coordinates", command=get_and_plot_coordinates)
button.pack()

coordinates_label = tk.Label(root, text="Coordinates: (0.00, 0.00)")
coordinates_label.pack()

root.mainloop()