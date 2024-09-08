#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import subprocess

def print_banner():
    banner = '''
  ____      ____    _    _   ____   _  __  _____  _____  _____  
 / ___|    | __ )  | |  | | | __ ) | |/ / | ____|| ____||_   _| 
| |        |  _ \  | |  | | |  _ \ | ' /  |  _|  |  _|    | |   
| |___     | |_) | | |__| | | |_) || . \  | |___ | |___   | |   
 \____|    |____/   \____/  |____/ |_|\_\ |_____||_____|  |_|   
    '''
    print(banner)

def call_script(script_name):
    try:
        subprocess.run(['python', script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while calling {script_name}: {e}")

if __name__ == '__main__':
    print_banner()

    # 显示选项并根据用户输入选择性地调用文件
    user_input = input("1.模糊域名FUZZ")
    if user_input == '1':
        call_script('ip.py')  # 调用 ip.py 文件
