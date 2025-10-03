# snake_pygame.py  —— 独立窗口版贪吃蛇
import pygame
import random
import sys


# ========== 游戏参数 ==========
CELL  = 20          # 格子大小（像素）
W, H  = 30, 20      # 地图格子数
WIDTH = CELL * W
HEIGHT= CELL * H

SNAKE = [(W-10, H-5)]  # 蛇身列表，头在[0]
FOOD1    = (3,3)
DX,DY =(1,0)
NEW_DX ,NEW_DY = (1,0)
SCORE  = 0
STAND_STILL = False
LAST_REAL_DX, LAST_REAL_DY = 1, 0
TOP_FILE = 'top.txt'      # 排行榜文件，在doucument中
N=5
LAST_KEY=None
RUNNING=True

# ========== Pygame 初始化,重要的是定义了pygame中的一些全局变量 ==========
pygame.init()                                       #初始化pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))   #创建300*400的窗口
pygame.display.set_caption("贪吃蛇")
clock  = pygame.time.Clock()
font   = pygame.font.SysFont(None, 24)     # 1. 创建字体对象：使用系统默认字体，字号 24

# ========== 工具函数 ==========
def load_top():
    """返回[int] 降序排列的前N名"""
    try:                                #尝试
        with open(TOP_FILE) as f:       #尝试将TOP_FILE文件作为f打开
            top = [int(line.strip()) for line in f if line.strip()] #如果非空，那就一行一行读，读了之后去掉头尾空格制表符，将剩余的内容转成整数型
                                                                    #strip就是去掉前后空格，制表符等
    except FileNotFoundError:           #FileNotFoundError这是python抛出的一种错误类型
        top = []
    return sorted(top, reverse=True)[:N]           #返回降序排列的top列表，只取前N个
                                                    #第一句看成是将所有降序，第二句是切片
#将TOP_FILE中的排名全部提出来，按照降序排列，并取出前N个
def save_top(score):
    """把新分数插进榜，保持降序，只留前N"""
    top = load_top()
    top.append(score)   #将新分数插入top列表
    top = sorted(top, reverse=True)[:N]     #将top列表降序同时取出前N个
    with open(TOP_FILE, 'w') as f:          #将TOP_FILE文件以覆盖模式打开
        for s in top:                   #这里top把内容附给s
            f.write(str(s)+'\n')        #把变量s通过字符串的方式写入f

def draw_rect(color, pos):
    pygame.draw.rect(screen, color, (pos[0]*CELL, pos[1]*CELL, CELL, CELL))
#颜色函数，利用这个函数可以快速编辑色块颜色，位置
def show():
    # ===== 原来的画图 =====
    screen.fill((30, 50, 30))#接近黑色的背景
    for x, y in SNAKE:
        draw_rect((0, 200, 0), (x, y))   # 身体
    draw_rect((0, 255, 0), SNAKE[0])     # 头更亮
    draw_rect((255, 50, 50), FOOD1)       # 食物
    # ===== 排行榜 =====
    top = load_top()
    font = pygame.font.SysFont(None, 22)
    header = font.render("TOP", True, (255,255,0))
    screen.blit(header, (WIDTH - 80, 5))
    for i, s in enumerate(top, 1):
        txt = font.render(f"{i}. {s}", True, (255,255,255))
        screen.blit(txt, (WIDTH - 80, 25 + i*20))
    # ===== 分数 =====
    txt = font.render(f'Score: {SCORE}', True, (255, 255, 255))     # 2. 把文字生成一张图片（抗锯齿，白色）
                                                                                    #参数：文字内容，是否平滑（True），颜色(RGB)
    screen.blit(txt, (5, 5))    # 把这张图片“贴”到窗口的 (5,5) 像素位置
    pygame.display.flip()           # 把前面所有绘制操作一次性显示到屏幕上
#画图，同时将排行榜和分数显示
def move():
    global FOOD1, SCORE, DX, DY
    x, y = SNAKE[0]
    nx, ny = x + DX, y + DY
    if nx < 0 or nx >= W or ny < 0 or ny >= H or (nx, ny) in SNAKE:
        return False
    SNAKE.insert(0, (nx, ny))
    if (nx, ny) == FOOD1:
        SCORE += 1
        food1 = random.randint(1, W-2)
        food2 = random.randint(1, H-2)
        while (food1, food2) in SNAKE:
            food1=random.randint(1, W-2)
            food2=random.randint(1, H-2)
        FOOD1 = (food1, food2)
    else:
        SNAKE.pop()
    return True
#用DX,DY去使得蛇往前走，撞墙和撞食物检测，重新生成食物
def read():
    global LAST_KEY,NEW_DX,NEW_DY,RUNNING
    for event in pygame.event.get():        # 遍历这一帧里所有用户事件（按键、鼠标、关闭窗口等）
        if event.type == pygame.QUIT:
            RUNNING = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                LAST_KEY = event.key
            elif event.key == pygame.K_ESCAPE:
                RUNNING = False
    if LAST_KEY == pygame.K_LEFT:
        NEW_DX, NEW_DY = -1,0
    elif LAST_KEY == pygame.K_RIGHT:
        NEW_DX, NEW_DY = 1,0
    elif LAST_KEY == pygame.K_UP:
        NEW_DX, NEW_DY = 0,-1
    elif LAST_KEY == pygame.K_DOWN:
        NEW_DX, NEW_DY = 0,1
    return NEW_DX, NEW_DY
#重新读取下一帧的方向键并存入NEW_DX,NEW_DY
def turn():
    global DX,DY,NEW_DX,NEW_DY
    if (NEW_DX, NEW_DY) != (-DX, -DY):
        DX, DY = NEW_DX, NEW_DY
#将合法的NEW_DX,NEW_DY赋值给DX,DY用于转向
# ========== 主循环 ==========
show()
RUNNING = True
while RUNNING:
    clock.tick(SCORE+3)          # 速度越来越快
    read()
    turn()
    if not move():
        save_top(SCORE)
        print("Game Over! Score:", SCORE)
        RUNNING = False
    show()
"""
1、狂按方向键会直接撞死？   
答：一帧内只处理第一个按键，其余按键被漏掉，但漏掉的按键仍然改变了方向，导致下一帧直接撞自己
"""
pygame.quit()
sys.exit()

