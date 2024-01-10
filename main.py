import pygame, random  # 导入pygame模块和random模块
from pygame.locals import *  # 导入pygame的常量


class Brick():  # 定义一个Brick类，表示游戏中的单个方块
    def __init__(self, p_position, p_color):  # 定义初始化方法，接受位置和颜色作为参数
        self.position = p_position  # 保存位置属性
        self.image = pygame.Surface([brick_width, brick_height])  # 创建一个Surface对象，表示方块的图像
        self.image.fill(p_color)  # 填充方块的颜色

    def draw(self):  # 定义绘制方法，将方块绘制到屏幕上
        screen.blit(self.image, (
            self.position[0] * brick_width, self.position[1] * brick_height))  # 使用screen的blit方法，根据方块的位置和大小，将方块的图像绘制到屏幕上


class Block():  # 定义一个Block类，表示游戏中的一个组合方块
    def __init__(self, p_bricks_layout, p_color):  # 定义初始化方法，接受方块的布局和颜色作为参数
        self.bricks_layout = p_bricks_layout  # 保存方块的布局属性，是一个元组，每个元素是一个元组，表示方块的不同方向的形状
        self.direction = random.randint(0, len(self.bricks_layout) - 1)  # 随机选择一个方向作为初始方向
        self.cur_layout = self.bricks_layout[self.direction]  # 根据方向选择当前的布局
        self.position = cur_block_init_position  # 设置方块的初始位置
        self.stopped = False  # 设置方块的停止状态为False
        self.move_interval = 800  # 设置方块的移动间隔为800毫秒
        self.bricks = [Brick((self.position[0] + x, self.position[1] + y), p_color) for (x, y) in
                       self.cur_layout]  # 根据当前的布局和颜色，创建一个列表，存储组成方块的Brick对象

    def setPosition(self, position):  # 定义设置位置的方法，接受一个位置作为参数
        self.position = position  # 更新方块的位置属性
        self.refresh_bircks()  # 调用刷新方块的方法，更新方块中每个Brick的位置

    def draw(self):  # 定义绘制方法，将方块绘制到屏幕上
        for brick in self.bricks:  # 遍历方块中的每个Brick对象
            brick.draw()  # 调用Brick的绘制方法，将Brick绘制到屏幕上

    def isLegal(self, layout, position):  # 定义判断是否合法的方法，接受一个布局和一个位置作为参数
        (x0, y0) = position  # 解包位置，得到横纵坐标
        for (x, y) in layout:  # 遍历布局中的每个元素，表示方块中每个Brick的相对位置
            if x + x0 < 0 or y + y0 < 0 or x + x0 >= field_width or y + y0 >= field_height or field_map[y + y0][x + x0] != 0:  # 判断方块中的Brick是否超出游戏区域的边界，或者是否与已经存在的Brick重叠，如果是，返回False
                return False
        return True  # 如果没有不合法的情况，返回True

    def move(self, dx, dy):  # 定义移动方法，接受横纵方向的位移作为参数
        new_position = (self.position[0] + dx, self.position[1] + dy)  # 计算移动后的新位置
        if self.isLegal(self.cur_layout, new_position):  # 判断新位置是否合法
            self.position = new_position  # 如果合法，更新方块的位置属性
            self.refresh_bircks()  # 调用刷新方块的方法，更新方块中每个Brick的位置

    def left(self):  # 定义向左移动的方法
        self.move(-1, 0)  # 调用移动方法，横向位移为-1，纵向位移为0

    def right(self):  # 定义向右移动的方法
        self.move(1, 0)  # 调用移动方法，横向位移为1，纵向位移为0

    def down(self):  # 定义向下移动的方法
        (x, y) = (self.position[0], self.position[1] + 1)  # 计算向下移动一格后的位置
        while self.isLegal(self.cur_layout, (x, y)):  # 判断这个位置是否合法，如果是，继续向下移动，直到不合法为止
            self.position = (x, y)  # 更新方块的位置属性
            self.refresh_bircks()  # 调用刷新方块的方法，更新方块中每个Brick的位置
            y += 1  # 纵坐标加1，继续向下移动

    def refresh_bircks(self):  # 定义刷新方块的方法，更新方块中每个Brick的位置
        for (brick, (x, y)) in zip(self.bricks, self.cur_layout):  # 使用zip函数，同时遍历方块中的每个Brick对象和当前的布局
            brick.position = (self.position[0] + x, self.position[1] + y)  # 根据方块的位置和布局中的相对位置，更新Brick的位置属性

    def stop(self):  # 定义停止方法，当方块触底或者碰到其他方块时，停止方块的移动，并将方块中的Brick添加到游戏区域中
        global field_bricks, score  # 声明全局变量，表示游戏区域中的Brick列表和分数
        self.stopped = True  # 设置方块的停止状态为True
        ys = []  # 创建一个空列表，用来存储方块中的Brick的纵坐标
        for brick in self.bricks:  # 遍历方块中的每个Brick对象
            field_bricks.append(brick)  # 将Brick添加到游戏区域中的Brick列表中
            (x, y) = brick.position  # 解包Brick的位置，得到横纵坐标
            if y not in ys:  # 如果纵坐标不在列表中
                ys.append(y)  # 将纵坐标添加到列表中
            field_map[y][x] = 1  # 在游戏区域的地图中，将Brick所在的位置标记为1，表示已经被占用
        eliminate_count = 0  # 创建一个变量，用来记录消除的行数
        ys.sort()  # 对列表进行排序，从小到大
        for y in ys:  # 遍历列表中的每个纵坐标
            if 0 in field_map[y]:  # 如果这一行中有0，表示没有被完全填满，跳过这一行
                continue
            eliminate_count += 1  # 如果这一行中没有0，表示被完全填满，消除计数加1
            for fy in range(y, 0, -1):  # 从这一行开始，向上遍历
                field_map[fy] = field_map[fy - 1][:]  # 将上一行的地图复制到这一行，相当于将上面的方块下移一行
            field_map[0] = [0 for i in range(field_width)]  # 将最上面的一行的地图清零，相当于空出一行
            field_bricks = [fb for fb in field_bricks if fb.position[1] != y]  # 从游戏区域中的Brick列表中，删除这一行的所有Brick
            for fb in field_bricks:  # 遍历游戏区域中的剩余的Brick
                if fb.position[1] < y:  # 如果Brick的纵坐标小于消除的行数，表示在消除的行数的上面
                    fb.position = (fb.position[0], fb.position[1] + 1)  # 将Brick的纵坐标加1，相当于下移一行
        score += [0, 1, 2, 4, 6][eliminate_count]  # 根据消除的行数，更新分数，消除一行得1分，消除两行得2分，消除三行得4分，消除四行得6分

    def update(self, time):  # 定义更新方法，接受当前的时间作为参数
        global last_move  # 声明全局变量，表示上一次移动的时间
        self.draw()  # 调用绘制方法，将方块绘制到屏幕上
        if last_move == -1 or time - last_move >= self.move_interval:  # 如果是第一次移动，或者距离上一次移动的时间超过了移动间隔
            new_position = (self.position[0], self.position[1] + 1)  # 计算向下移动一格后的新位置
            if self.isLegal(self.cur_layout, new_position):  # 判断新位置是否合法
                self.position = new_position  # 如果合法，更新方块的位置属性
                self.refresh_bircks()  # 调用刷新方块的方法，更新方块中每个Brick的位置
                last_move = time  # 更新上一次移动的时间为当前时间
            else:  # 如果不合法，表示方块触底或者碰到其他方块
                self.stop()  # 调用停止方法，停止方块的移动，并将方块中的Brick添加到游戏区域中

    def rotate(self):  # 定义旋转方法，让方块在不同的方向之间切换
        new_direction = (self.direction + 1) % len(self.bricks_layout)  # 计算旋转后的新方向，使用取余运算，保证方向在0到布局长度之间循环
        new_layout = self.bricks_layout[new_direction]  # 根据新方向，选择新的布局
        if self.isLegal(new_layout, self.position):  # 判断新的布局是否合法
            self.direction = new_direction  # 如果合法，更新方块的方向属性
            self.cur_layout = new_layout  # 更新方块的当前布局属性
            self.refresh_bircks()  # 调用刷新方块的方法，更新方块中每个Brick的位置


def drawField():  # 定义绘制游戏区域的方法，将游戏区域中的所有Brick绘制到屏幕上
    for brick in field_bricks:  # 遍历游戏区域中的每个Brick对象
        brick.draw()  # 调用Brick的绘制方法，将Brick绘制到屏幕上


def drawInfoPanel():  # 定义绘制信息面板的方法，显示分数和下一个方块
    font = pygame.font.SysFont('华文仿宋', 18)  # 使用系统字体 华文仿宋，大小为 18，创建一个字体对象
    survivedtext = font.render('得分：' + str(score), True, (255, 255, 255),
                               (0, 0, 0))  # 使用字体对象的render方法，创建一个Surface对象，表示分数的文本，指定文本内容，颜色，抗锯齿选项，和背景颜色
    textRect = pygame.Rect((field_width + 2) * brick_width, 10, survivedtext.get_width(),
                           survivedtext.get_height())  # 使用pygame.Rect方法，创建一个和文本大小相同，位置为屏幕右上角的Rect对象
    screen.blit(survivedtext, textRect)  # 使用screen的blit方法，根据Rect对象的位置，将文本的Surface对象绘制到屏幕上
    next_block.draw()  # 调用下一个方块的绘制方法，将下一个方块绘制到屏幕上


def drawFrame():  # 定义绘制边框的方法，将游戏区域和显示下一个方块的区域的边框绘制到屏幕上
    frame_color = pygame.Color(200, 200, 200)  # 创建一个颜色对象，表示边框的颜色
    pygame.draw.line(screen, frame_color, (field_width * brick_width, field_height * brick_height),
                     (field_width * brick_width, 0), 3)  # 使用pygame的draw模块的line方法，绘制一条直线，指定屏幕对象，颜色对象，起点坐标，终点坐标，和线宽


def getBlock():  # 定义获取一个方块的方法，随机生成一个方块对象，并返回
    block_type = random.randint(0, 6)  # 随机选择一个方块的类型，从0到6
    return Block(bricks_layouts[block_type],
                 colors_for_bricks[block_type])  # 根据方块的类型，从布局列表和颜色列表中选择对应的元素，创建一个Block对象，并返回


bricks_layouts = (  # 定义一个元组，存储所有方块的布局，每个元素是一个元组，表示一个方块的布局，每个元素是一个元组，表示方块的不同方向的形状，每个元素是一个元组，表示方块中每个Brick的相对位置
    (((0, 0), (0, 1), (0, 2), (0, 3)), ((0, 1), (1, 1), (2, 1), (3, 1))),
    (((1, 0), (2, 0), (1, 1), (2, 1)),),
    (((1, 0), (0, 1), (1, 1), (2, 1)), ((0, 1), (1, 0), (1, 1), (1, 2)), ((1, 2), (0, 1), (1, 1), (2, 1)),
     ((2, 1), (1, 0), (1, 1), (1, 2))),
    (((0, 1), (1, 1), (1, 0), (2, 0)), ((0, 0), (0, 1), (1, 1), (1, 2))),
    (((0, 0), (1, 0), (1, 1), (2, 1)), ((1, 0), (1, 1), (0, 1), (0, 2))),
    (((0, 0), (1, 0), (1, 1), (1, 2)), ((0, 2), (0, 1), (1, 1), (2, 1)), ((1, 0), (1, 1), (1, 2), (2, 2)),
     ((2, 0), (2, 1), (1, 1), (0, 1))),
    (((2, 0), (1, 0), (1, 1), (1, 2)), ((0, 0), (0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (1, 1), (1, 0)),
     ((2, 2), (2, 1), (1, 1), (0, 1))),
)
colors_for_bricks = (  # 定义一个元组，存储所有方块的颜色，每个元素是一个颜色对象，表示一个方块的颜色
    pygame.Color(255, 0, 0),  # 红
    pygame.Color(255, 97, 0),  # 橙
    pygame.Color(255, 255, 0),  # 黄
    pygame.Color(0, 255, 0),  # 绿
    pygame.Color(0, 255, 255),  # 青
    pygame.Color(0, 0, 255),  # 蓝
    pygame.Color(160, 32, 240),  # 紫
    pygame.Color(255, 255, 255),  # 白
    pygame.Color(100, 100, 100), pygame.Color(120, 200, 0), pygame.Color(100, 0, 200), pygame.Color(10, 100, 30)
)
field_width, field_height = 12, 17  # 定义两个常量，表示游戏区域的宽度和高度，单位是方块的个数
cur_block_init_position = (4, 0)  # 定义一个常量，表示当前方块的初始位置，是一个元组，表示横纵坐标
info_panel_width = 8  # 定义一个常量，表示信息面板的宽度，单位是方块的个数
next_block_init_position = (field_width + 3, 5)  # 定义一个常量，表示下一个方块的初始位置，是一个元组，表示横纵坐标
field_map = [[0 for i in range(field_width)] for i in range(field_height)]  # 定义一个列表，表示游戏区域的地图，是一个二维列表，每个元素是0或1，表示这个位置是否被占用
game_over_img = pygame.image.load("game_over.gif")  # 使用pygame的image模块的load方法，加载一个图片文件，创建一个Surface对象，表示游戏结束时的图片
running = True  # 定义一个变量，表示游戏是否运行中
score = 0  # 定义一个变量，表示游戏的分数
brick_width, brick_height = 30, 30  # 定义两个常量，表示每个方块的宽度和高度，单位是像素
field_bricks = []  # 定义一个列表，表示游戏区域中的所有Brick对象
next_block = None  # 定义一个变量，表示下一个方块，初始值为None
last_move = -1  # 定义一个变量，表示上一次移动的时间，初始值为-1
pygame.init()  # 调用pygame的init方法，初始化pygame模块

screen = pygame.display.set_mode(((field_width + info_panel_width) * brick_width, field_height * brick_height), 0,32)  # 调用pygame的display模块的set_mode方法，创建一个Surface对象，表示屏幕，指定屏幕的宽度和高度，单位是像素，以及其他选项

pygame.display.set_caption('俄罗斯方块')  # 调用pygame的display模块的set_caption方法，设置屏幕的标题
while running:  # 使用一个while循环，表示游戏的主循环
    if next_block == None:  # 如果下一个方块是None，表示是游戏开始
        cur_block = getBlock()  # 调用getBlock方法，获取一个随机的方块对象，赋值给当前方块
    else:  # 如果下一个方块不是None，表示是游戏进行中
        cur_block = next_block  # 将下一个方块赋值给当前方块
        cur_block.setPosition(cur_block_init_position)  # 调用当前方块的setPosition方法，设置当前方块的位置为初始位置
    next_block = getBlock()  # 调用getBlock方法，获取一个随机的方块对象，赋值给下一个方块
    next_block.setPosition(next_block_init_position)  # 调用下一个方块的setPosition方法，设置下一个方块的位置为初始位置
    if not cur_block.isLegal(cur_block.cur_layout, cur_block.position):  # 判断当前方块的布局和位置是否合法，如果不合法，表示游戏结束
        cur_block.draw()  # 调用当前方块的绘制方法，将当前方块绘制到屏幕上
        running = False  # 设置游戏的运行状态为False，跳出主循环
        continue  # 跳过本次循环的剩余部分，进入下一次循环
    while not cur_block.stopped:  # 使用一个while循环，表示当前方块的移动循环
        screen.fill(0)  # 调用屏幕的fill方法，用黑色填充屏幕，相当于清空屏幕
        drawFrame()  # 调用绘制边框的方法，将游戏区域和显示下一个方块的区域的边框绘制到屏幕上
        time = pygame.time.get_ticks()  # 调用pygame的time模块的get_ticks方法，获取当前的时间，单位是毫秒
        cur_block.update(time)  # 调用当前方块的更新方法，根据当前的时间，更新当前方块的位置和状态
        drawField()  # 调用绘制游戏区域的方法，将游戏区域中的所有Brick绘制到屏幕上
        drawInfoPanel()  # 调用绘制信息面板的方法，显示分数和下一个方块
        pygame.display.flip()  # 调用pygame的display模块的flip方法，更新整个屏幕
        pygame.display.update()  # 调用pygame的display模块的update方法，更新屏幕的变化部分
        for event in pygame.event.get():  # 使用一个for循环，遍历pygame的event模块的get方法返回的事件列表，处理用户的输入事件
            if event.type == pygame.QUIT:  # 如果事件的类型是pygame.QUIT，表示用户点击了关闭按钮
                pygame.quit()  # 调用pygame的quit方法，退出pygame模块
                exit(0)  # 调用exit函数，退出程序
            if event.type == pygame.KEYDOWN:  # 如果事件的类型是pygame.KEYDOWN，表示用户按下了一个键
                if event.key == K_w or event.key == K_UP:  # 如果按下的键是W或者上箭头，表示用户想要旋转方块
                    cur_block.rotate()  # 调用当前方块的旋转方法，让方块在不同的方向之间切换
                    last_move = time  # 更新上一次移动的时间为当前时间
                elif event.key == K_a or event.key == K_LEFT:  # 如果按下的键是A或者左箭头，表示用户想要向左移动方块
                    cur_block.left()  # 调用当前方块的向左移动的方法，让方块向左移动一格
                elif event.key == K_d or event.key == K_RIGHT:  # 如果按下的键是D或者右箭头，表示用户想要向右移动方块
                    cur_block.right()  # 调用当前方块的向右移动的方法，让方块向右移动一格
                elif event.key == K_s or event.key == K_DOWN:  # 如果按下的键是S或者下箭头，表示用户想要向下移动方块
                    cur_block.down()  # 调用当前方块的向下移动的方法，让方块快速下落到底部
                    last_move = time - 500  # 更新上一次移动的时间为当前时间减去500毫秒，相当于缩短下一次移动的间隔
screen.blit(game_over_img, (
    field_width / 2 * brick_width, (field_height / 2 - 2) * brick_height))  # 调用屏幕的blit方法，根据游戏区域的中心位置，将游戏结束的图片绘制到屏幕上
while True:  # 使用一个while循环，表示游戏结束后的循环
    for event in pygame.event.get():  # 使用一个for循环，遍历pygame的event模块的get方法返回的事件列表，处理用户的输入事件
        if event.type == pygame.QUIT:  # 如果事件的类型是pygame.QUIT，表示用户点击了关闭按钮
            pygame.quit()  # 调用pygame的quit方法，退出pygame模块
            exit(0)  # 调用exit函数，退出程序
    pygame.display.flip()  # 调用pygame的display模块的flip方法，更新整个屏幕
    pygame.display.update()  # 调用pygame的display模块的update方法，更新屏幕的变化部分
