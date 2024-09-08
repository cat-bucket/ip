
def print_banner():
    banner = '''
  ____      _   ____  _    _ _  __ _  __ ______ _ 
 / ___| ___| |_| __ )| |  | | |/ /| |/ /| ____ (_)
/ |    / _ \ __|  _ \| |  | | ' / | ' / |  _| | | 
| |___|  __/ |_| |_) | |__| | . \ | . \ | |___| | 
 \____|\___|\__|____/ \____/|_|\_\|_|\_\|_____|_|
    '''
    print(banner)

if __name__ == '__main__':
    print_banner()

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import string
import itertools

def fetch_url(template, letter_combination, include_non_200):
    url = template.replace('*', ''.join(letter_combination))
    try:
        response = requests.get(url, timeout=10)  # 设置超时为10秒
        if response.status_code == 200 or include_non_200:
            print(f"可访问: {url} (状态码: {response.status_code})")  # 调试输出
            return url, response.status_code  # 返回成功的URL和状态码
        else:
            print(f"不可访问 (状态码 {response.status_code}): {url}")  # 调试输出
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e} -> {url}")  # 打印异常进行调试
    return None  # 如果失败，返回None

def main():
    print("欢迎使用网页状态检查工具！")
    template = input("请输入包含'*'的域名模板 (如http://bili*ili.com): ").strip()
    
    if '*' not in template:
        print("错误: 域名模板必须包含'*'以进行替换。")
        return

    # 允许用户选择字符集
    char_set = input("选择字符集:\n1. 小写字母\n2. 数字\n3. 小写字母 + 数字\n请输入选项 (1/2/3): ")
    
    if char_set == '1':
        letters = string.ascii_lowercase  # 小写字母
    elif char_set == '2':
        letters = string.digits  # 数字
    elif char_set == '3':
        letters = string.ascii_lowercase + string.digits  # 小写+数字
    else:
        letters = string.ascii_lowercase  # 默认小写字母

    # 询问用户希望替换的字符个数
    num_of_chars = int(input("请输入要替换的字符个数 (如1, 2, 3等): "))
    
    # 询问用户是否包括状态码不等于200的网页
    include_non_200 = input("是否将状态码不等于200的网页列为可访问网页？(y/n): ").strip().lower() == 'y'

    # 生成所有可能的字符组合
    combinations = itertools.product(letters, repeat=num_of_chars)

    accessible_domains = []  # 存储成功访问的域名
    status_codes = []  # 存储状态码信息
    
    with ThreadPoolExecutor(max_workers=100) as executor:  # 设置线程数
        futures = {executor.submit(fetch_url, template, combination, include_non_200): combination for combination in combinations}

        for future in as_completed(futures):
            result = future.result()
            if result:
                accessible_domains.append(result[0])  # 只存储URL
                status_codes.append(result[1])  # 存储状态码

    # 打印所有成功访问的域名
    if accessible_domains:
        print("\n以下域名可访问:")
        for domain in accessible_domains:
            print(domain)
        
        # 如果用户选择了显示状态码不等于200的网页，打印状态码
        if include_non_200:
            print("\n状态码信息:")
            for domain, code in zip(accessible_domains, status_codes):
                print(f"{domain} - 状态码: {code}")
    else:
        print("没有可访问的域名。")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("操作已中断。")
