from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import numpy as np

class GoogleSearch:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36'
        ]
        self._configure_browser()

    def _configure_browser(self):
        """配置浏览器选项"""
        self.options.add_argument(f'--user-agent={random.choice(self.user_agents)}')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        # 添加随机窗口大小
        window_sizes = [(1366, 768), (1920, 1080), (1440, 900), (1600, 900)]
        window_size = random.choice(window_sizes)
        self.options.add_argument(f'--window-size={window_size[0]},{window_size[1]}')

    def generate_human_like_mouse_path(self, start_point, end_point, points=10):
        """生成类似人类的鼠标移动路径"""
        path = []
        x_dist = end_point[0] - start_point[0]
        y_dist = end_point[1] - start_point[1]
        
        # 生成贝塞尔曲线控制点
        control_point_1 = (
            start_point[0] + x_dist * 0.3 + random.randint(-100, 100),
            start_point[1] + y_dist * 0.3 + random.randint(-100, 100)
        )
        control_point_2 = (
            start_point[0] + x_dist * 0.7 + random.randint(-100, 100),
            start_point[1] + y_dist * 0.7 + random.randint(-100, 100)
        )
        
        # 使用贝塞尔曲线生成路径点
        t_points = np.linspace(0, 1, points)
        for t in t_points:
            # 三次贝塞尔曲线公式
            x = (1-t)**3 * start_point[0] + 3*(1-t)**2 * t * control_point_1[0] + \
                3*(1-t) * t**2 * control_point_2[0] + t**3 * end_point[0]
            y = (1-t)**3 * start_point[1] + 3*(1-t)**2 * t * control_point_1[1] + \
                3*(1-t) * t**2 * control_point_2[1] + t**3 * end_point[1]
            path.append((int(x), int(y)))
        return path

    def human_like_mouse_move(self, driver, element=None):
        """执行人性化的鼠标移动"""
        actions = ActionChains(driver)
        current_pos = (0, 0)
        
        if element:
            element_pos = element.location
            element_size = element.size
            target_pos = (
                element_pos['x'] + element_size['width']//2,
                element_pos['y'] + element_size['height']//2
            )
            
            # 生成路径并执行移动
            path = self.generate_human_like_mouse_path(current_pos, target_pos)
            for point in path:
                actions.move_by_offset(point[0] - current_pos[0], 
                                     point[1] - current_pos[1])
                current_pos = point
                actions.pause(random.uniform(0.001, 0.003))
            
        actions.perform()

    def human_like_typing(self, element, text):
        """模拟人类输入行为"""
        # 常见的输入模式
        typing_patterns = [
            (0.01, 0.03),  # 快速输入
            (0.03, 0.06),  # 中等速度
            (0.06, 0.1)    # 较慢输入
        ]
        pattern = random.choice(typing_patterns)
        
        for char in text:
            element.send_keys(char)
            # 某些字符后添加略微longer的停顿
            if char in [' ', ',', '.', '!', '?']:
                time.sleep(random.uniform(0.05, 0.15))
            else:
                time.sleep(random.uniform(*pattern))

    def random_scroll(self, driver):
        """执行随机滚动"""
        scroll_pause_time = random.uniform(0.2, 0.5)
        # 获取页面高度
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        # 随机滚动3-5次
        for _ in range(random.randint(3, 5)):
            # 随机滚动距离
            scroll_distance = random.randint(100, 400)
            driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
            time.sleep(scroll_pause_time)

    def search(self, query, num_results=5):
        driver = None
        try:
            driver = webdriver.Chrome(options=self.options)
            driver.get('https://www.google.com')
            
            # 等待并找到搜索框
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            
            # 人性化鼠标移动到搜索框
            self.human_like_mouse_move(driver, search_box)
            
            # 模拟人类输入
            self.human_like_typing(search_box, query)
            time.sleep(random.uniform(0.2, 0.4))
            search_box.send_keys(Keys.RETURN)
            
            # 等待结果加载
            search_results = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.g"))
            )
            
            # 随机滚动
            self.random_scroll(driver)
            
            print(f"\n搜索关键词: {query}")
            print("-" * 50)
            
            for i, result in enumerate(search_results[:num_results], 1):
                try:
                    # 移动到结果元素
                    self.human_like_mouse_move(driver, result)
                    
                    title_element = result.find_element(By.CSS_SELECTOR, "h3")
                    link_element = result.find_element(By.CSS_SELECTOR, "a")
                    
                    try:
                        snippet_element = result.find_element(By.CSS_SELECTOR, "div.VwiC3b")
                        snippet = snippet_element.text
                    except:
                        snippet = "无摘要"
                    
                    print(f"\n{i}. 标题: {title_element.text}")
                    print(f"   链接: {link_element.get_attribute('href')}")
                    print(f"   摘要: {snippet}")
                    print("-" * 50)
                    
                    time.sleep(random.uniform(0.2, 0.4))
                    
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"搜索出错: {str(e)}")
            
        finally:
            if driver:
                driver.quit()

def main():
    searcher = GoogleSearch()
    while True:
        query = input("\n请输入搜索关键词 (输入 'q' 退出): ")
        if query.lower() == 'q':
            break
        searcher.search(query)

if __name__ == "__main__":
    main()
