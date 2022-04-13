#!/usr/bin/env python3
import os
import datetime
import shutil

''' Скрипт запрашивает у администратора список доменных имён пользователей для удаления, бэкапит исходный конфиг,
сохраняет во временный файл результат удаления, заменяет старый файл новым.'''
del_name = input("Введите доменное имя пользователя (логин), можно задать список логинов (apetrov,gsokolov,gtarasov): ")
if len(del_name.split(',')) > 1:
    del_name = del_name.split(',')


def del_user_from_svn():
    # ('/etc/apache2/svn.auth') - на сервере
    read_file = 'svn.auth'
    write_file = 'new_svn.auth'
    today = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    with open(read_file, 'r') as svn_auth, open(write_file, 'w+') as svn_auth_new:
        for line in svn_auth.readlines():
            line = line.strip('\n')
            if line.startswith('[groups]'):
                svn_auth_new.write(f"{line}\n")  # adding [groups] in new config-file
            elif not line.startswith('[groups]') and line.startswith('['):
                svn_auth_new.write(f"\n{line}\n")  # adding groups in new config-file
            if len(line.split('=')) == 2:
                name, rights = line.split('=')
                name = name.rstrip(' ')
                if len(rights.split(',')) > 1:
                    group_users = rights.split(',')
                    group_users_new = str()
                    # print(group_users)
                    for i in group_users:
                        if i not in del_name:
                            group_users_new += i + ','
                    rights = group_users_new[:-1]
                if name not in del_name:
                    # print(name, '==', del_name)
                    svn_auth_new.write(f"{name} = {rights}\n")
    shutil.copyfile('./svn.auth', ('svn_auth' + today + '.txt'))  # Бэкапит исходный конфиг перед удалением
    os.replace('./new_svn.auth', './svn.auth')
    print(f"Удалены пользователи: {del_name}")


print(f'Удалить:{del_name}?')  # Доп. проверка перед удалением
user_answer = input("Введите [yes/no]: ").lower()
yes = ("yes", "y", "ye")

if user_answer in yes:
    del_user_from_svn()
else:
    print("Действие отменено.")
    exit()
