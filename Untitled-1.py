# %%
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np


# %%
################################### параметры страницы ###################################

# %%
st.title("Дашборд UrgY")

# %%
################################### основные вычисления ###################################

# %%
count_task = st.file_uploader("Выбирете файл")


use_example_file = st.checkbox(
    "Использовать пример выгрузки", False, help="Будет использована базовая выгрузка, c 1 апреля по 1 июля"
)

# использование примера файла
if use_example_file:
    count_task = "offers_statuses_04_01_07_01.txt"

# использование загруженного файла
if count_task:
    df = pd.read_csv(count_task, sep='|')
    df = df.dropna()

    df.columns = ['offer_id', 'offer_created_at','platform','count_responds', 'count_prematch']

    df['offer_created_at'] = pd.to_datetime(df['offer_created_at'])
    df.offer_created_at = df.offer_created_at.values.astype('M8[D]')

    df['count_responds'] = df['count_responds'].astype(int)
    df['count_prematch'] = df['count_prematch'].astype(int)

    df['platform'] = df['platform'].str.strip()

st.info(
        f"""
             👆 Загрузите файл с расширением csv или txt. В файле должны стого содержаться следующие столбцы:
             - id оффера
             - дата создания оффера
             - платформа создания оффера
             - количество прематчей на задачу
             - количество матчей на задачу
             """
    )

if not count_task or not use_example_file:
        st.stop()

# %%
df['month'] = df['offer_created_at'].dt.month

# %%
# df = pd.read_csv("/Users/arturfattahov/Downloads/Telegram Desktop/offers_statuses_04_01_07_01.txt", sep='|')

# df = df.dropna()

# df.columns = ['offer_id', 'offer_created_at','platform','count_responds', 'count_prematch']

# df['offer_created_at'] = pd.to_datetime(df['offer_created_at'])
# df.offer_created_at = df.offer_created_at.values.astype('M8[D]')

# df['count_responds'] = df['count_responds'].astype(int)
# df['count_prematch'] = df['count_prematch'].astype(int)

# df['platform'] = df['platform'].str.strip()
# df['month'] = df['offer_created_at'].dt.month

# %%
################################## Количество созданных офферов в месяц с разделением по платформе
# создание датафрейма для графика "Количество созданных офферов в месяц"

offers_count_month = (
    df.query('platform != "''"')
    .pivot_table(index=["month", "platform"], values='offer_id', aggfunc='count'))

offers_count_month = offers_count_month.reset_index()

# %%
df_mobile = df
################################## Процент офферов через приложение
# меняем ios и android на mobile

df_mobile['platform'] = np.where((df_mobile.platform == "ios"), "mobile", df_mobile.platform)
df_mobile['platform'] = np.where((df_mobile.platform == "android"), "mobile", df_mobile.platform)


# датафрейм со всеми задачами в месяц, без разделения по платформам
all_task_month = (
    df_mobile.query('platform != "''"')
    .pivot_table(index=["month"], values='offer_id', aggfunc='count'))
all_task_month = all_task_month.reset_index()


# датафрейм с задачами через мобильное приложение
percentage_tasks_mobile = (
    df_mobile.query('platform == "mobile"')
    .pivot_table(index=["month"], values='offer_id', aggfunc='count'))
percentage_tasks_mobile = percentage_tasks_mobile.reset_index()


# мердж двух таблиц
percentage_tasks_mobile = percentage_tasks_mobile.merge(all_task_month, left_on='month', right_on='month')
percentage_tasks_mobile.columns = ['month', 'mobile', 'all']


# рассчет процентов задач через приложение
percentage_tasks_mobile['percentage_mobile'] = percentage_tasks_mobile['mobile'] * 100 / percentage_tasks_mobile['all']
percentage_tasks_mobile['percentage_mobile'] = percentage_tasks_mobile['percentage_mobile'].round(2)

# %%
################################### графики и отображаемые элементы ###################################

# %%
# bar "Количество созданных офферов в месяц"

cx = px.bar(offers_count_month, x='month', y='offer_id',
            color='platform',
            height=700,
            title="Количество созданных офферов в месяц",
            labels={'offer_id':'Количество созданных офферов', 'platform':'Платформа создания'},
            barmode = 'group',
            text_auto=True)
cx.show()

# %%
# bar Процент офферов через приложение

cxx = px.bar(percentage_tasks_mobile, x='month', y='percentage_mobile',
            height=700,
            width=500,
            title="Процент офферов через приложение",
            labels={'month':'Месяц', 'percentage_mobile':'Процент задач через приложение'},
            text_auto=True)
cxx.show()

# %%



