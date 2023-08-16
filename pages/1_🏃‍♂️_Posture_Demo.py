import threading
import time

import pygame as pygame
# import winsound

import cv2
from sqlalchemy.sql import text
import numpy as np
import streamlit as st
import socket
import pickle
import matplotlib.pyplot as plt


# from streamlit_modal import Modal
st.set_page_config(page_title="Plotting Demo", page_icon="📈")


# 数据库
conn = st.experimental_connection(
    "local_db",
    type="sql",
    url="mysql://admin:123456@8.130.75.230:3306/my"
)



# 接收数据
def receive_data(conn):
    message_size = int.from_bytes(conn.recv(4), byteorder='big')
    data = b""
    while len(data) < message_size:
        packet = conn.recv(message_size - len(data))
        if not packet:
            return None
        data += packet
    return pickle.loads(data)
addr = ('localhost', 23347)



# 文字内容
st.markdown("# 坐姿检测")
st.sidebar.header("Posture Demo")
st.write(
    """在此页面您可以查看到当前姿态的骨架预测图，根据骨架预测图可以观察到坐姿的变化。
    """
)
# 关节骨架图数据处理
# point = np.zeros((10, 2))
arm = [4, 3, 2, 1, 5, 6, 7]
bodyLeft = [0, 1, 8]
right = [9, 1]

# 页面布局
fig, ax = plt.subplots()
col1, col2 = st.sidebar.columns(2)
start_button1 = col1.button("开始")
stop_button1 = col2.button("停止")
col1,col2 = st.columns(2)
with col1:
    gjt = st.empty()
with col2:
    lab = st.empty()
error_warn = st.empty()
insert = st.empty()
frame_num = 0
last_label = ''
error_label = ''
error_name = ''
# 按钮事件
loo = False
if start_button1 and not stop_button1:
    loo = True
    if stop_button1:
        loo = False

# 图像更新
if loo:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(addr)
        while True:
            frame = ''
            label = ''
            datas = receive_data(s)
            frame, label = datas
            frame = cv2.resize(frame, (0, 0), fx=3, fy=3)
            print(frame.shape)
            # point = frame
            frame = np.clip(frame, 0.0, 1.0)
            gjt.image(frame)
            # time.sleep(0.1)
            # print(point)
            # 散点图
            # plt.cla()
            # ax.scatter(point[:, 0], point[:, 1], c='red', s=40.0)
            # ax.plot(point[arm, 0], point[arm, 1], c='green', lw=2.0)
            # ax.plot(point[bodyLeft, 0], point[bodyLeft, 1], c='green', lw=2.0)
            # ax.plot(point[right, 0], point[right, 1], c='green', lw=2.0)
            # ax.invert_yaxis()
            # gjt.pyplot(fig)
            if label == 'error':
                lab.metric('预测结果', last_label)
            else:
                lab.metric('预测结果', label)
            print(frame_num)
            print(last_label)
            if label != 'correct':
                if label in {'left', 'right', 'hunchback', 'left_ts', 'right_ts'}:
                    if label != last_label:
                        frame_num = 1
                        last_label = label
                    else:
                        frame_num = frame_num + 1
            if frame_num >= 500:
                error_label = label
                if label == 'left':
                    error_name = "右后倾"
                elif label == 'right':
                    error_name = "左后倾"
                elif label == 'left_ts':
                    error_name = '右前倾'
                elif label == 'right_ts':
                    error_name = '左前倾'
                elif label == 'hunchback':
                    error_name = "前倾驼背"
                time_all = time.ctime()  # 记录开始时间
                etime = time_all.split(' ')[3]
                date = time_all.replace(time_all.split(' ')[3], '')
                error_warn.warning('姿势错误！！！', icon="⚠️")
                pygame.mixer.init()  # 初始化混音器模块（pygame库的通用做法，每一个模块在使用时都要初始化pygame.init()为初始化所有的pygame模块，可以使用它也可以单初始化这一个模块）
                pygame.mixer.music.load("D:\\pythonProject\\real-time-radar-master\\tools\pages\\test1.wav")  # 加载音乐
                pygame.mixer.music.set_volume(0.5)  # 设置音量大小0~1的浮点数
                pygame.mixer.music.play()  # 播放音频
                time.sleep(5)
                with conn.session as session:
                    session.execute(text("INSERT INTO error (time,type,date) VALUES (:time,:mess,:date);"),
                                    {"time": etime, "mess": error_name, "date": date})
                    session.commit()
                error_warn.empty()
                frame_num = 1
    # 模拟数据
    # if num < 3:
    #     num = num + 1
    # else:
    #     num = 1
    # point = np.load("./data/{}".format(num) + ".npy")
    # for i in range(point.shape[0]):
    #     point[i, 0] = point[i, 0] // 10
    #     point[i, 1] = point[i, 1] // 10

    # (bokeh)一坨
    # p = figure(
    #     title='gjt',
    #     x_axis_label='x',
    #     y_axis_label='y')
    # p.scatter(point[:, 0], point[:, 1],
    #           fill_color='red',
    #           line_color=None)
    # p.line(point[arm, 0], point[arm, 1], legend_label='Trend', line_width=2)
    # p.line(point[bodyLeft, 0], point[bodyLeft, 1], legend_label='Trend', line_width=2)
    # p.line(point[right, 0], point[right, 1], legend_label='Trend', line_width=2)
    # gjt.bokeh_chart(p)
    # 创建一个空的散点图对象(plt)





