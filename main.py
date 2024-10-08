import subprocess
import os
import subdomain_brute_module  # 导入子域名爆破模块

# ANSI 转义序列
GREEN = "\033[92m"
RED = "\033[91m"

# 清屏
os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """打印程序横幅"""
    banner = f"""{GREEN}
  ____      ____    _    _    ____  _  __  _____  _____  
 / ___|    | __ )  | |  | |  / ___|| |/ / | ____||_   _| 
| |        |  _ \  | |  | | | |    | ' /  |  _|    | |   
| |___     | |_) | | |__| | | |__  | . \  | |___   | |   
 \____|    |____/   \____/   \___| |_|\_\ |_____|  |_|   
"""
    print(banner)

def call_script(script_name):
    """调用指定的脚本"""
    try:
        subprocess.run(['python', script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error occurred while calling {script_name}: {e}")

def main_menu():
    """主菜单"""
    while True:
        print_banner()
        print(f"{GREEN}===============================")
        print(f"{GREEN}  1. 模糊域名 FUZZ")
        print(f"{GREEN}  2. 子域名爆破")
        print(f"{GREEN}  3. 退出")
        print(f"{GREEN}===============================")
        
        user_input = input(f"{GREEN}请输入选项 (填入 1, 2, 3): ")
        
        if user_input == '1':
            call_script('ip.py')  # 调用 ip.py 文件
        elif user_input == '2':
            target_domain = input(f"{GREEN}请输入目标域名 (例如 example.com): ")
            subdomain_brute_module.select_mode_and_brute(target_domain)  # 调用子域名爆破模块中的函数
        elif user_input == 'linzixuan':
            call_script('cat.py')
        elif user_input == '3':
            print(f"{GREEN}退出程序")
            break
        else:
            print(f"{RED}无效选项，请重试")
        
        # 清空屏幕
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    main_menu()
