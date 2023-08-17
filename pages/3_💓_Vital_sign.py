import time
import streamlit as st
import numpy as np
from sqlalchemy.sql import text
# from bokeh.plotting import figure
import socket
import pickle
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
addr = ('localhost', 23350)

conn = st.experimental_connection(
    "local_db",
    type="sql",
    url="mysql+pymysql://admin:123456@8.130.75.230:3306/my"
)
st.markdown("# 生命体征检测")
st.sidebar.header("Vital Sign")
col5, col6 = st.sidebar.columns(2)
start_button = col5.button("开始")
stop_button = col6.button("停止")
st.write(
    """在此页面您可以查看到实时的心跳频率和呼吸频率折线图，同时当监测到当前检测人员心跳频率异常时，会发出警告，提醒心率异常。
    """
)
init_data = 0
init_datas = np.zeros(100)
# breathing_line = st.line_chart()
# heartbeat_line = st.line_chart()
hb_num = st.header("动态展示呼吸频率与心跳频率的数据变化")
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
if start_button and not stop_button:
    loo = True
    if stop_button:
        loo = False
start_btime = 0
start_htime = 0
while loo:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(addr)
        while True:
            datas = receive_data(s)
            breathing_data, heartbeat_data, breathing_bpm, heartbeat_bpm = datas
    # breathing_data = np.random.rand(100)*100
    # heartbeat_data = np.random.rand(100)*100
            breathing_line.line_chart(breathing_data)
            heartbeat_line.line_chart(heartbeat_data)

            # breathing_value.metric("呼吸频率", "{:.2f}".format(np.mean(breathing_data)) + " bpm",
            #                        "{:.2f}".format(np.mean(breathing_data) - np.mean(breathing_data_old)) + " bpm")
            # heartbeat_value.metric("心跳频率", "{:.2f}".format(np.mean(heartbeat_data)) + " bpm",
            #                        "{:.2f}".format(np.mean(heartbeat_data) - np.mean(heartbeat_data_old)) + " bpm")
            breathing_value.metric("呼吸频率", "{:.2f}".format(np.mean(breathing_bpm)) + " bpm",
                                   "{:.2f}".format(np.mean(breathing_bpm) - np.mean(breathing_data_old)) + " bpm")
            heartbeat_value.metric("心跳频率", "{:.2f}".format(np.mean(heartbeat_bpm)) + " bpm",
                                   "{:.2f}".format(np.mean(heartbeat_bpm) - np.mean(heartbeat_data_old)) + " bpm")
            breathing_data_old = breathing_bpm
            heartbeat_data_old = heartbeat_bpm
            if np.mean(breathing_bpm) > 31:
                if time.time()-start_btime > 4:
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
            if time.time()-start_btime > 3:
                bwarn.empty()
            if time.time()-start_htime > 3:
                hwarn.empty()
    # fig, ax = plt.subplots()
    # ax.plot(breathing_data)
    # ax.legend(loc='upper right')
    # breathing_line.pyplot(fig)
    #
    # fig, ax = plt.subplots()
    # ax.plot(heartbeat_data)
    # ax.legend(loc='upper right')
    # heartbeat_line.pyplot(fig)
