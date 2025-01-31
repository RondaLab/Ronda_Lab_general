```
Last update: July 11, 2024
by Zhixiang Yao
```

# Documents on code usage in CLI

## What is this document?

This document is made to provide instructions to use following codes in a command line interface (CLI) environment (the list of codes may expand...):
1. xlsx_to_csv.py
2. plotting.py

## What do the codes do?

### 1. xlsx_to_csv.py
**xlsx_to_csv.py** is a Python code used to convert recorded data from plate readers in a time course into a .csv file that only collects the readings but exclude all machine settings saved in an Excel file. \
*The converted .csv file will be saved at the same folder as that of the input .xlsx file*

### 2. plotting.py
**plotting.py** is a Python code used to plot growth curves from a .csv dataset. The code provides options to plot growth curves separatedly or average values with errorbars (defined by stdev). You can either save plots separatedly by experiment conditions or save one graph holding all plots generated. \
*The plots will be saved in a new folder under `base_path`; additional folders for separated files will be created to help better organize the output.*

## Before using the codes, you need to know:
1. The codes are available to all Ronda Lab members, and all members are welcome to modify and input suggestions
2. The codes available may be updated from time to time, this document maynot be up-to-date, if you encounter any difficulties using these codes, please contact Zhixiang Yao at zy154@berkeley.edu or through Ronda Lab's Slack.

## A. How to use xlsx_to_csv.py

### 1. Make the following files available:
1) the input .xlsx file you want to transform
2) the condition list in a .txt file format, one condition one line

### 2. Open Terminal.app (for Macbook users), or any shell environment (e.g.: GitBash)

### 3. [Optional] Redirect your working directory (wd) to the folder files indicated in step one are saved.
   [Trick] For Macbook users, you can directly open terminal under the desired folder by tapping at the folder in Finder and selecting 'New Terminal at Folder' \
   [Note] It is better to redirect your wd to the desired folder so that you will not need to type in the directories repeatedly later 

### 4. In command line, type in the commands

```bash
python3 xlsx_to_csv.py \
--input_file_name [PATH to .xlsx file] \
--base_path [PATH to where your files are saved] \ # Optional. Default is the current working directory of the Terminal.
--condition_file [PATH to .txt file saving your condition list] \
--sheet_name [NAME of the SHEET you want to convert] \ # Since .csv files cannot have multiple sheets, this program converts one sheet per run.
--measurements [List of signal channels] \ # E.g., 'OD600', 'RFP'. You can specify multiple channels.
--output_files [List of custom file names for saving each signal channel] \ # Optional. If not provided, the program will save using default names based on the measurements.
--rep [Number of replicates in your experiment] \ # Optional. Default value is 3.
--start_col [LETTER of the first column label] \ # Optional. Default is D.
```

### Parameters:
- **`--input_file_name`**: Path to the input Excel (.xlsx) file.
- **`--base_path`**: Path where output files will be saved. Optional, default is the current directory.
- **`--condition_file`**: Path to the text file containing your condition list.
- **`--sheet_name`**: The name of the Excel sheet you want to convert.
- **`--measurements`**: List of signal channels to extract (e.g., "OD600", "RFP"). You can specify multiple measurements.
- **`--output_files`**: (Optional) Custom file names for each measurement channel. If not provided, the script will use default names based on the measurement.
- **`--rep`**: (Optional) Number of replicates. Default is 3.
- **`--start_col`**: (Optional) Starting column label. Default is 'D'.

### Examples:

```bash
# Example 1: Extract OD600 and RFP data, using default file names
python3 xlsx_to_csv.py --input_file_name Book1.xlsx --condition_file conditions.txt --sheet_name 'Plate 1 - Sheet1' --measurements "OD600" "RFP"
```

```bash
# Example 2: Extract data and save with custom file names
python3 xlsx_to_csv.py --input_file_name Book1.xlsx --base_path ~/Desktop/data --condition_file conditions.txt --sheet_name 'Sheet1' --measurements "OD600" "RFP" --output_files "od600_data.csv" "rfp_data.csv" --rep 3 --start_col D
```

This updated instruction covers the new features:
- **Flexible signal channel selection** (`--measurements`).
- **Optional custom output filenames** (`--output_files`).

## B. How to use plotting.py

### 1. Make the following files available:
1) the input .xlsx file you want to transform
2) the condition list in a .txt file format, one condition one line

### 2. Same as step 2 in A

### 3. Same as step 3 in A

### 4. In command line, type in the commands

```bash
python3 plotting.py \
--base_path [PATH to where your files are saved] \ # Optional. Default is the current working directory of the Terminal
--condition_file [PATH to .txt file saving your condition list] \
--data_file [PATH to .csv file recording your measurements] \
--t_interval [Time interval between measurements in MINUTES] \
--rep [Number of replicates in your experiment] \ # Optional. Default value is 3.
--plot_option [Choose how to plot your timecourse: error bars, separate curves, or averages] \ # Plot option: 'errorbar', 'curves', or 'average'
--save_option [Keep your plots separately or organize them in one graph (supports any number of plots with optimal layout)]\ # Save option: 'separate' for multiple files by conditions or 'all' for all plots in one graph.
--y_lim [Y-axis limits for your plot (e.g., 0 1.5)] \ # Required. Set the Y-axis range for your plots.
--y_scale [Y-axis scale: linear or log] \ # Optional. Default is 'linear'.
--y_label [Label for the Y-axis] \ # Required. Set the Y-axis label for your plot.
--plot_filename_base [Custom base name for saving your plot files] \ # Optional. Default name based on plot option.
```

### Example Commands:

```bash
python3 plotting.py --condition_file conditions.txt --data_file df.csv --t_interval 15 --plot_option curves --save_option all --y_lim 0 1.5 --y_label 'OD'
```

```bash
python3 ~/Desktop/plotting.py --base_path ~/Desktop/data --condition_file conditions.txt --data_file df.csv --t_interval 15 --rep 3 --plot_option errorbar --save_option all --y_lim 0 1.5 --y_scale log --y_label 'OD' --plot_filename_base 'MyCustomPlot'
```

### Changes from the older version:

1. **Plot options:** In addition to `errorbar` and `curves`, you can now choose the `average` option to plot only the average values.
2. **Y-axis settings:** You must specify the y-axis limits (`--y_lim`), and you can choose between a linear or logarithmic scale (`--y_scale`).
3. **Y-axis label:** The y-axis label is now customizable via the `--y_label` argument.
4. **Custom plot filenames:** You can set a custom base name for the plot files using the `--plot_filename_base` argument.
5. **Flexible subplot layout:** The script now supports any number of plots, and it automatically arranges the subplots in an optimal layout.