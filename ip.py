import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import string
import itertools

def fetch_url(template, letter_combination):
    url = template.replace('*', ''.join(letter_combination))
    try:
        response = requests.get(url, timeout=10)  # 设置超时为10秒
        if response.status_code == 200:
            print(f"可访问: {url}")  # 调试输出
            return url  # 返回成功的URL
        else:
            print(f"不可访问 (状态码 {response.status_code}): {url}")  # 调试输出
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e} -> {url}")  # 打印异常进行调试
    return None  # 如果失败，返回None

def main():
    template = input("请输入包含'*'的域名模板 (如http://bili*ili.com): ").strip()
    
    if '*' not in template:
        print("域名模板必须包含'*'以进行替换。")
        return

    # 允许用户选择字符集
    char_set = input("请输入要使用的字符集 (默认是小写字母，输入 '1' 使用小写字母，'2' 使用大写字母，'3' 使用数字，'4' 使用小写字母+大写字母+数字): ")
    
    if char_set == '1':
        letters = string.ascii_lowercase  # 小写字母
    elif char_set == '2':
        letters = string.ascii_uppercase  # 大写字母
    elif char_set == '3':
        letters = string.digits  # 数字
    elif char_set == '4':
        letters = string.ascii_letters + string.digits  # 小写+大写+数字
    else:
        letters = string.ascii_lowercase  # 默认小写字母

    # 询问用户希望替换的字符个数
    num_of_chars = int(input("请输入要替换的字符个数 (如1, 2, 3等): "))
    
    # 生成所有可能的字符组合
    combinations = itertools.product(letters, repeat=num_of_chars)

    accessible_domains = []  # 存储成功访问的域名
    
    with ThreadPoolExecutor(max_workers=100) as executor:  # 设置线程数
        futures = {executor.submit(fetch_url, template, combination): combination for combination in combinations}

        for future in as_completed(futures):
            result = future.result()
            if result:
                accessible_domains.append(result)

    # 打印所有成功访问的域名
    if accessible_domains:
        print("以下域名可访问:")
        for domain in accessible_domains:
            print(domain)
    else:
        print("没有可访问的域名。")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("操作已中断。")
