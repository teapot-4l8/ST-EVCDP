import pandas as pd
import matplotlib.pyplot as plt

# Read data from CSV file
df = pd.read_csv('data.csv')

# Create the line plot
plt.figure(figsize=(12, 6))

# Plot each line with different colors and labels
plt.plot(df.index, df['Actual Occupancy'], label='Actual', linewidth=2, color='black')
plt.plot(df.index, df['ChatEV'], label='ChatEV', linewidth=2, color='red')
plt.plot(df.index, df['PAG'], label='PAG', linewidth=2)
plt.plot(df.index, df['LSTM'], label='LSTM', linewidth=2, color='green')

# Customize the plot
plt.xlabel('Time Step', fontsize=12)
plt.ylabel('Occupancy Rate', fontsize=12)
plt.title('Comparison of Actual vs Predicted Occupancy Rates', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=10)

# Show the plot
plt.tight_layout()
plt.show()