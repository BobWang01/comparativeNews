import sys
import math

def progress(fas, frss):  # （文件的总大小，接收的文件大小）
    wight = 50  # 控制进度条的总长度
    t = frss / fas  # 计算接收文件的大小与文件总大小之间的百分比
    wt = int(math.ceil(wight * t))  # 通过百分比来控制#号的个数
    tb = math.ceil(t * 100)  # 接收文件百分比
    r = '  %d' % tb + '%\t' + '[' + '=' * wt + ' ' * (wight - wt) + ']' + '\r'  # 定义输出的内容格式
    sys.stdout.write(r)  # 标准输出
    sys.stdout.flush()  # 强制刷新