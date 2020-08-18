##################
### dec_ins.py ###
##################

# This is the primary function for making suitable edits in .conf files.
# Use of Decorator Pattern is Optional here but in Logging module it made the work easier.

import functools
from find_path import *


def dec_ins(f_found):
    # bkp = []
    # f_found = find_path()
    for x in f_found:
        def my_decorator1(func1):
            @functools.wraps(func1)
            def function_that_runs_func1():
                backup(x)
                func1()
            return function_that_runs_func1

        @my_decorator1
        def my_function1():
                fil = open(x, 'r')
                print "\nModifying file " + x
                file_data = fil.readlines()
                fil.close()

                # print "Now will read file..."
                list_find = lf()
                for item in list_find:
                    count = 0
                    for lines in file_data:
                        if item in lines:
                            count = 1
                            if lines.startswith('#'):
                                file_data[file_data.index(lines)] = str(item)
                                break
                    if count == 0:
                        file_data.append('\n'+str(item))
                        print "\nSuccessfully added " + item + " in file " + x

                s_file_data = "".join(file_data)
                fil = open(x, 'w')
                fil.write(s_file_data)
                fil.close()

        my_function1()
