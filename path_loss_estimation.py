import sqlite3

import pandas as pd
import numpy as np
from scipy import stats

def treat_outliers(group):
    Q1 = group['y'].quantile(0.25)
    Q3 = group['y'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    median = group['y'].median()
    group['y'] = np.where((group['y'] < lower_bound) | (group['y'] > upper_bound), median, group['y'])
    return group


def path_loss_param_calculation():
    global cursor
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT dictance, rssi FROM reference')
    data = cursor.fetchall()
    conn.close()
    distance = [row[0] for row in data]
    rssi = [row[1] for row in data]
    data = pd.DataFrame({'distance': distance, 'rssi': rssi})
    distances = data["distance"].apply(lambda x: float(x))
    rssi_values = data["rssi"]
    data = pd.DataFrame({'x': distances, 'y': rssi_values})
    treated_data = data.groupby('x').apply(treat_outliers).reset_index(drop=True)
    cleaned_rssi = treated_data['y']
    log_distances = np.log10(distances)
    slope, intercept, r_value, p_value, std_err = stats.linregress(log_distances, cleaned_rssi)
    n = -slope / 10
    C = intercept
    r_squared = r_value ** 2
    print(f"Estimated value of n is: {n}")
    print(f"Estimated value of C is: {C}")
    print(f"R^2 value: {r_squared}")
    return n, C