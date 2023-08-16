
import streamlit as st
import subprocess
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# 这是一个正经的生命体征检测和坐姿检测记录系统! 👋")

st.sidebar.success("Select a page above.")

st.markdown(
    """
    在此系统中，您将了解到自己的坐姿习惯和此时的心跳频率和呼吸频率。
    
    **👈从侧边框中选择你想要打开的页面**就能看到相应的结果展示。
    
"""
)

#
col1, col2 = st.columns(2)

with col1:
    button1 = st.button('数据获取')
    button2 = st.button('姿态预测')
    button5 = st.button('关闭进程')
with col2:
    button3 = st.button('生命体征')
    button4 = st.button('关闭雷达')
    button6 = st.button('关闭生命体征')
# col1 , col2 ,col3= st.columns(3)
# with col1:
#     button1 = st.button('数据获取')
# with col2:
#     button2 = st.button('数据处理')
# with col3:
#     button3 = st.button('关闭雷达')
# def send_data(conn, np_array):
#     data = pickle.dumps(np_array)
#     message_size = len(data)
#     print('send data')
#     conn.sendall(message_size.to_bytes(4, byteorder='big'))
#     conn.sendall(data)
# output_addr=('localhost', 23349)
if __name__ == '__main__':
    print(button1,button2,button3,button4)
    # if 'stop' not in st.session_state:
    #     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     sock.bind(output_addr)
    #     sock.listen(1)
    #     conn, addr = sock.accept()
    #     st.session_state.stop = 'a'
    if button1:
        if 'count1' not in st.session_state:
            a = subprocess.Popen(
                ['D:\\pythonProject\\real-time-radar-master\\venv\\Scripts\\python.exe', './posture/Real-time-plot-RAI_RDI_XWR1843_app.py'],stdin=subprocess.PIPE)
            st.session_state.count1 = a
        # if 'count2' not in st.session_state:
        #     b = subprocess.Popen(
        #         ['D:\\pythonProject\\real-time-radar-master\\venv\\Scripts\\python.exe', './tools/server_a.py'])
        #     st.session_state.count2 = b
    if button2:
        if 'count3' not in st.session_state:
            c = subprocess.Popen(
                ['D:\\pythonProject\\real-time-radar-master\\venv\\Scripts\\python.exe', './posture/onnx_run.py'])
            st.session_state.count3 = c
    if button3:
        if 'count4' not in st.session_state:
            d = subprocess.Popen(
                ['D:\\pythonProject\\real-time-radar-master\\venv\\Scripts\\python.exe', './vital_sign/client.py'])
            st.session_state.count4 = d
    if button4:
        stop_data = b"stop"
        if 'count1' in st.session_state:
            print('关闭雷达')
            st.session_state.count1.stdin.write(stop_data)
            st.session_state.count1.stdin.flush()
            # send_data(conn, 'stop')
            # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # sock.bind(output_addr)
            # sock.listen(1)
            # while True:
            #     conn, addr = sock.accept()
            #     while True:
            #         try:
            #             print('send')
            #             send_data(conn, 'stop')
            #         except (ConnectionResetError, BrokenPipeError):
            #             break
            #     conn.close()
    if button5:

        if 'count1' in st.session_state:
            print('关闭a')
            st.session_state.count1.kill()
            del st.session_state.count1
        # if 'count2' in st.session_state:
        #     print('关闭b')
        #     st.session_state.count2.kill()
        #     del st.session_state.count2
        if 'count3' in st.session_state:
            print('关闭c')
            st.session_state.count3.kill()
            del st.session_state.count3
        if 'count4' in st.session_state:
            print('关闭d')
            st.session_state.count4.kill()
            del st.session_state.count4
    # if button1 and not button2 and not button3:
    #     a = subprocess.Popen(['D:\\pythonProject\\real-time-radar-master\\venv\\Scripts\\python.exe','./tools/server_t.py'])
    #     b = subprocess.Popen(['D:\\pythonProject\\real-time-radar-master\\venv\\Scripts\\python.exe', './tools/server_a.py'])
    #     if button3:
    #         print('关闭ab')
    #         a.kill()
    #         b.kill()
    # if button2 and not button3:
    #     c = subprocess.Popen(['D:\\pythonProject\\real-time-radar-master\\venv\\Scripts\\python.exe', './tools/onnx_run.py'])
    #     d = subprocess.Popen(['D:\\pythonProject\\real-time-radar-master\\venv\\Scripts\\python.exe', './tools/client.py'])
    #     if button3:
    #         print('关闭cd')
    #         c.kill()
    #         d.kill()

