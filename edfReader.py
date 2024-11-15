import pyedflib
import pandas as pd

def edf_to_csv(edf_file, csv_output):
    """
    Reads an EDF file and exports its signals to a CSV file.
    
    Args:
        edf_file (str): Path to the EDF file.
        csv_output (str): Path to save the output CSV file.
    """
    try:
        # Open the EDF file
        edf_reader = pyedflib.EdfReader(edf_file)
        
        # Retrieve header information
        signal_headers = edf_reader.getSignalHeaders()
        n_signals = edf_reader.signals_in_file
        
        # Extract signals and their labels
        signals = []
        labels = [signal_headers[i]['label'] for i in range(n_signals)]
        
        for i in range(n_signals):
            signals.append(edf_reader.readSignal(i))
        
        # Convert to DataFrame
        df = pd.DataFrame(data=list(zip(*signals)), columns=labels)
        
        # Save to CSV
        df.to_csv(csv_output, index=False)
        print(f"Data successfully exported to {csv_output}")
        
        # Close EDF reader
        edf_reader.close()
    
    except Exception as e:
        print(f"Error processing {edf_file}: {e}")

# Example Usage
edf_file_path = "SC4001E0-PSG.edf" # Replace with the path to your EDF file
csv_output_path = "SC4001EC-Hypnogram.edf"     # Replace with the desired output CSV path

edf_to_csv(edf_file_path, csv_output_path)
