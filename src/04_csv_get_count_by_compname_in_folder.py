#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#   Author          :   Viacheslav Zamaraev
#   email           :   zamaraev@gmail.com
#   Script Name     : 04_csv_get_count_by_compname_in_folder.py
#   Created         : 25th December 2019
#   Last Modified	: 25th December 2019
#   Version		    : 1.0
#   PIP             : pip install pewee, psycopg2
#   RESULT          : csv file with columns: COMPNAME;COUNT
# Modifications	: 1.1 -
#               : 1.2 -
#
# Description   : get count lines in each csv fle in folder

import os  # Load the Library Module
import os.path
import sys
import time
from sys import platform as _platform
from time import strftime  # Load just the strftime Module from Time
from datetime import datetime
import csv
import codecs
import logging
from peewee import *
from itertools import (takewhile,repeat)

# non standard packages
# try:
#     import peewee
# except Exception as e:
#     print("Exception occurred " + str(e), exc_info=True)
#     print("try: pip install peewee")


import cfg  # some global configurations



'''
    Create log file 
'''
def do_log_file():
    for handler in logging.root.handlers[:]:  # Remove all handlers associated with the root logger object.
        logging.root.removeHandler(handler)

    dir_out = get_output_directory()
    file_log = str(os.path.join(dir_out, cfg.file_log))  # from cfg.file
    if os.path.isfile(file_log):     # Если выходной LOG файл существует - удаляем его
        os.remove(file_log)
    logging.basicConfig(filename=file_log, format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG,
                        filemode='w')  #
    logging.info(file_log)


'''
    Get input directory from config file 
'''
def get_input_directory_from_cfg():
    directory_in = str(os.getcwd())
    if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
        if os.path.isdir(cfg.folder_linux_in):
            print('Input directory from a config file: ' + cfg.folder_linux_in)
            return cfg.folder_linux_in
        else:
            print('Input directories from config wrong: ' + cfg.folder_linux_in + ' Using current directory: ' + directory_in)
            return directory_in
    if _platform == "win32" or _platform == "win64":  # Windows or Windows 64-bit
        if os.path.isdir(cfg.folder_win_in):
            print('Input directory from a config file: ' + cfg.folder_win_in)
            return cfg.folder_win_in
        else:
            print('Input directories from config wrong: ' + cfg.folder_win_in + ' Using current directory: ' + directory_in)
            return directory_in
    return directory_in


def get_input_directory():
    # get from config
    directory_in = str(os.getcwd())
    # if only run the script (1 argument)
    if len(sys.argv) == 1:  # there is no arguments in command line
        return get_input_directory_from_cfg()

    if len(sys.argv) == 2:  # there is only one argument in command line
        directory_in = str(sys.argv[1:][0])
        if os.path.isdir(directory_in):
            return directory_in
        else:
            return get_input_directory_from_cfg()

    if len(sys.argv) > 2:  # there is only one argument in command line
        print("Arguments much more than 1! Please use only path as an argument. (Script.py /mnt/some_path) ")
        print(sys.argv, len(sys.argv))
        exit(1)
    return directory_in


def get_output_directory():
    dir_out = str(os.getcwd())
    # Linux platform
    if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
        dir_out = cfg.folder_linux_out
        print('Output directory from config file: ' + dir_out)
        if os.path.exists(dir_out) and os.path.isdir(dir_out):
            return dir_out
    if _platform == "win32" or _platform == "win64":  # Windows or Windows 64-bit
        dir_out = cfg.folder_win_out
        print('Output directory from config file' + dir_out)
        if os.path.exists(dir_out) and os.path.isdir(dir_out):
            return dir_out
    else:
        print(
            'Output directories from config wrong: ' + cfg.folder_out_win + ' or ' + cfg.folder_out_linux + ' Using current directory: ' + dir_out)
    print('Using Output directory: ' + dir_out)
    return dir_out

'''
    Get row count from file 
'''
def file_row_count(filename):
    f = open(filename, 'rb')
    bufgen = takewhile(lambda x: x, (f.raw.read(1024*1024) for _ in repeat(None)))
    return sum( buf.count(b'\n') for buf in bufgen )



'''
    Do csv files and make one csv file big
'''
def do_csv_dir(dir_input=''):
    csv_dict = {'COMPNAME': '',
                  'CNT': ''
                 }

    csv_list_in  = []
    #csv_list_out = []

    #Если выходной CSV файл существует - удаляем его
    file_csv = str(os.path.join(get_output_directory(), 'cnt' + cfg.file_csv)) # from cfg.file
    if os.path.isfile(file_csv):
        os.remove(file_csv)

    with open(file_csv, 'w', newline='', encoding='utf-8') as csv_file:  # Just use 'w' mode in 3.x
        csv_file_open = csv.DictWriter(csv_file, csv_dict.keys(), delimiter=cfg.csv_delimiter)
        csv_file_open.writeheader()
    try:
        for root, subdirs, files in os.walk(dir_input):
            for file in os.listdir(root):
                file_path = str(os.path.join(root, file))
                #.lower() - под линуксом есть разница!!!
                ext = '.'.join(file.split('.')[1:]).lower()
                if os.path.isfile(file_path) and file_path.endswith('csv'):     #ext == "csv":
                    print(file_path)
                    #csv_dict['FULLNAME'] = file_name
                    csv_dict['COMPNAME'] = file.split('-')[0]
                    csv_dict['CNT'] = file_row_count(file_path)
                    csv_list_in.append(csv_dict.copy())

    except Exception as e:
        print("Exception occurred get_list_csv_dir" + str(e))
    with open(file_csv, 'a', newline='', encoding='utf-8') as csv_file:  # Just use 'w' mode in 3.x
        csv_file_open = csv.DictWriter(csv_file, csv_dict.keys(), delimiter=cfg.csv_delimiter)
        if len(csv_list_in):
            cnt_all = 0
            ss = ''
            for csv_item in csv_list_in:
                if ss == csv_item['COMPNAME']:
                    ss = csv_item['COMPNAME']
                    cnt_all = int(cnt_all) + int(csv_item['CNT'])
                else:
                    if len(ss):
                        #ss = csv_item['COMPNAME']
                        csv_dict['COMPNAME'] = ss
                        csv_dict['CNT'] = cnt_all
                        ss = ''
                        cnt_all = 0
                        print(csv_dict)
                        csv_file_open.writerow(csv_dict)
                    else:
                        ss = csv_item['COMPNAME']
                        cnt_all = int(cnt_all) + int(csv_item['CNT'])
            csv_dict['COMPNAME'] = ss
            csv_dict['CNT'] = cnt_all
            ss = ''
            cnt_all = 0
            print(csv_dict)
            csv_file_open.writerow(csv_dict)



# ---------------- do main --------------------------------
def main():
    time1 = datetime.now()
    print('Starting at :' + str(time1))

    dir_input = get_input_directory()

    do_log_file()

    do_csv_dir(dir_input)


    time2 = datetime.now()
    print('Finishing at :' + str(time2))
    print('Total time : ' + str(time2 - time1))
    print('DONE !!!!')


if __name__ == '__main__':
    main()
