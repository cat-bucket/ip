import subprocess
import os

os.system('cls' if os.name == 'nt' else 'clear')

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
    while True:  # 添加循环以允许重新调用
        print_banner()
        user_input = input("1.模糊域名FUZZ\n2.退出\n请输入选项: ")
        if user_input == '1':
            call_script('ip.py')  # 调用 ip.py 文件
        elif user_input == '2':
            print("退出程序。")
            break  # 退出循环
        else:
            print("无效选项，请重试。")
        os.system('cls' if os.name == 'nt' else 'clear')  # 清空屏幕
