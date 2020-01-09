#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#   Author          :   Viacheslav Zamaraev
#   email           :   zamaraev@gmail.com
#   Script Name     : 01_shp_prj_srid_identify_check.py
#   Created         : 25th September 2019
#   Last Modified	: 25th September 2019
#   Version		    : 1.0
#   PIP             : pip install sridentify chardet openpyxl pandas
#   RESULT          : csv file with columns: FILENAME;PRJ;SRID;METADATA;CODEPAGE;HAS_DEFIS;DATA_CREATION;DATA_MODIFY;DATA_LASTACCESS
# Modifications	: 1.1 -
#               : 1.2 -
#
# Description   : This script will search some *.shp files in the given directory and makes CSV file with some information

import os  # Load the Library Module
import os.path
import sys
import time
from sys import platform as _platform
from time import strftime  # Load just the strftime Module from Time
from datetime import datetime
import csv
# non standard packages

# try:
#     import peewee
# except Exception as e:
#     print("Exception occurred " + str(e), exc_info=True)
#     print("try: pip install peewee")


import cfg  # some global configurations


def get_input_directory():
    # get from config
    directory_in_win = cfg.folder_win_in
    directory_in_linux = cfg.folder_linux_in
    directory_in = str(os.getcwd())
    # if only run the script (1 argument)
    if len(sys.argv) == 1:  # there is only one argument in command line
        # Linux platform
        if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
            directory_in = directory_in_linux
            return directory_in
        if _platform == "win32" or _platform == "win64":  # Windows or Windows 64-bit
            directory_in = directory_in_win
            return directory_in
        else:
            directory_in = str(os.getcwd())
            print(
                'Input directories from config wrong: ' + directory_in_win + ' or ' + directory_in_linux + ' Using current directory: ' + directory_in)
        print('Input directory from a config file: ' + directory_in)
        return directory_in

    if len(sys.argv) == 2:  # there is only one argument in command line
        directory_in = str(sys.argv[1:][0])
        if os.path.isdir(directory_in):
            return directory_in
        else:
            print(
                directory_in + " is not a Directory (Folder). Please specify an input directory. correctly. We use config file parameters.")
            if _platform == "linux" or _platform == "linux2" or _platform == "darwin":  # Linux platform
                directory_in = directory_in_linux
                return directory_in
            if _platform == "win32" or _platform == "win64":  # Windows or Windows 64-bit
                directory_in = directory_in_win
                return directory_in
            else:
                directory_in = str(os.getcwd())
                print(
                    'Input directories from config wrong: ' + directory_in_win + ' or ' + directory_in_linux + ' Using current directory: ' + directory_in)
            print('Input directory from a config file: ' + directory_in)
            return directory_in

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
        if os.path.exists(dir_out) and os.path.isdir(dir_out):
            return dir_out
    if _platform == "win32" or _platform == "win64":  # Windows or Windows 64-bit
        dir_out = cfg.folder_win_out
        if os.path.exists(dir_out) and os.path.isdir(dir_out):
            return dir_out
    else:
        dir_out = str(os.getcwd())
        print(
            'Output directories from config wrong: ' + cfg.folder_out_win + ' or ' + cfg.folder_out_linux + ' Using current directory: ' + dir_out)
    print('Using Output directory: ' + dir_out)
    return dir_out


def do_csv_file_in(filename_with_path=''):
    file_name = filename_with_path.split('.')[0]
    # print(file_name)
    # with open(filename_with_path, newline='', encoding='utf-8') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     for row in reader:
    #         print(row['FullName'], row['Length'])


    # # Read CSV file
    # kwargs = {'newline': ''}
    # mode = 'r'
    # if sys.version_info < (3, 0):
    #     kwargs.pop('newline', None)
    #     mode = 'rb'
    # with open(filename_with_path, mode, **kwargs) as fp:
    #     reader = csv.reader(fp, delimiter=cfg.csv_delimiter, quotechar='"') #delimiter=','
    #     # next(reader, None)  # skip the headers
    #     data_read = [row for row in reader]
    #     print(data_read[0])

    with open(filename_with_path, 'r', encoding='utf-8') as csvfile:
     #sniff to find the format
        filedialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        #read the CSV file into a dictionary
        dict_reader = csv.DictReader(csvfile, dialect=filedialect, quotechar='"')
        for row in dict_reader:
            #do your processing here
            print(row)


def do_csv_dir(dir_input=''):
    #_yes = cfg.value_yes
    #_no = cfg.value_no
    #_error = cfg.value_error
    # file_csv = cfg.file_csv

    file_csv = str(os.path.join(get_output_directory(),
                                cfg.file_csv))  # str(strftime("%Y-%m-%d") + "_shp_info_in_folder_" + ".csv")

    if os.path.isfile(file_csv):
        os.remove(file_csv)

    csv_dict = {'COMPNAME': '',
                'DISK': '',
                'FOLDER': '',
                'FILENAME': '',
                # 'CODEPAGE': '',
                # 'HAS_DEFIS': '',
                # 'DATA_CREATION': '',
                # 'DATA_MODIFY': '',
                # 'DATA_LASTACCESS': '',
                # 'DATA_SCRIPT_RUN': '',
                # 'PRJ_INFO': '',
                # 'COUNT_REC': '',
                # 'COUNT_FIELDS': '',
                'LAST_UPDATE': ''}  # 'CODEPAGE_DBF': '', # CODEPAGE_DBF -  work a long time

    with open(file_csv, 'w', newline='', encoding='utf-8') as csv_file:  # Just use 'w' mode in 3.x

        csv_file_open = csv.DictWriter(csv_file, csv_dict.keys(), delimiter=cfg.csv_delimiter)
        csv_file_open.writeheader()
        for root, subdirs, files in os.walk(dir_input):
            for file in os.listdir(root):
                file_path = str(os.path.join(root, file)).lower()
                ext = '.'.join(file.split('.')[1:]).lower()
                if os.path.isfile(file_path) and file_path.endswith('csv'):#ext == "csv":
                    for key in csv_dict:
                        csv_dict[key] = ''
                    #csv_dict['DATA_SCRIPT_RUN'] = str(time.strftime("%Y-%m-%d"))
                    csv_dict['FILENAME'] = file_path


                    do_csv_file_in(file_path)


                    # csv_dict['DATA_LASTACCESS'] = str(
                    #     datetime.fromtimestamp(os.path.getatime(file_path)).strftime('%Y-%m-%d'))
                    # Codepage DBF - work long time
                    # file_dbf = file_name + '.dbf'
                    # if os.path.isfile(file_dbf):
                    #
                    #     csv_dict['CODEPAGE_DBF'] = get_encoding(file_dbf)
                    # else:
                    #     csv_dict['CODEPAGE_DBF'] = _no
                    # Get records Count from DBF - work long time
                    # if len(str_log):
                    csv_file_open.writerow(csv_dict)
                    # print(str(csv_dict.values()))
        csv_file.close()


# ---------------- do main --------------------------------
def main():
    time1 = datetime.now()
    print('Starting at :' + str(time1))

    dir_input = get_input_directory()

    do_csv_dir(dir_input)

    # csv2xls()

    time2 = datetime.now()
    print('Finishing at :' + str(time2))
    print('Total time : ' + str(time2 - time1))
    print('DONE !!!!')


if __name__ == '__main__':
    main()
