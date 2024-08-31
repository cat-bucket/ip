import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import string

def fetch_url(template, letter):
    url = template.replace('*', letter)
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

    letters = string.ascii_lowercase  # 获取所有小写字母 'a' 到 'z'
    
    accessible_domains = []  # 存储成功访问的域名
    
    with ThreadPoolExecutor(max_workers=26) as executor:  # 使用26个线程（因为有26个字母）
        futures = {executor.submit(fetch_url, template, letter): letter for letter in letters}

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
