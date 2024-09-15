import aiohttp
import asyncio
import string
import itertools
import sys
import time

async def fetch_url(session, template, letter_combination, include_non_200, semaphore):
    url = template.replace('*', ''.join(letter_combination))
    async with semaphore:  # 使用信号量控制并发数量
        for _ in range(2):  # 
            try:
                async with session.get(url, timeout=3) as response:  # 超时设置为5秒
                    if response.status == 200 or include_non_200:
                        return url, response.status  # 返回成功的URL和状态码
            except Exception:  # 捕获所有请求异常并进行重试
                await asyncio.sleep(0.02)  # 重试前等待1秒
    return None  # 如果失败，返回None

async def main():
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
    total_combinations = len(letters) ** num_of_chars

    accessible_domains = []  # 存储成功访问的域名
    status_codes = []  # 存储状态码信息

    # 设置并发量限制
    semaphore = asyncio.Semaphore(1000)  # 控制并发数为1000

    async with aiohttp.ClientSession() as session:  # 使用 aiohttp 的 session 管理请求
        tasks = []
        for i, combination in enumerate(combinations, 1):
            task = fetch_url(session, template, combination, include_non_200, semaphore)
            tasks.append(task)

            # 批量处理请求, 每1000个任务处理一次
            if i % 1000 == 0 or i == total_combinations:
                results = await asyncio.gather(*tasks)  # 批量执行任务
                for result in results:
                    if result:
                        accessible_domains.append(result[0])  # 只存储URL
                        status_codes.append(result[1])  # 存储状态码
                tasks = []  # 清空任务列表
                print_progress_bar(i, total_combinations)  # 每批任务完成后更新进度条

    print()  # 打印换行以清理进度条输出

    # 打印所有成功访问的域名
    if accessible_domains:
        print("\n以下域名可访问:\n" + "="*40)
        for domain, code in zip(accessible_domains, status_codes):
            print(f"域名: {domain} - 状态码: {code}")
        print("="*40)
        
    else:
        print("没有可访问的域名。")

if __name__ == "__main__":
    while True:  # 添加循环以允许继续使用
        try:
            asyncio.run(main())  # 使用 asyncio.run() 来执行异步函数
        except KeyboardInterrupt:
            print("操作已中断。")
        
        # 询问用户是否继续使用
        continue_choice = input("是否继续使用？(y/n): ").strip().lower()
        if continue_choice != 'y':
            print("退出程序。")
            break  # 退出循环
