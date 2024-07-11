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
--base_path [PATH to where your files are saved] \ # Optional. Default is the current working directory of the Terminal
--condition_file [PATH to .txt file saving your condition list] \
--sheet_name [NAME of the SHEET you want to convert] \ # Since .csv file cannot have multiple sheets, this progarmme converts one sheet per run
--row_skip [Number of rows to skip] \ # Optional. Default value is 61, last row number before your data records start in .xlsx file.
--t_interval [Time interval between measurements in MINUTES] \
--total_hr [Total time of your measurements in HOUR] \
--rep [Number of replicates in your experiment] \ # Optional. Default value is 3.
--start_col [LETTER of the first column label] \ # Optional. Default is D.
--output_file_name [PATH to .csv file] \ # Optional. Default is df.csv under the base_path.
```

Examples:

```bash
python3 xlsx_to_csv.py --input_file_name Book1.xlsx --condition_file conditions.txt --sheet_name 'Plate 1 - Sheet1' --t_interval 15 --total_hr 30
```

```bash
python3 ~/Desktop/xlsx_to_csv.py --input_file_name Book1.xlsx --base_path ~/Desktop/data --condition_file conditions.txt --sheet_name 'Sheet1' -- row_skip 61 --t_interval 15 --total_hr 30 --rep 3 --start_col D --output_file_name df.csv
```

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
--plot_option [Plot your timecourse with error bars or as separated curves] \ # Plot option: 'errorbar' or 'curves'
--save_option [Keep your plots separately or organize them in one graph (currently only available for 20 plots in 4 x 5 layout, still updating)]\ #Save option: 'separate' for multiple files by conditions or 'all' for all plots in one graph.
```

Examples:

```bash
python3 plotting.py --condition_file conditions.txt --data_file df.csv --time_interval 15 --plot_option curves --save_option all
```

```bash
python3 ~/Desktop/plotting.py --base_path ~/Desktop/data --condition_file conditions.txt --data_file df.csv --time_interval 15 --rep 3 --plot_option curves --save_option all
```
