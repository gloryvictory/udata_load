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
#import csv
import codecs

# non standard packages

# try:
#     import peewee
# except Exception as e:
#     print("Exception occurred " + str(e), exc_info=True)
#     print("try: pip install peewee")


import cfg  # some global configurations


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


def get_file_name_with_extension(path):
    return path.split('\\').pop().split('/')[0]        #  path.split('\\').pop().split('/').pop().rsplit('.', 1)[0]


def get_file_name_without_extension(path):
    return path.split('\\').pop().split('/').pop().rsplit(get_extension(path), 1)[0]



def get_extension(filename):
    basename = os.path.basename(filename)  # os independent
    ext = '.'.join(basename.split('.')[1:])
    return '.' + ext if ext else None


def do_csv_file_in(filename_with_path=''):
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

    file_name = filename_with_path.split('.')[0]

    for key in csv_dict:
        csv_dict[key] = ''
    # csv_dict['DATA_SCRIPT_RUN'] = str(time.strftime("%Y-%m-%d"))
    csv_dict['FILENAME'] = file_name # file_path

    f = codecs.open(filename_with_path, 'r', 'UTF-8')

    # get Headers from file (first line of file)
    for line in f:
        ss = line.strip()
        headers = ss.split(',')
        headers2 = []
        for header in headers:
            ss = header.strip('\"')
            headers2.append(ss)
        print('Columns from csv_file: ' + str(len(headers)) + ' in File: ' + filename_with_path)
        column_names_in = cfg.csv_fieldnames_in
        print('Columns from cfg: ' + str(len(column_names_in)))
        tt = [x for x in headers2 if x in column_names_in]  # [x for x in a if x in b]
        print('Сolumns matched: ' + str(len(tt)) + ' Columns: ' + str(tt))
        break    # break here

    # do all lines in csv file
    for line in f:
        next(f)  # skip first ine
        try:
            current_line = str(line).split(cfg.csv_delimiter)
            compname = current_line[0].strip("\"")
            file_full_path_name = current_line[1].strip("\"")
            length = current_line[2].strip("\"")
            tmpstr = current_line[3].replace(",", "")
            tmpstr = tmpstr.replace("\"", "")
            creation_time = tmpstr.strip()

            _is_profile = False

            _compname = compname
            _disk = file_full_path_name.split(":")[0]
            _folder = str(os.path.dirname(os.path.abspath(file_full_path_name)))
            ss = _folder.lower()
            if _folder.startswith("c:\\users"):
                _is_profile = True
            _filename_long = get_file_name_with_extension(file_full_path_name)
            _filename_shot = get_file_name_without_extension(file_full_path_name)
            _ext_long = get_extension(file_full_path_name)
            _ext_shot = file_full_path_name.split(".")[-1]
            _size = length
            _fullname = file_full_path_name
            _year = creation_time.split()[0]
            _month = creation_time.split(".")[1]
            _creationtime = creation_time
            _fio = ''
            _otdel = ''

            _text = file_full_path_name.strip().lower()
            _text = _text.replace(":"," ")
            _text = _text.replace("\\", " ")
            _text = _text.replace(",", " ")
            _text = _text.replace(".", " ")
            _text = _text.replace("-", " ")
            _text = _text.replace(";", " ")
            _text = _text.replace("\"", "")
            _text = _text.replace("_", "")
            _text = _text.replace("\'", "")

            _textfull = _text
            _textless = _text # need to tranformate
            lastupdate = ''


            print(line)
            #

        except Exception as e:
            print("Exception occurred " + str(e), exc_info=True)


    # with open(filename_with_path, 'r', encoding='utf-8') as csvfile:
    #     #read the CSV file into a dictionary
    #     dict_reader = csv.DictReader(csvfile, dialect='excel', quotechar='"', delimiter=cfg.csv_delimiter)
    #     column_names = dict_reader.fieldnames
    #     column_names_in = cfg.csv_fieldnames_in
    #
    #     print('Columns from cfg: ' + str(len(column_names_in)))
    #     print('Columns from csv_file: ' + str(len(column_names)) + ' in File: ' + filename_with_path)
    #
    #     tt = [x for x in column_names if x in column_names_in]  # [x for x in a if x in b]
    #     print('Сolumns matched: ' + str(len(tt)) + ' Columns: ' + str(tt))
    #
    #     reader = csv.reader(csvfile)
    #     for row in reader:
    #         #do your processing here
    #         asd = str(row).split(cfg.csv_delimiter)
    #         qq = row['compname']
    #         aa = row['FullName']
    #         print(qq)
    f.close()




#    csv_file_open.writerow(csv_dict)
#         csv_file.close()


def do_csv_dir(dir_input=''):
    # Если выходной CSV файл существует - удаляем его
    file_csv = str(os.path.join(get_output_directory(), cfg.file_csv)) # from cfg.file
    if os.path.isfile(file_csv):
        os.remove(file_csv)

    # Если выходной LOG файл существует - удаляем его
    file_log = str(os.path.join(get_output_directory(), cfg.file_log))  # from cfg.file
    if os.path.isfile(file_log):
        os.remove(file_log)

    # for root, subdirs, files in os.walk(dir_input):
    #     for file in os.listdir(root):
    #         file_path = str(os.path.join(root, file)).lower()
    #         ext = '.'.join(file.split('.')[1:]).lower()
    #         if os.path.isfile(file_path) and file_path.endswith('csv'):     #ext == "csv":
    #             do_csv_file_in(file_path) #'e:\\temp\\csv\\weizelev-c-.csv'

    do_csv_file_in('e:\\temp\\csv\\weizelev-c-.csv')  # 'e:\\temp\\csv\\weizelev-c-.csv'



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
