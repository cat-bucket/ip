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

def clear_screen():
    # 清除终端屏幕
    os.system('cls' if os.name == 'nt' else 'clear')

def display_animation():
    while True:
        for frame in frames:
            clear_screen()
            print(frame)
            time.sleep(0.3)  # 控制帧之间的时间间隔

if __name__ == "__main__":
    try:
        display_animation()
    except KeyboardInterrupt:
        # 用户按下 Ctrl+C 时退出
        clear_screen()
        print("动画已停止。")
