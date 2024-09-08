import subprocess
import os

# ANSI 转义序列
GREEN = "\033[92m"
RED = "\033[91m"

os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""{GREEN}
  ____      ____    _    _    ____  _  __  _____  _____  
 / ___|    | __ )  | |  | |  / ___|| |/ / | ____||_   _| 
| |        |  _ \  | |  | | | |    | ' /  |  _|    | |   
| |___     | |_) | | |__| | | |__  | . \  | |___   | |   
 \____|    |____/   \____/   \___| |_|\_\ |_____|  |_|   
"""
    print(banner)

def call_script(script_name):
    try:
        subprocess.run(['python', script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error occurred while calling {script_name}: {e}")

if __name__ == '__main__':
    while True:  # 添加循环以允许重新调用
        print_banner()
        user_input = input(f"{GREEN}1.模糊域名FUZZ\n2.退出\n请输入选项(填入1,2,3……): ")
        if user_input == '1':
            call_script('ip.py')  # 调用 ip.py 文件
        elif user_input == '2':
            print(f"{GREEN}退出程序")
            break  # 退出循环
        else:
            print(f"{RED}无效选项，请重试")
        os.system('cls' if os.name == 'nt' else 'clear')  # 清空屏幕
