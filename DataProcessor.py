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
is_bme280 = False
is_bronkhorst_propar = False
is_ds18b20 = False
is_max31865 = False
is_mlx90614 = False
is_xgzp6847d = False

num_of_columns_to_use = -1

if 'ads1115' in str(args.file_path):
  is_ads1115 = True
  num_of_columns_to_use = 5
elif 'bme280' in str(args.file_path):
  is_bme280 = True
  num_of_columns_to_use = 3
elif 'bronkhorst_propar' in str(args.file_path):
  is_bronkhorst_propar = True
  num_of_columns_to_use = 6
elif 'ds18b20' in str(args.file_path):
  is_ds18b20 = True
  num_of_columns_to_use = 3
elif 'max31865' in str(args.file_path):
  is_max31865 = True
  num_of_columns_to_use = 2
elif 'mlx90614' in str(args.file_path):
  is_mlx90614 = True
  num_of_columns_to_use = 3
elif 'xgzp6847d' in str(args.file_path):
  is_xgzp6847d = True
  num_of_columns_to_use = 2

if num_of_columns_to_use == -1:
  print("ERROR: File name not known.")
  quit()

if args.debug:
  print("is_ads1115: " + str(is_ads1115))
  print("is_bme280: " + str(is_bme280))
  print("is_bronkhorst_propar: " + str(is_bronkhorst_propar))
  print("is_ds18b20: " + str(is_ds18b20))
  print("is_max31865: " + str(is_max31865))
  print("is_mlx90614: " + str(is_mlx90614))
  print("is_xgzp6847d: " + str(is_xgzp6847d))

start_time_string = str(args.start_time)
start_time_date = datetime.datetime.strptime(start_time_string, '%Y-%m-%d-%H-%M-%S')
# unix time of start
start_time = start_time_date.timestamp()

if args.debug:
  print("start_time_date: " + str(start_time_date))
  print("start_time: " + str(start_time))

end_time_string = str(args.end_time)
end_time_date = datetime.datetime.strptime(end_time_string, '%Y-%m-%d-%H-%M-%S')
# unix time of end
end_time = end_time_date.timestamp()

if args.debug:
  print("end_time_date: " + str(end_time_date))
  print("end_time: " + str(end_time))

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

with open(str(args.file_path), 'r') as data_file:
  with open(str(outpath), 'w') as out_file:
    for line in data_file:
      number_of_lines = number_of_lines + 1

      line_split_by_space = line.rstrip().split(' ')

      line_is_corrupt = False
      # If the line has less columns than the maximum, it is corrupt.
      if len(line_split_by_space) < num_of_columns_to_use:
        if args.debug:
          print("line is corrupt")
        line_is_corrupt = True
        num_of_missing_columns = num_of_missing_columns + 1

      line_has_error = False
      line_has_none = False
      Counter = 0
 
      # This skips potential error messages, maybe move this check further down or think of a better way to handle this later. Maybe a seperate script to fix
      if line_split_by_space[0].isnumeric():
        if float(line_split_by_space[0]) < start_time or float(line_split_by_space[0]) > end_time:
          continue

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
        # Delete columns and change units from some sensors
        # The + '\n' will create a trailing new line at the end of the file. Probably not a problem, but noted just in case anyway
        if is_ads1115:
          out_file.write(line_split_by_space[0] + ' ' + str(float(line_split_by_space[1]) / 1000) + ' ' + str(float(line_split_by_space[2]) / 1000000) + '\n')
        elif is_ds18b20:
          out_file.write(line_split_by_space[0] + ' ' + str(float(line_split_by_space[1]) / 1000) + '\n')
        elif is_mlx90614:
          out_file.write(line_split_by_space[0] + ' ' + str(float(line_split_by_space[1])) + '\n')
        else:
          out_file.write(' '.join(line_split_by_space) + "\n")
        if args.debug:
          print("line was fine")
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
