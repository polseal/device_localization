import numpy as np
from scipy.optimize import minimize
import sqlite3
from path_loss_estimation import path_loss_param_calculation


def calculate_estimated_position():
    nu, C = path_loss_param_calculation()
    n = 1

    positions = np.array([
        (0, 0),
        (n, 0),
        (0, n)
    ])

    def fetch_last_9_entries(cursor, position):
        x, y = position
        cursor.execute("""
           SELECT rssi, point
           FROM rssi_data
           WHERE point = ?
           ORDER BY timestamp DESC
           LIMIT 9
       """, (f'{x},{y}',))
        return cursor.fetchall()

    def treat_outliers(values):
        q1 = np.percentile(values, 15)
        q3 = np.percentile(values, 85)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        cleaned_values = [value for value in values if lower_bound <= value <= upper_bound]
        return cleaned_values

    try:
        conn = sqlite3.connect('database.sqlite')
        cursor = conn.cursor()
        results = {}
        for pos in positions:
            results[tuple(pos)] = fetch_last_9_entries(cursor, pos)

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)

    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")

    rssi_values_A = [entry[0] for entry in results[(0, 0)]]
    rssi_values_B = [entry[0] for entry in results[(n, 0)]]
    rssi_values_C = [entry[0] for entry in results[(0, n)]]

    median_rssi_A = np.median(treat_outliers(rssi_values_A))
    median_rssi_B = np.median(treat_outliers(rssi_values_B))
    median_rssi_C = np.median(treat_outliers(rssi_values_C))

    # median_rssi = np.array([median_rssi_A, median_rssi_B, median_rssi_C])

    distances = 10 ** ((np.array([median_rssi_A, median_rssi_B, median_rssi_C]) - C) / (-10 * nu))
    e, f, g = distances

    p = np.linalg.norm(positions[1] - positions[0])
    q = np.linalg.norm(positions[2] - positions[0])
    r = np.linalg.norm(positions[2] - positions[1])

    def objective_function(vars):
        x, y = vars
        eq1 = e ** 2 - (x ** 2 + y ** 2)
        eq2 = f ** 2 - ((x - p) ** 2 + y ** 2)
        eq3 = g ** 2 - ((x - q) ** 2 + (y - r) ** 2)
        return eq1 ** 2 + eq2 ** 2 + eq3 ** 2

    initial_guess = np.mean(positions, axis=0)

    result = minimize(objective_function, initial_guess, method='Nelder-Mead')

    estimated_position = result.x

    print(f"Estimated position of the receiver: {estimated_position}")
    return estimated_position
