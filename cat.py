import os
import time

# 猫与爱心的帧列表
frames = [
    r"""
     /\_/\  
    ( o.o ) 
     > ^ <   ♥ ♥ ♥
    """,
    r"""
      /\_/\  
     ( o.o )  
      > ^ <  ♥ ♥
    """,
    r"""
       /\_/\  
      ( o.o )  
       > ^ < ♥
    """,
    r"""
     /\_/\  
    ( o.o ) 
     > ^ <   ♥ ♥ ♥
    """,
    r"""
      /\_/\  
     ( o.o )  
      > ^ <  ♥ ♥
    """,
    r"""
       /\_/\  
      ( o.o )  
       > ^ < ♥
    """,
    r"""
      /\_/\  
     ( o.o ) 
      > ^ <  ♥
    """,
    r"""
     /\_/\  
    ( o.o ) 
     > ^ <   ♥ ♥
    """,
    r"""
    /\_/\  
   ( o.o )  
    > ^ <  ♥ ♥ ♥
    """,
]

# 猫猫我爱你的艺术字
art_text = r"""
  猫猫我爱你
   /\_/\  
  ( o.o ) 
   > ^ < 
"""

def clear_screen():
    # 清除终端屏幕
    os.system('cls' if os.name == 'nt' else 'clear')

def display_animation(duration=5):
    start_time = time.time()
    while True:
        # 播放动画直到超过指定的持续时间（如5秒）
        for frame in frames:
            clear_screen()
            print(frame)
            time.sleep(0.3)  # 控制帧之间的时间间隔
            if time.time() - start_time > duration:
                return  # 动画持续5秒后退出

if __name__ == "__main__":
    try:
        display_animation(5)  # 播放5秒的动画
        clear_screen()
        print(art_text)  # 动画结束后，打印艺术字
    except KeyboardInterrupt:
        clear_screen()
        print("动画已停止。")
