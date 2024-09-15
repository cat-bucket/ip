import aiohttp
import asyncio
import string
import itertools
import sys

def print_progress_bar(iteration, total, length=40):
    percent = (iteration / total) * 100
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r|{bar}| {percent:.2f}% 完成 ({iteration}/{total})')
    sys.stdout.flush()

async def fetch_url(session, template, letter_combination, include_non_200, semaphore):
    url = template.replace('*', ''.join(letter_combination))
    async with semaphore:  # 使用信号量控制并发数量
        for _ in range(3):  # 尝试最多3次
            try:
                async with session.get(url, timeout=2) as response:  
                    if response.status == 200 or include_non_200:
                        return url, response.status  # 返回成功的URL和状态码
            except Exception:  # 捕获所有请求异常并进行重试
                await asyncio.sleep(0.05)  # 重试前等待0.05秒
    return None  # 如果失败，返回None

async def process_batch(session, batch, template, include_non_200, semaphore, total, processed):
    tasks = [fetch_url(session, template, combination, include_non_200, semaphore) for combination in batch]
    results = await asyncio.gather(*tasks)
    
    accessible_domains = []
    status_codes = []
    
    for result in results:
        if result:
            accessible_domains.append(result[0])
            status_codes.append(result[1])
    
    processed[0] += len(batch)  # 更新已处理的数量
    print_progress_bar(processed[0], total)  # 更新进度条
    return accessible_domains, status_codes

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
    semaphore = asyncio.Semaphore(500)  # 控制并发数为500

    batch_size = 500  # 每批处理500个组合
    processed = [0]  # 已处理的数量（用列表以便在协程中修改）
    
    async with aiohttp.ClientSession() as session:  # 使用 aiohttp 的 session 管理请求
        batch = []
        for combination in combinations:
            batch.append(combination)
            if len(batch) >= batch_size:
                # 批量处理
                domains, codes = await process_batch(session, batch, template, include_non_200, semaphore, total_combinations, processed)
                accessible_domains.extend(domains)
                status_codes.extend(codes)
                batch = []  # 清空批次任务

        # 处理剩余未满批次的任务
        if batch:
            domains, codes = await process_batch(session, batch, template, include_non_200, semaphore, total_combinations, processed)
            accessible_domains.extend(domains)
            status_codes.extend(codes)

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
