import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

# 进度条打印函数
def print_progress_bar(iteration, total, length=40):
    percent = (iteration / total) * 100
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r|{bar}| {percent:.2f}% 完成')
    sys.stdout.flush()

# 子域名爆破函数
def check_subdomain(subdomain, target_domain):
    url = f"http://{subdomain}.{target_domain}"
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return url  # 返回子域名的 URL
    except (requests.ConnectionError, requests.Timeout):
        pass  # 如果子域名无法访问，忽略错误
    return None

def subdomain_brute(target_domain, subdomain_list_file, threads=50):
    try:
        # 读取子域名字典
        with open(subdomain_list_file, 'r') as file:
            subdomains = file.read().splitlines()

        total_subdomains = len(subdomains)
        print(f"正在对 {target_domain} 使用字典 {subdomain_list_file} 进行子域名爆破...\n")
        found_subdomains = []

        # 使用多线程进行子域名爆破
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {executor.submit(check_subdomain, subdomain, target_domain): subdomain for subdomain in subdomains}
            completed_tasks = 0

            # 初始化进度条
            print_progress_bar(completed_tasks, total_subdomains)

            # 通过 as_completed 获取完成的任务
            for future in as_completed(futures):
                try:
                    result = future.result()  # 获取任务结果
                    if result:
                        found_subdomains.append(result)
                except Exception as e:
                    # 捕获并忽略每个 Future 内部的异常，防止程序崩溃
                    pass
                completed_tasks += 1  # 更新已完成任务数
                # 更新进度条
                print_progress_bar(completed_tasks, total_subdomains)

        # 完成后打印发现的子域名
        print()  # 打印新行，清理进度条的行
        if not found_subdomains:
            print("未发现任何子域名")
        else:
            print("\n子域名爆破完成！发现的子域名列表：")
            for domain in found_subdomains:
                print(domain)

        # 添加继续执行和结束的选择
        while True:
            print("\n请选择接下来的操作:")
            print("1. 返回主菜单")
            print("2. 结束程序")
            user_choice = input("请输入选项 (1/2): ")
            
            if user_choice == '1':
                # 返回主菜单
                return
            elif user_choice == '2':
                # 结束程序
                print("程序结束。")
                sys.exit(0)  # 正常退出程序
            else:
                print("无效选项，请重试。")

    except FileNotFoundError:
        print(f"无法找到文件 {subdomain_list_file}")

def select_mode_and_brute(target_domain):
    # 提供三种模式对应不同的字典文件，每个模式都调用50个线程
    print("选择爆破模式:")
    print("1. 快速 (min.txt)")
    print("2. 普通 (azk.txt)")
    print("3. 较大 (max.txt)")

    mode = input("请输入选择的模式 (1/2/3): ")
    
    if mode == '1':
        subdomain_brute(target_domain, 'min.txt', threads=50)  # 快速模式
    elif mode == '2':
        subdomain_brute(target_domain, 'azk.txt', threads=50)  # 普通模式
    elif mode == '3':
        subdomain_brute(target_domain, 'max.txt', threads=50)  # 较大模式
    else:
        print("无效选项，请重试。")
