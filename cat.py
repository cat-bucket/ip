import requests

# 子域名爆破函数
def subdomain_brute(target_domain, subdomain_list_file):
    try:
        with open(subdomain_list_file, 'r') as file:
            subdomains = file.read().splitlines()

        print(f"正在对 {target_domain} 进行子域名爆破...\n")
        found_subdomains = []

        for subdomain in subdomains:
            url = f"http://{subdomain}.{target_domain}"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    print(f"发现子域名: {url}")
                    found_subdomains.append(url)
            except requests.ConnectionError:
                # 子域名不存在
                pass
        
        if not found_subdomains:
            print("未发现任何子域名")
        else:
            print("\n子域名爆破完成！发现的子域名列表：")
            for domain in found_subdomains:
                print(domain)

    except FileNotFoundError:
        print(f"无法找到文件 {subdomain_list_file}")

if __name__ == '__main__':
    domain = input("请输入目标域名 (例如 example.com): ")
    subdomain_brute(domain, 'subdomains.txt')
