import csv
import logging
import time
import numpy as np
from brainflow.board_shim import BoardShim, BrainFlowInputParams

class Muse2Board(BoardShim):
    def __init__(self, serial_port="COM5", debug=False, num_points=None, manual_mode=False):
        self.params = BrainFlowInputParams()
        self.params.serial_port = serial_port  # Muse 2 uses a COM port
        self.board_id = 22  # Muse 2 board ID for Windows

        super().__init__(self.board_id, self.params)

        if debug:
            BoardShim.enable_dev_board_logger()

        if num_points is None:
            self.sampling_rate = BoardShim.get_sampling_rate(self.board_id)
            window_size = 4  # 4-second window
            self.num_points = window_size * self.sampling_rate
        else:
            self.num_points = num_points

        logging.info('Preparing session')
        self.prepare_session()

        if not manual_mode:
            self.start_stream()

        self.exg_channels = np.array(BoardShim.get_exg_channels(self.board_id))
        self.last_board_data_count = 0

    def get_new_data(self):
        new_board_data_count = self.get_board_data_count()
        count_diff = new_board_data_count - self.last_board_data_count
        self.last_board_data_count = new_board_data_count
        return self.get_current_board_data(count_diff)

    def stop(self):
        self.stop_stream()
        self.release_session()

def save_data_to_csv(filename, data, channels):
    """Save EEG data to a CSV file."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        header = ["Timestamp"] + [f"Channel_{i}" for i in range(channels)]
        writer.writerow(header)

        # Write data rows
        timestamps = np.linspace(0, data.shape[1] / 256, data.shape[1])  # Simulated timestamps
        for i in range(data.shape[1]):  # Iterate over samples
            row = [timestamps[i]] + list(data[:, i])
            writer.writerow(row)

def main():
    logging.basicConfig(level=logging.INFO)

    # Initialize the Muse 2 board
    board = Muse2Board(serial_port="COM5", debug=True, num_points=256)
    start_time = time.time()  # Record the start time

    # File to save the EEG data
    csv_filename = "eeg_data.csv"

    try:
        while True:
            # Stop after 10 seconds
            if time.time() - start_time >= 10:
                print("10 seconds have passed, stopping...")
                break

            # Fetch new EEG data
            data = board.get_current_board_data(264)  # Always get 264 samples per channel

            if data.shape[1] == 0:
                print("No new data available yet...")
                time.sleep(0.1)  # Avoid tight looping
                continue

            # Save data to CSV
            save_data_to_csv(csv_filename, data, data.shape[0])

            # Display data (optional)
            print("Data shape:", data.shape)
            print("Raw Data (first 5 values of each channel):")
            for i in range(data.shape[0]):
                print(f"Channel {i}: {data[i, :5]}")

    except KeyboardInterrupt:
        print("Stopping...")

    board.stop()

if __name__ == "__main__":
    main()
