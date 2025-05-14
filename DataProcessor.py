# Author: Maximilian Leo Huber
# Date:   30.03.2024

import argparse
import os
import pathlib
import datetime

current_path = str(pathlib.Path(__file__).parent.resolve()) + '/'

# TODO: Einheiten
# TODO: Manche Spalten von Sensoren können weg
# TODO: Schauen welche Sensoren datei eingegeben wurde

print("Parsing arguments...")
parser = argparse.ArgumentParser(description='Input file and flags')
parser.add_argument('-i', required=True, dest='file_path', metavar="FILE", help='File path of the input file. If the file has the name ads1115.txt, ds18b20.txt or mlx90614.txt, it will perform a bit more tasks, such as some unit conversion by dividing by 1000 for example.')
# parser.add_argument('-o', required=True, dest='output_path', metavar="FILE", help='file name of the output file')
parser.add_argument('-start_time', required=True, dest='start_time', help='starting time of the experiment/relevant data. Format is yyyy-mm-dd-hh-mm-ss. Example: "2025-03-20-14-59-00".')
parser.add_argument('-end_time', required=True, dest='end_time', help='end time of experiment/relevant data. Format is yyyy-mm-dd-hh-mm-ss. Example: "2025-03-23-14-59-00".')
parser.add_argument('-log_none_lines', required=False, dest='log_none_lines', action=argparse.BooleanOptionalAction, help='If this flag is set, all none lines will be written to the log file.')
parser.add_argument('-log_error_lines', required=False, dest='log_error_lines', action=argparse.BooleanOptionalAction, help='If this flag is set, all error lines will be written to the log file.')
parser.add_argument('-debug', required=False, dest='debug', action=argparse.BooleanOptionalAction, help='Prints out useful information for debugging the script.')

args = parser.parse_args()

check_file_path = current_path + args.file_path
# print(check_file_path)
if not os.path.exists(check_file_path):
  parser.error("The file does not exist!")
  quit()

is_ads1115 = False
is_ds18b20 = False
is_mlx90614 = False
if 'ads1115' in str(args.file_path):
  is_ads1115 = True
elif 'ds18b20' in str(args.file_path):
  is_ds18b20 = True
elif 'mlx90614' in str(args.file_path):
  is_mlx90614 = True

if args.debug:
  print("is_ads1115: " + str(is_ads1115))
  print("is_ds18b20: " + str(is_ds18b20))
  print("is_mlx90614: " + str(is_mlx90614))

start_time_string = str(args.start_time)
start_time_date = datetime.datetime.strptime(start_time_string, '%Y-%m-%d-%H-%M-%S')
# unix time of start
start_time = start_time_date.timestamp()
#print(start_time_date)
#print(start_time)

end_time_string = str(args.end_time)
end_time_date = datetime.datetime.strptime(end_time_string, '%Y-%m-%d-%H-%M-%S')
# unix time of end
end_time = end_time_date.timestamp()
#print(end_time_date)
#print(end_time)

date_and_time_now = datetime.datetime.now()
#print(date_and_time_now)
#outpath = current_path + args.output_path + str(date_and_time_now)
outpath = current_path + "filtered_" + args.file_path
logfile_path = current_path + "logfile_" + str(date_and_time_now).replace(' ', '_')

#if not os.path.exists(outpath):
#     os.makedirs(outpath)

error_message_lines = 0
removed_lines = []
none_lines = []
none_lines_counter = 0
number_of_lines = 0
num_of_missing_columns = 0

# Determine number of columns. The problem here is that sometimes a sensor 
# doesn't output data, so a column is missing. However, since the next 
# column will just be written in that place instead, it is possible that 
# an entry for column 3 for example, lands in column 2, because the sensor 
# didn't write any data for column 2. The data for column 2 would then be 
# wrong. Therefore, we need to determine the maximum number of columns and 
# always check if the current line we are looking at has as many columns 
# as the maximum. If not, we discard that line, as it is corrupt.
#
# This is obviously a huge performance inhibitor, as you have to go over
# the (usually very large) file, but I haven't found a way to check for
# this in a faster and equally inclusive manner.
# Maybe it is possible to only do the first 100 lines or something like
# that, but then you would be susceptible to situations like a sensor
# temporarily not working, which would then lead to corrupt data being
# passed on as valid.
#
# Potential problem: A space character at the end of the file can completely ruin this approach.
#
# Potential TODO: find out how many columns each file should have, check which file we are working on, use appropiate value.
#                 That should wayyy faster and more secure.
max_number_of_columns = 0
with open(str(args.file_path), 'r') as data_file:
  for line in data_file:
    line_split_by_space = line.rstrip().split(' ')
    number_of_columns = len(line_split_by_space)
    if number_of_columns > max_number_of_columns:
      max_number_of_columns = number_of_columns

if args.debug:
  print("max_number_of_columns: " + str(max_number_of_columns))

# If the maximum number of columns is 0, the file must be empty, so we
# exit the script here and inform the user.
if max_number_of_columns == 0:
  print("WARNING: the file appears to be empty!")
  quit()

with open(str(args.file_path), 'r') as data_file:
  with open(str(outpath), 'w') as out_file:
    for line in data_file:
      number_of_lines = number_of_lines + 1

      line_split_by_space = line.rstrip().split(' ')

      line_is_corrupt = False
      # If the line has less columns than the maximum, it is corrupt.
      # See comment above variable 'max_number_of_columns' for an
      # explanation.
      # Potential minor problem: error message could have little to no space chars, triggering the wrong condition here. Maybe check for error message first?
      if len(line_split_by_space) < max_number_of_columns:
        if args.debug:
          print("line is corrupt")
        line_is_corrupt = True
        num_of_missing_columns = num_of_missing_columns + 1

      line_has_error = False
      line_has_none = False
      Counter = 0

      for elem in line_split_by_space:
        if not elem.isnumeric() and elem == "None":
          if not line_has_none:
            if args.debug:
              print("line has none")
            # Add unchanged line to list for potential logging
            none_lines.append(line)

          line_has_none = True
          line_split_by_space[Counter] = '0'
        elif not elem.isnumeric():
          if args.debug:
            print("line has error message")
          line_has_error = True
          error_message_lines = error_message_lines + 1
          break

        Counter = Counter + 1

      if line_has_none:
        none_lines_counter = none_lines_counter + 1

      if not line_has_error:
        # Delete columns from some sensors
        if is_ads1115:
          out_file.write(line_split_by_space[0] + ' ' + str(float(line_split_by_space[1]) / 1000) + ' ' + str(float(line_split_by_space[2]) / 1000000) + '\n')
        elif is_ds18b20 or is_mlx90614:
          out_file.write(line_split_by_space[0] + ' ' + str(float(line_split_by_space[1]) / 1000) + '\n')
        else:
          # This creates a trailing new line. Probably not a problem, but noted just in case anyway
          out_file.write(' '.join(line_split_by_space) + "\n")
      elif args.log_error_lines:
        removed_lines.append(line)

with open(str(logfile_path), 'w') as logfile:
  logfile.write("Number of data lines in file: " + str(number_of_lines) + "\n")
  logfile.write("Number of data lines that had 'None' changed to zero: " + str(none_lines_counter) + "\n")
  logfile.write("Number of data lines that had errors in them: " + str(error_message_lines) + "\n")
  logfile.write("Number of data lines with missing columns: " + str(num_of_missing_columns) + "\n")

  if args.log_none_lines:
    logfile.write("------------------------------" + "\n")
    logfile.write("These lines had none entries!:" + "\n")
    logfile.write("------------------------------" + "\n")
    for none_line in none_lines:
      logfile.write(none_line)

  if args.log_error_lines:
    logfile.write("--------------------------" + "\n")
    logfile.write("These lines were REMOVED!:" + "\n")
    logfile.write("--------------------------" + "\n")
    for removed_line in removed_lines:
      logfile.write(removed_line)
