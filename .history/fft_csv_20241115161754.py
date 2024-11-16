import numpy as np
import pandas as pd
from brainflow.data_filter import DataFilter, WindowFunctions, BrainFlowMetrics

# Step 1: Load CSV data
def load_csv_data(file_path):
    data = pd.read_csv(file_path, header=None)  # Adjust header as per your CSV structure
    return data.values  # Convert to a NumPy array

# Step 2: Apply Bandpass Filtering (optional)
def bandpass_filter(data, sampling_rate, low_cutoff, high_cutoff):
    for i in range(data.shape[0]):  # Iterate over channels
        DataFilter.perform_bandpass(data[i], sampling_rate, low_cutoff, high_cutoff, 4, 
                                     FilterTypes.BUTTERWORTH.value, 0)
    return data

# Step 3: Perform FFT
def compute_fft(data, sampling_rate):
    fft_results = []
    for channel_data in data:
        # Compute FFT for each channel
        fft_result = DataFilter.perform_fft(channel_data, WindowFunctions.HANNING.value)
        fft_results.append(fft_result)
    return fft_results

# Step 4: Save FFT results (Optional)
def save_fft_results(fft_results, file_path):
    fft_array = np.array(fft_results)
    np.savetxt(file_path, fft_array, delimiter=",")
    print(f"FFT results saved to {file_path}")

# Main script
if __name__ == "__main__":
    csv_file = "filtered_psg_data.csv"  # Replace with your file path
    fft_output_file = "fft_results.csv"
    sampling_rate = 256  # Example sampling rate (Hz)

    # Load data
    raw_data = load_csv_data(csv_file)

    # Optional: Bandpass filtering (1-50 Hz)
    filtered_data = bandpass_filter(raw_data, sampling_rate, 1, 50)

    # Perform FFT
    fft_results = compute_fft(filtered_data, sampling_rate)

    # Save FFT results
    save_fft_results(fft_results, fft_output_file)

    print("FFT process completed.")
