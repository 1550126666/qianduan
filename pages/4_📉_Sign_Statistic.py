import time

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
st.set_page_config(page_title="Sign Statistic", page_icon="📉")
st.title("生命体征检测统计系统")
st.sidebar.header("Sign Statistic")
renew = st.sidebar.button("更新")
out = 0
sign_warning = st.metric("今日生命体征异常次数", out)

ini = pd.DataFrame()
st.header("生命体征异常次数")
sign_bar = st.bar_chart(ini)
st.header("每日生命体征异常次数")
sign_date = st.line_chart(ini)
mydb = mysql.connector.connect(
  host="8.130.75.230",
  user="admin",
  password="123456",
  database="my"
)


if renew:
    # 从数据库中获取数据
    query = "SELECT time,type,date FROM signs"
    df = pd.read_sql(query, mydb)
    # df = conn.query("select time,type,date from vital")
    data = pd.DataFrame(df)

    warning_counts = data['type'].value_counts()
    warning = pd.DataFrame(
        warning_counts.values, warning_counts.index
    )
    sign_bar.bar_chart(warning)
    sign_counts_by_type = data.groupby(['date', 'type']).size().unstack(fill_value=0)
    sign_date.line_chart(sign_counts_by_type)
    now_time = time.ctime()
    now_time = now_time.replace(now_time.split(" ")[3], "")
    sign_counts_over_time = data['date'].value_counts()
    for sign in sign_counts_over_time.index:
        if now_time in sign:
            out = sign_counts_over_time[sign]
    sign_warning.metric("今日生命体征异常次数",  out)

