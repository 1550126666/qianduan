import time

import pygame as pygame
import cv2
from sqlalchemy.sql import text
import numpy as np
import streamlit as st
import socket
import pickle
import matplotlib.pyplot as plt
def receive_data(conn):
    message_size = int.from_bytes(conn.recv(4), byteorder='big')
    data = b""
    while len(data) < message_size:
        packet = conn.recv(message_size - len(data))
        if not packet:
            return None
        data += packet
    return pickle.loads(data)

st.set_page_config(page_title="overview", page_icon="👀")

conn = st.experimental_connection(
    "local_db",
    type="sql",
    url="mysql+pymysql://admin:123456@8.130.75.230:3306/my"
)
addr = ('localhost', 23347)
addr1 = ('localhost', 23350)

st.markdown("# 项目总览")
st.sidebar.header("Overview")
st.write(
    """在此页面你可以同时检测自身的坐姿以及查看到实时的心跳频率和呼吸频率折线图
    """
)
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
start_btime = 0
start_htime = 0
# 按钮事件
init_data = 0
init_datas = np.zeros(100)
# breathing_line = st.line_chart()
# heartbeat_line = st.line_chart()
# hb_num = st.header("动态展示呼吸频率与心跳频率的数据变化")
scol1, scol2 = st.columns(2)
with scol1:
    breathing_value = st.metric("呼吸频率", "{:.2f}".format(init_data) + " bpm")
    bline_text = st.header("呼吸频率折线图")
    breathing_line = st.line_chart(init_datas)
    bwarn = st.empty()
with scol2:
    heartbeat_value = st.metric("心跳频率", "{:.2f}".format(init_data) + " bpm")
    hline_text = st.header("心跳频率折线图")
    heartbeat_line = st.line_chart(init_datas)
    hwarn = st.empty()
breathing_data_old = 0
heartbeat_data_old = 0
loo = False
if start_button1 and not stop_button1:
    loo = True
    if stop_button1:
        loo = False

# 图像更新



if loo:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(addr)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1:
            s1.connect(addr1)
            while True:
                datas = receive_data(s)
                frame, label = datas
                frame = cv2.resize(frame, (0, 0), fx=3, fy=3)
                frame = cv2.flip(frame,1)
                print(frame.shape)
                # point = frame
                frame = np.clip(frame, 0.0, 1.0)
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
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
                if label == 'left':
                    error_name = "左后倾"
                elif label == 'right':
                    error_name = "右后倾"
                elif label == 'left_ts':
                    error_name = '左前倾'
                elif label == 'right_ts':
                    error_name = '右前倾'
                elif label == 'hunchback':
                    error_name = "前倾驼背"
                # if label == 'error':
                #     lab.metric('预测结果', last_label)
                # else:
                #     lab.metric('预测结果', label)
                if label != 'correct':
                    lab.metric('预测结果', error_name)
                else:
                    lab.metric('预测结果','坐姿正确')
                print(frame_num)
                print(label)
                if label != 'correct':
                    if label in {'left', 'right', 'hunchback', 'left_ts', 'right_ts'}:
                        if label != last_label:
                            frame_num = 1
                            last_label = label
                        else:
                            frame_num = frame_num + 1
                if frame_num >= 500:
                    error_label = label
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
                datas1 = receive_data(s1)
                breathing_data, heartbeat_data, breathing_bpm, heartbeat_bpm = datas1
                # breathing_data = np.random.rand(100)*100
                # heartbeat_data = np.random.rand(100)*100

                breathing_line.line_chart(breathing_data)
                heartbeat_line.line_chart(heartbeat_data)
                breathing_value.metric("呼吸频率", "{:.2f}".format(np.mean(breathing_data)) + " bpm",
                                       "{:.2f}".format(np.mean(breathing_data) - np.mean(breathing_data_old)) + " bpm")
                heartbeat_value.metric("心跳频率", "{:.2f}".format(np.mean(heartbeat_data)) + " bpm",
                                       "{:.2f}".format(np.mean(heartbeat_data) - np.mean(heartbeat_data_old)) + " bpm")
                breathing_value.metric("呼吸频率", "{:.2f}".format(np.mean(breathing_bpm)) + " bpm",
                                       "{:.2f}".format(
                                           np.mean(breathing_bpm) - np.mean(breathing_data_old)) + " bpm")
                heartbeat_value.metric("心跳频率", "{:.2f}".format(np.mean(heartbeat_bpm)) + " bpm",
                                       "{:.2f}".format(
                                           np.mean(heartbeat_bpm) - np.mean(heartbeat_data_old)) + " bpm")
                breathing_data_old = breathing_bpm
                heartbeat_data_old = heartbeat_bpm
                if np.mean(breathing_bpm) > 31:
                    if time.time() - start_btime > 4:
                        start_btime = time.time()
                        btimeall = time.ctime()  # 记录开始时间
                        btime = btimeall.split(' ')[3]
                        bdate = btimeall.replace(btimeall.split(' ')[3], '')
                        bwarn.warning('呼吸过快！！！', icon="⚠️")
                        with conn.session as session:
                            session.execute(text("INSERT INTO signs (time,type,date) VALUES (:btime,:mess,:date);"),
                                            {"btime": btime, "mess": '呼吸过快', "date": bdate})
                            session.commit()
                if np.mean(heartbeat_bpm) > 105:
                    if time.time() - start_btime > 4:
                        start_htime = time.time()
                        htimeall = time.ctime()  # 记录开始时间
                        htime = htimeall.split(' ')[3]
                        hdate = htimeall.replace(htimeall.split(' ')[3], '')
                        hwarn.warning('心跳太快！！！', icon="⚠️")
                        with conn.session as session:
                            session.execute(text("INSERT INTO signs (time,type,date) VALUES (:htime,:mess,:date);"),
                                            {"htime": htime, "mess": '心跳过快', "date": hdate})
                            session.commit()
                if time.time() - start_btime > 3:
                    bwarn.empty()
                if time.time() - start_htime > 3:
                    hwarn.empty()
                time.sleep(3)



