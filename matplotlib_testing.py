import matplotlib.pyplot as plt
import numpy as np
import pandas as po

df = po.read_csv("scores.csv")

print(df.head())
print("--------------------------------------------------")
print(df.tail())
print("--------------------------------------------------")
print(df)
print("--------------------------------------------------")
print("--------------------------------------------------")

print(df.describe())

print("--------------------------------------------------")
print("--------------------------------------------------")


print(df.groupby("database")["python"].mean())