import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# 子域名爆破函数
def check_subdomain(subdomain, target_domain):
    url = f"http://{subdomain}.{target_domain}"
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            print(f"发现子域名: {url}")
            return url
    except requests.ConnectionError:
        # 子域名不存在
        pass
    return None

def subdomain_brute(target_domain, subdomain_list_file, threads=50):
    try:
        with open(subdomain_list_file, 'r') as file:
            subdomains = file.read().splitlines()

        print(f"正在对 {target_domain} 使用字典 {subdomain_list_file} 进行子域名爆破...\n")
        found_subdomains = []

        # 使用多线程进行子域名爆破
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(check_subdomain, subdomain, target_domain) for subdomain in subdomains]

            for future in as_completed(futures):
                result = future.result()
                if result:
                    found_subdomains.append(result)

        if not found_subdomains:
            print("未发现任何子域名")
        else:
            print("\n子域名爆破完成！发现的子域名列表：")
            for domain in found_subdomains:
                print(domain)

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
