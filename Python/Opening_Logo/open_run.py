# -*- coding:utf-8 -*-
# Login
import os
import sys
import datetime
import configparser

config = configparser.ConfigParser()
config.read("user1.ini")
username = config.sections()
print(username)

time = datetime.datetime.now()
for i in range(3):
    user_name = input('Please input username:')
    if user_name not in username:
          print ("%s do not exist! Please input again!" % user_name)
          continue
    if os.path.exists('%s.log' % user_name):
        print ('%s is locked! Please connect admin!' % user_name)
        sys.exit()
    j = 0
    title = 3
    while j < title:
        if not config.has_option(user_name, 'password'):
            print ("Login! Welcone to our home,%s!" % user_name)
            sys.exit()
        else:
            passwd = input('Please input your password: ')
            if passwd != config.get(user_name, 'password'):
                print ("Wrong! Please input again! You still have %d choice to try." % (title - j - 1) )
                j += 1
                continue
            else:
                print ("Login! Welcone to our home,%s!" % user_name)
                sys.exit()
    else:
        print ("Try to much! %s has been locled!" % user_name)
        lock_file = open(os.path.join(os.getcwd(), "{0}.log".format( user_name) ), "w")
        lock_file.write("Trying Opening This System At {0} Time.".format(time))
        lock_file.close()
        sys.exit()
else:
    print ("Try too much!Please try later!")
    sys.exit()


    
'''
info_list = []
user_file = open(os.path.join(os.getcwd(), 'user.ini'), 'r')
for ele in user_file.readlines():
    user_info = ele.strip().replace(' ', '')
    info_list.append(user_info.split(':'))
user_dict = dict(info_list)
print(user_dict)
user_file.close()
time = datetime.datetime.now()
for i in range(3):
    user_name = input('Please input username:')
    if user_name not in user_dict.keys():
          print ("%s do not exist! Please input again!" % user_name)
          continue
    if os.path.exists('%s.log' % user_name):
        print ('%s is locked! Please connect admin!' % user_name)
        sys.exit()
    j = 0
    title = 3
    while j < title:
        passwd = input('Please input your password: ')
        if passwd != user_dict[user_name]:
            print ("Wrong! Please input again! You still have %d choice to try." % (title - j - 1) )
            j += 1
            continue
        else:
            print ("Login! Welcone to our home,%s!" % user_name)
            sys.exit()
    else:
        print ("Try to much! %s has been locled!" % user_name)
        lock_file = open(os.path.join(os.getcwd(), "{0}.log".format( user_name) ), "w")
        lock_file.write("Trying Opening This System At {0} Time.".format(time))
        lock_file.close()
        sys.exit()
else:
    print ("Try too much!Please try later!")
    sys.exit()
'''
