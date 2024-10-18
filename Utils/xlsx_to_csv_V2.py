import pandas as pd
import argparse
import os

# Function to convert column letter to index
def col_to_index(col):
    index = 0
    for char in col:
        index = index * 26 + (ord(char.upper()) - ord('A')) + 1
    return index

# Function to extract the total runtime, interval, and number of intervals from the "Start Kinetic" row
def extract_runtime_info(df):
    start_kinetic_row = df[df[0] == "Start Kinetic"].index[0]
    runtime_info = df.iloc[start_kinetic_row, 1]

    # Extract total hours and interval in minutes from the string
    total_hr = int(runtime_info.split(' ')[1].split(':')[0])  # Extract total hours (e.g., "30:00:00")
    t_interval = int(runtime_info.split('Interval ')[1].split(':')[1])  # Extract interval in minutes (e.g., "0:15:00")
    
    # Calculate number of intervals
    total_min = total_hr * 60
    num_interval = total_min // t_interval + 1
    
    return total_hr, t_interval, num_interval

# Function to find the row with a specified measurement (e.g., "OD600", "RFP") in column A
def find_measurement_row(df, measurement):
    for i, value in enumerate(df.iloc[:, 0]):  # Iterate over the first column (A)
        if measurement in str(value):  # Allow partial matching (e.g., "OD600" matches "OD600:600")
            return i  # Return the row index where it's found
    return None  # If not found, return None

def main(args):
    # Load the workbook and select the specific sheet
    file_path = os.path.join(args.base_path, args.input_file_name)
    condition_path = os.path.join(args.base_path, args.condition_file)
    sheet_name = args.sheet_name
    
    # Initialize an empty list to store conditions
    conditions = []
    with open(condition_path, 'r') as file:
        for line in file:
            conditions.append(line.strip())  # strip() removes any trailing whitespace or newline characters

    # Load the entire sheet to extract runtime info and locate measurement rows
    df_all = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    
    # Extract total hours, interval, and number of intervals from "Start Kinetic"
    total_hr, t_interval, num_interval = extract_runtime_info(df_all)
    print(f"Extracted total_hr: {total_hr}, t_interval: {t_interval}, num_interval: {num_interval}")

    # Fixed end_col set to "CU"
    end_col = "CU"

    # Identify the column range for data extraction
    cols = f'{args.start_col}:{end_col}'

    # Iterate over each signal channel provided by the user
    for i, measurement in enumerate(args.measurements):
        # Find the row containing the specified measurement (e.g., "OD600", "RFP")
        measurement_row = find_measurement_row(df_all, measurement)
        if measurement_row is None:
            print(f"The value '{measurement}' was not found in column A.")
            continue

        # Skip 3 rows from the found row for data extraction
        row_skip = measurement_row + 3
        
        # Read the specific range into a DataFrame, starting from the calculated row_skip
        df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=cols, skiprows=row_skip, nrows=num_interval, header=None)

        # Remove any empty columns
        df.dropna(axis=1, how='all', inplace=True)  # Drops columns where all values are NaN

        # Define output file name (use user-provided name if available, else default to measurement-based name)
        if args.output_files and len(args.output_files) > i:
            out_file_name = args.output_files[i]
        else:
            out_file_name = f'{measurement.replace(":", "_").replace(",", "_")}.csv'
        
        out_path = os.path.join(args.base_path, out_file_name)

        # Save DataFrame to a CSV file for the current measurement
        df.to_csv(out_path, index=False, header=False)

        print(f'The data for "{measurement}" has been saved as {out_file_name}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read specific range from an Excel file and save it to separate CSV files for each signal channel.")
    parser.add_argument('--input_file_name', type=str, help="Name of the input Excel file.")
    parser.add_argument('--base_path', type=str, default=os.getcwd(), help="Base path for input and output files.")
    parser.add_argument('--condition_file', type=str, required=True, help=".txt file name for the condition file.")
    parser.add_argument('--sheet_name', type=str, required=True, help="Sheet name to read from.")
    parser.add_argument('--measurements', type=str, nargs='+', required=True, help="List of signal measurements (e.g., 'OD600', 'RFP').")
    parser.add_argument('--output_files', type=str, nargs='*', help="Optional list of filenames for saving each measurement (e.g., 'od600.csv', 'rfp.csv').")
    parser.add_argument('--rep', type=int, default=3, help="Number of replicates.")
    parser.add_argument('--start_col', type=str, default='D', help="Starting column.")
    
    args = parser.parse_args()
    main(args)
