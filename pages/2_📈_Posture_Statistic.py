import time
import plotly.express as px
import streamlit as st
import numpy as np
import pandas as pd
import mysql.connector
# import matplotlib.pyplot as plt
# import seaborn as sns
# 文字内容
st.set_page_config(page_title="Posture Statistic", page_icon="📈")
gx = st.sidebar.button("更新")
st.title("错误坐姿统计系统")
st.sidebar.header("Posture Statistic")
st.write("欢迎使用错误坐姿统计系统！")

# 页面初始化
ini = pd.DataFrame()
col1, col2 = st.columns(2)
with col1:
    error_num = st.metric("今日错误坐姿次数", 0)
    st.header("错误坐姿次数统计")
    # error_posture = st.bar_chart(ini)
    error_posture = st.empty()
with col2:
    error_more = st.metric("今日最常出现坐姿", "无")
    st.header("时间和错误坐姿次数关系")
    error_time = st.line_chart(ini)
st.header("错误坐姿记录列表")
error_table = st.table(ini)
# error_heatmap = st.empty()

# 数据库
mydb = mysql.connector.connect(
  host="8.130.75.230",
  user="admin",
  password="123456",
  database="my"
)

# 创建游标
# mycursor = mydb.cursor()


if gx:
    # 从数据库中获取数据
    query = "SELECT time,type,date FROM error"
    df = pd.read_sql(query, mydb)
    data = pd.DataFrame(df)
    # 类型与次数
    error_counts = data['type'].value_counts()
    error = pd.DataFrame(
        {'type': error_counts.index, 'num': error_counts.values}
    )
    fig = px.pie(
        names=error_counts.index,
        values=error_counts.values,
        title="错误坐姿次数统计",
        labels={"names": "错误坐姿类型", "values": "次数"},
        hole=0.4,  # 控制内部空心圆的大小，值为0到1之间
        color_discrete_sequence=px.colors.qualitative.Set3,  # 颜色序列
        template="plotly_white",  # 图表的样式模板
    )
    fig.update_traces(
        textposition="inside",  # 将标签置于扇形内部
        textinfo="percent+label",  # 显示百分比和标签
    )
    error_posture.plotly_chart(fig, use_container_width=True)
    # error_posture.bar_chart(error)

    # 数据列表
    error_table.dataframe(data, use_container_width=True)
    # 时间与次数
    # error_counts_over_time = data['date'].value_counts()
    # fig, ax = plt.subplots()
    # error = pd.DataFrame(
    #     error_counts_over_time.values, error_counts_over_time.index
    # )
    # error_time.area_chart(error)
    error_counts_by_type = data.groupby(['date', 'type']).size().unstack(fill_value=0)
    error_time.line_chart(error_counts_by_type)
    # 今日错误坐姿次数
    now_time = time.ctime()
    now_time = now_time.replace(now_time.split(" ")[3], "")
    out = data[data['date'] == now_time].shape[0]
    error_num.metric("今日错误坐姿次数",  out)

    data_today = data[data['date'] == now_time]
    if not data_today.empty:
        today = data_today['type'].value_counts()
        out1 = today.index[0]
    else:
        out1 = '无'
    error_more.metric("今日最常出现坐姿", out1)

    # ax.plot(error_counts_over_time.index, error_counts_over_time.values)
    # ax.set_xlabel('时间')
    # ax.set_ylabel('错误坐姿次数')
    # st.pyplot(fig)
#
# def add_error_record():
#     st.header("添加错误坐姿记录")
#     error_type = st.text_input("错误坐姿类型")
#     time = st.text_input("时间")
#     if st.button("添加记录"):
#         data.loc[len(data)] = [error_type, time]
#         st.success("错误坐姿记录添加成功！")
