import mne
import numpy as np
import pandas as pd

def load_edf(file_path):
    # Load the EDF file
    raw = mne.io.read_raw_edf(file_path, preload=True)
    
    # Extract EEG channel names
    eeg_channels = mne.pick_types(raw.info, eeg=True, exclude=[])
    
    # Select only EEG data
    eeg_data = raw.get_data(picks=eeg_channels)
    sfreq = raw.info['sfreq']  # Sampling frequency
    
    print(f"Loaded EDF file with {len(eeg_channels)} EEG channels and sampling rate {sfreq} Hz.")
    return eeg_data, sfreq, eeg_channels
