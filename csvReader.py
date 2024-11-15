import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Define a bandpass filter function
def bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs  # Nyquist frequency
    low = lowcut / nyquist  # Normalize lowcut
    high = highcut / nyquist  # Normalize highcut

    # Ensure cutoff frequencies are in valid range
    if not (0 < low < 1) or not (0 < high < 1):
        raise ValueError("Cutoff frequencies must be between 0 and Nyquist frequency.")

    # Create bandpass filter
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, data)
    return y

# Load CSV file
data = pd.read_csv("psg_data.csv")

# Define parameters for bandpass filtering
fs = 100  # Sampling rate in Hz (100 Hz based on your description)
lowcut = 0.5  # Low cutoff frequency in Hz
highcut = 49.9  # High cutoff frequency in Hz

# Filter the signals in the dataset
filtered_data = data.copy()
for column in ["EEG Fpz-Cz", "EEG Pz-Oz", "EOG horizontal", "EMG submental"]:
    filtered_data[column] = bandpass_filter(data[column], lowcut, highcut, fs)

# Save filtered data to a new CSV file
filtered_data.to_csv("filtered_psg_data.csv", index=False)

# Plot example to verify filtering
plt.figure(figsize=(10, 6))
plt.plot(data["EEG Fpz-Cz"][:1000], label="Original EEG Fpz-Cz")
plt.plot(filtered_data["EEG Fpz-Cz"][:1000], label="Filtered EEG Fpz-Cz", linestyle="--")
plt.legend()
plt.title("EEG Fpz-Cz: Original vs. Filtered")
plt.xlabel("Samples")
plt.ylabel("Amplitude (µV)")
plt.show()
