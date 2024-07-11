import pandas as pd
import argparse
import os

# Function to convert column letter to index
def col_to_index(col):
    index = 0
    for char in col:
        index = index * 26 + (ord(char.upper()) - ord('A')) + 1
    return index

# Function to convert column index to letter
def index_to_col(index):
    col = ''
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        col = chr(65 + remainder) + col
    return col

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
    
    # Set data range
    total_min = args.total_hr * 60  # total time in minutes
    num_interval = total_min // args.t_interval + 1 # Number of time points

    # Identify number of measurements
    total_col = len(conditions) * args.rep  # Total columns

    # Identify number of columns in .xlsx document
    start_index = col_to_index(args.start_col)
    end_index = start_index + total_col - 1
    end_col = index_to_col(end_index)  # End column in .xlsx document
    cols = f'{args.start_col}:{end_col}'

    # Read the entire range into a DataFrame
    df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=cols, skiprows=args.row_skip, nrows=num_interval, header=None)

    # Define output path and file name
    out_path = os.path.join(args.base_path, args.output_file_name)

    # Save DataFrame to CSV
    df.to_csv(out_path, index=False, header=False)
    
    print(f'The data from Excel in range {args.start_col}{args.row_skip + 1}:{end_col}{args.row_skip + num_interval} is saved as {out_path}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read specific range from an Excel file and save it to a CSV file.")
    parser.add_argument('----input_file_name', type=str, help="Name of the input Excel file.")
    parser.add_argument('--base_path', type=str, default=os.getcwd(), help="Base path for input and output files.")
    parser.add_argument('--condition_file', type=str, required=True, help=".txt file name for the condition file.")
    parser.add_argument('--sheet_name', type=str, required=True, help="Sheet name to read from.")
    parser.add_argument('--row_skip', type=int, default=61, help="Number of rows to skip.")
    parser.add_argument('--t_interval', type=int, required=True, help="Time interval in minutes.")
    parser.add_argument('--total_hr', type=int, required=True, help="Total time in hours.")
    parser.add_argument('--rep', type=int, default=3, help="Number of replicates.")
    parser.add_argument('--start_col', type=str, default='D', help="Starting column.")
    parser.add_argument('--output_file_name', type=str, default='df.csv', help="Name of the output CSV file.")
    
    args = parser.parse_args()
    main(args)
