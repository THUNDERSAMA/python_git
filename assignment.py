# -*- coding: utf-8 -*-
"""assignment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Gd3r3x0YSmPeM1_CemiwkyK8YdVhDbrY
"""

import pandas as pd

df = pd.read_excel("Assignment_Timecard.xlsx")

df['Time'] = pd.to_datetime(df['Time'])
df['Time Out'] = pd.to_datetime(df['Time Out'])

df['Timecard Hours (as Time)'] = df['Time Out'] - df['Time']

df['Timecard Hours (as Hours)'] = df['Timecard Hours (as Time)'].dt.total_seconds() / 3600

consecutive_days = df.groupby((df['Employee Name'] != df['Employee Name'].shift()).cumsum()).filter(lambda x: len(x) >= 7)

shift_duration = df.groupby('Employee Name')['Timecard Hours (as Hours)'].apply(lambda x: x.diff().gt(1).cumsum().where(x.diff().gt(9), 0).cumsum())
shifts = df.loc[shift_duration.gt(0)]

long_shifts = df[df['Timecard Hours (as Hours)'] > 14]

print("Employees who have worked for 7 consecutive days:")
print(consecutive_days[['Employee Name', 'Position Status']])
print("\nEmployees who have less than 10 hours of time between shifts but greater than 1 hour:")
print(shifts[['Employee Name', 'Position Status']])
print("\nEmployees who have worked for more than 14 hours in a single shift:")
print(long_shifts[['Employee Name', 'Position Status']])