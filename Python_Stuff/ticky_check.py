#!/usr/bin/env python3

import re
import operator
import csv

error_types = {}
user_errors = {}

def extract_errors(log_line):
  pattern = r"ticky: ERROR ([\w ']*).* \(([\w .]*)\)"
  result = re.search(pattern,log_line)
  if result is None:
    return ""
  return result

def extract_users(log_line):
  pattern = r"ticky: ([A-Z]*).* \(([\w .]*)\)"
  result = re.search(pattern,log_line)
  if result is None:
    return ""
  return result

with open("C:\\Users\\joelr\\OneDrive\\Documents\\GitHub\\GitHub_Coursera\\Python_Stuff\\syslog.log") as file:
  for line in file:
    result = extract_errors(line)
    if result != "":
      if result[1] in error_types:
        error_types[result.group(1)] += 1
      else:
        error_types[result.group(1)] = 1
    user_result = extract_users(line)
    if user_result != "":
      if user_result.group(2) in user_errors:
        if user_result.group(1)=="INFO":
          user_errors[user_result.group(2)][0]+=1
        elif user_result.group(1)=="ERROR":
          user_errors[user_result.group(2)][1]+=1
      else:
        if user_result[1]=="INFO":
          user_errors[user_result.group(2)]=[1,0]
        elif user_result[1]=="ERROR":
          user_errors[user_result.group(2)]=[0,1]

sorted_errors=[("Error","Count")] + sorted(error_types.items(), key=operator.itemgetter(1), reverse=True)
print(sorted_errors)

# print(sorted(user_errors.items()))

# print(sorted(user_errors.items()))
sorted_users=[("Username",["INFO","ERROR"])] + sorted(user_errors.items())
# print(sorted_users[0][1])

i=0
sorted_users_tuples = []
while i < len(sorted_users):
  sorted_users_tuples = sorted_users_tuples + [(sorted_users[i][0],sorted_users[i][1][0],sorted_users[i][1][1])]
  i+=1
print(sorted_users_tuples)

# name of csv file
filename = "error_message.csv"

# writing errors to csv file
with open(filename, 'w',newline='') as csvfile:
  # creating a csv writer object
  csvwriter = csv.writer(csvfile)

  # writing the fields
  csvwriter.writerows(sorted_errors)

# name of users csv file
filename = "user_statistics.csv"

# writing to csv file
with open(filename, 'w',newline='') as csvfile:
  # creating a csv writer object
  csvwriter = csv.writer(csvfile)

  # writing the fields
  csvwriter.writerows(sorted_users_tuples)

  # for key in sorted_users.keys():
  #   csvwriter.writerow([key]+sorted_users[key])

