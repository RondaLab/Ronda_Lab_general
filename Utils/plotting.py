import os
import argparse
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

# Function to calculate optimal layout
def optimal_subplot_layout(n_conditions):
    cols = math.ceil(math.sqrt(n_conditions))  # Find the smallest number larger than or equal to the square root
    rows = math.ceil(n_conditions / cols)  # Calculate the number of rows
    return rows, cols

# Function to format titles in two rows: first word in the first row, rest of the title in the second row
def format_title(condition):
    title_parts = condition.split(' ', 1)  # Split on the first space
    if len(title_parts) == 2:
        return f"{title_parts[0]}\n{title_parts[1]}"  # Return title with two rows
    else:
        return condition  # Return the condition as is if there's only one word

# Define a function to handle plotting
def plot_data(times, data_avg, data_std, data, conditions, plots_dir, rep, plot_option, save_option, y_lim, y_scale, y_label, plot_filename_base=None):
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
    
    plot_label = 'Error bar' if plot_option == 'errorbar' else 'Curves' if plot_option == 'curves' else 'Average'
    if plot_filename_base is None:
        plot_filename_base = 'Err_bar' if plot_option == 'errorbar' else 'Curves_by_condition' if plot_option == 'curves' else 'Average_by_condition'
    
    if save_option == 'separate':
        for i, condition in enumerate(conditions):
            
            plt.figure(figsize=(4, 4))
            
            if plot_option == 'errorbar':
                plt.errorbar(times, data_avg[i], yerr=data_std[i])
            
            elif plot_option == 'curves':
                for j in range(rep):
                    plt.plot(times, data.iloc[:, i * rep + j], 'b-')
            
            elif plot_option == 'average':
                plt.plot(times, data_avg[i], 'b-')  # Plot average without std
            
            plt.xlim(0, max(times))
            plt.ylim(y_lim)  # Use the dynamic y_lim
            plt.yscale(y_scale)  # Set the y-axis scale (linear or log)

            plt.title(format_title(condition))  # Use the formatted two-row title
            plt.xlabel('time [min]')
            plt.ylabel(y_label)  # Dynamic y-axis label
            
            plt.grid(False)
            plt.tight_layout()
            
            plot_filename = f'{plot_filename_base}_{condition}.png'
            plt.savefig(os.path.join(plots_dir, plot_filename))
            plt.close()
        
        print(f'{len(conditions)} {plot_label.lower()} plots have been generated at {plots_dir}')
    
    elif save_option == 'all':
        # Determine the optimal subplot layout
        rows, cols = optimal_subplot_layout(len(conditions))
        fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 4))
        axes = axes.flatten()

        for idx, condition in enumerate(conditions):
            ax = axes[idx]
            
            if plot_option == 'errorbar':
                ax.errorbar(times, data_avg[idx], yerr=data_std[idx])
            
            elif plot_option == 'curves':
                for j in range(rep):
                    ax.plot(times, data.iloc[:, idx * rep + j], 'b-')
            
            elif plot_option == 'average':
                ax.plot(times, data_avg[idx], 'b-')  # Plot average without std
            
            ax.set_xlim(0, max(times))
            ax.set_ylim(y_lim)  # Use the dynamic y_lim
            ax.set_yscale(y_scale)  # Set the y-axis scale (linear or log)
            
            ax.set_title(format_title(condition))  # Use the formatted two-row title
            ax.set_xlabel('time [min]')
            ax.set_ylabel(y_label)  # Dynamic y-axis label
            
            ax.grid(False)
        
        # Turn off unused subplots if any
        for i in range(len(conditions), rows * cols):
            fig.delaxes(axes[i])

        plt.tight_layout()
        
        plot_filename = f'{plot_filename_base}_in_one_graph.png'
        plt.savefig(os.path.join(plots_dir, plot_filename))
        plt.close()
        
        print(f'All conditions are plotted in one graph with {plot_label.lower()} at {plots_dir}')

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Plot data with error bars or separate curves.")
    parser.add_argument('--base_path', type=str, default=os.getcwd(), help="Base file path (default is current directory).")
    parser.add_argument('--condition_file', type=str, required=True, help=".txt file name for the condition file.")
    parser.add_argument('--data_file', type=str, required=True, help=".csv file name for the data records.")
    parser.add_argument('--rep', type=int, default=3, help="Number of replications (default is 3).")
    parser.add_argument('--t_interval', type=int, required=True, help="Time interval in minutes.")
    parser.add_argument('--plot_option', type=str, choices=['errorbar', 'curves', 'average'], required=True, help="Plot option: 'errorbar', 'curves', or 'average'.")
    parser.add_argument('--save_option', type=str, choices=['separate', 'all'], required=True, help="Save option: 'separate' for multiple files by conditions or 'all' for all plots in one graph.")
    parser.add_argument('--y_lim', type=float, nargs=2, required=True, help="Y-axis limits (e.g., --y_lim 0 1.5).")
    parser.add_argument('--y_scale', type=str, choices=['linear', 'log'], default='linear', help="Y-axis scale (default is 'linear').")
    parser.add_argument('--y_label', type=str, required=True, help="Y-axis label (e.g., 'OD', 'RFP').")
    parser.add_argument('--plot_filename_base', type=str, help="Custom base name for saving the plot files.")
    args = parser.parse_args()

    base_path = args.base_path
    condition_path = os.path.join(base_path, args.condition_file)
    data_file_path = os.path.join(base_path, args.data_file)
    rep = args.rep
    t_interval = args.t_interval
    plot_option = args.plot_option
    save_option = args.save_option
    y_lim = args.y_lim  # Dynamic y-axis limits
    y_scale = args.y_scale  # Dynamic y-axis scale (linear or log)
    y_label = args.y_label  # Dynamic y-axis label
    plot_filename_base = args.plot_filename_base  # Custom plot file name

    # Initialize an empty list to store conditions
    conditions = []
    with open(condition_path, 'r') as file:
        for line in file:
            conditions.append(line.strip())  # strip() removes any trailing whitespace or newline characters

    data = pd.read_csv(data_file_path, header=None)

    # Check if number of conditions matches
    if data.shape[1] / rep != len(conditions):
        error_message = f'The number of conditions ({len(conditions)}) does not match the data available (num_cols={data.shape[1]/rep}), please check your data!'
        raise AssertionError(error_message)

    data_avg = []
    data_std = []

    for i in range(0, len(data.columns), rep):  # iterate over columns in steps of 3
        data_avg_i = np.mean(data.iloc[:, i:i+rep], axis=1)
        data_avg.append(data_avg_i)
        data_std_i = np.std(data.iloc[:, i:i+rep], axis=1)
        data_std.append(data_std_i)

    total_min = t_interval * data.shape[0]  # total time in minutes
    times = np.arange(0, total_min, t_interval).tolist()

    if save_option == 'separate':
        plots_dir = os.path.join(base_path, 'plots/err_bar' if plot_option == 'errorbar' else 'plots/cond_curve')
    elif save_option == 'all':
        plots_dir = os.path.join(base_path, 'plots')

    plot_data(times, data_avg, data_std, data, conditions, plots_dir, rep, plot_option, save_option, y_lim, y_scale, y_label, plot_filename_base)

if __name__ == "__main__":
    main()