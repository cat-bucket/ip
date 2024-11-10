import hashlib
import time
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pathlib import Path
from tqdm import tqdm
import itertools
import os

class MD5Cracker:
    def __init__(self, target_hash, chunk_size=10000):
        self.target_hash = target_hash
        self.chunk_size = chunk_size
        self.cpu_count = mp.cpu_count()
        
    def md5_worker(self, password):
        try:
            calculated_hash = hashlib.md5(password.encode()).hexdigest()
            return calculated_hash == self.target_hash, password, calculated_hash
        except Exception:
            return False, password, None

    def process_chunk(self, passwords):
        matches = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = executor.map(self.md5_worker, passwords)
            for is_match, pwd, hash_val in results:
                if is_match:
                    matches.append((pwd, hash_val))
                    return matches
        return matches

    def crack_from_file(self, filepath):
        print(f"\n开始破解，使用 {self.cpu_count} 个进程")
        start_time = time.time()
        
        with ProcessPoolExecutor(max_workers=self.cpu_count) as process_executor:
            futures = []
            
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                while True:
                    chunk = list(itertools.islice(f, self.chunk_size))
                    if not chunk:
                        break
                    chunk = [line.strip() for line in chunk]
                    futures.append(process_executor.submit(self.process_chunk, chunk))
            
            for future in tqdm(futures, desc="处理进度"):
                result = future.result()
                if result:
                    process_executor.shutdown(wait=False)
                    elapsed = time.time() - start_time
                    return result, elapsed
        
        elapsed = time.time() - start_time
        return None, elapsed

def main():
    print("MD5 哈希破解器")
    
    target_hash = input("\n请输入目标MD5哈希值: ").strip()
    filename = input("请输入密码文件名称: ").strip()
        
    cracker = MD5Cracker(target_hash)
    
    try:
        result, elapsed = cracker.crack_from_file(filename)
        
        if result:
            password, hash_val = result[0]
            print(f"\n[+] 找到密码!")
            print(f"密码: {password}")
            print(f"哈希值: {hash_val}")
        else:
            print("\n[-] 在密码列表中未找到匹配")
            
        print(f"\n耗时: {elapsed:.2f} 秒")
        
    except KeyboardInterrupt:
        print("\n[!] 用户中断操作")
    except FileNotFoundError as e:
        print(f"\n[!] 错误: {str(e)}")
    except Exception as e:
        print(f"\n[!] 发生错误: {str(e)}")

if __name__ == "__main__":
    main()
