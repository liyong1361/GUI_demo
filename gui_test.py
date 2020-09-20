import tkinter
from tkinter import ttk
import math, time
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import numpy as np

root = tkinter.Tk()
root.wm_title("Angle detection demo")

# 创建下拉菜单
cmb = ttk.Combobox(root)
cmb.pack()
# 设置下拉菜单中的值
cmb['value'] = ('VL53L1', 'VL53L5')
# 设置默认值，即默认下拉框中的内容
cmb.current(1)

# 执行函数
def func(event):
    var.set(cmb.get()+ '  selected' + "\n")


cmb.bind("<<ComboboxSelected>>",func)
var = tkinter.StringVar()  # 将label标签的内容设置为字符类型，用var来接收hit_me函数的传出内容用以显示在标签上
b1 = tkinter.Canvas(root, bg='white', height=300, width=800)
b1.pack()
fig = Figure(figsize=(4, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

l = tkinter.Label(root, textvariable=var, bg='green', fg='white', font=('Arial', 12), width=30, height=2)
var.set('click start to measure the angle')
# 说明： bg为背景，fg为字体颜色，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
l.pack()

def draw_angle(Angle_detected, Angle_detected2):
    line_center = b1.create_line(400, 0, 400, 400, fill='red', width=5)
    line_v1 = b1.create_line(200, 0, 200, 300)
    line_h1 = b1.create_line(0, 150, 400-10, 150)

#左坐标中心点(200, 150), 右边坐标中心点（600，150）

    b1.create_arc(200-50, 150-50, 200+50, 150+50, start=180, extent=Angle_detected, activedash=True)
    line_x1 = b1.create_line(200, 150, 200+200, 150 - 200*math.tan(Angle_detected*math.pi/180), width=1)
    line_x1 = b1.create_line(200, 150, 200-200, 150 + 200*math.tan(Angle_detected*math.pi/180), width=1)
    b1.create_text(200 - 50, 150 - 50, text= str(Angle_detected) + ' degree', font=('Times',15))
    #左边与斜线相交的点坐标
    temp_y1 = 150 * math.tan(22*math.pi/180) / (math.tan(22*math.pi/180) + math.tan((90-Angle_detected)*math.pi/180))
    temp_x1 = temp_y1 * math.tan((90-Angle_detected)* math.pi/180)
    #右边与斜线相交的点坐标
    temp_y2 = 150 * math.tan(22*math.pi/180) * math.tan(Angle_detected*math.pi/180)/(1-math.tan(Angle_detected*math.pi/180)
                                                                                     *math.tan(22*math.pi/180))
    temp_x2 = temp_y2 / math.tan(Angle_detected*math.pi/180)

    points = [
        200 - temp_x1, 150 + temp_y1,
        200 + temp_x2, 150 - temp_y2,
        200, 300,
    ]
    # 根据点来连线
    b1.create_polygon(
        points,
        outline="red",  # 线的颜色
        fill=''  # 填充色
    )

    #Angle_detected2 = 20
    line_v2 = b1.create_line(600, 0, 600, 300)
    line_h2 = b1.create_line(400+10, 150, 800, 150)
    b1.create_arc(600-50, 150-50, 600+50, 150+50, start=180, extent=Angle_detected2, activedash=True)
    line_x2 = b1.create_line(600, 150, 600+200, 150 - 200*math.tan(Angle_detected2*math.pi/180), width=1)
    line_x2 = b1.create_line(600, 150, 600-200, 150 + 200*math.tan(Angle_detected2*math.pi/180), width=1)
    b1.create_text(600 - 50, 150 - 50, text= str(Angle_detected2) + ' degree', font=('Times',15))
    #左边与斜线相交的点坐标
    temp_y3 = 150 * math.tan(22*math.pi/180) / (math.tan(22*math.pi/180) + math.tan((90-Angle_detected2)*math.pi/180))
    temp_x3 = temp_y3 * math.tan((90-Angle_detected2) * math.pi/180)
    #右边与斜线相交的点坐标
    temp_y4 = 150 * math.tan(22*math.pi/180) * math.tan(Angle_detected2*math.pi/180)/(1-math.tan(Angle_detected2*math.pi/180)
                                                                                     *math.tan(22*math.pi/180))
    temp_x4 = temp_y4 / math.tan(Angle_detected2*math.pi/180)
    points2 = [
        600 - temp_x3, 150 + temp_y3,
        600 + temp_x4, 150 - temp_y4,
        600, 300,
    ]
    # 根据点来连线
    b1.create_polygon(
        points2,
        outline="red",  # 线的颜色
        fill=''  # 填充色
    )
    b1.pack()


def draw_heatmap(m):
    ax = fig.add_subplot(111)
    ax.matshow(m)
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            ax.text(x=j, y=i, s=m[i, j], verticalalignment='center',horizontalalignment='center')
    canvas.draw()


def get_data_and_draw():
    time.sleep(3)
    global fig, canvas, b1
    b1.delete('all')
    fig.clear()
    a = - np.random.randint(60)
    b = - np.random.randint(60)
    draw_angle(Angle_detected=a, Angle_detected2=b)
    t = np.random.randint(3000,size=16)
    m = t.reshape((4, 4))
    draw_heatmap(m)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent


def set_chart():
    var.set('measured results shown')


frm_1 = tkinter.Frame(master=root)
button = tkinter.Button(master=frm_1, text="Start", command=lambda: [set_chart(), get_data_and_draw()])
button.pack(side=tkinter.LEFT)

button = tkinter.Button(master=frm_1, text="Quit", command=_quit)
button.pack(side=tkinter.BOTTOM)
frm_1.pack(side=tkinter.BOTTOM)

tkinter.mainloop()
# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.