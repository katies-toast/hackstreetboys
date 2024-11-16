import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load Data from CSV
file_path = "data.csv"  # Replace with your CSV file path
data = pd.read_csv(file_path)

# Extract the column of interest (assuming it's named 'signal')
signal = data['signal'].values  # Replace 'signal' with the column name in your CSV

# Step 2: Apply FFT
N = len(signal)  # Number of data points
T = 1.0 / 100.0  # Sampling interval (1/Sampling frequency, e.g., 100 Hz)
fft_values = np.fft.fft(signal)
frequencies = np.fft.fftfreq(N, T)

# Step 3: Analyze FFT
magnitude = np.abs(fft_values)  # Magnitude spectrum
positive_frequencies = frequencies[:N // 2]  # Only keep positive frequencies
positive_magnitude = magnitude[:N // 2]  # Positive half of spectrum

# Step 4: Plot the Results
plt.figure(figsize=(10, 6))
plt.plot(positive_frequencies, positive_magnitude)
plt.title("FFT Magnitude Spectrum")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid()
plt.show()
