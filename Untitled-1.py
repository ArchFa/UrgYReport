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
months = {
        1: 'Январь',
        2: 'Февраль',
        3: 'Март',
        4: 'Апрель',
        5: 'Май',
        6: 'Июнь',
        7: 'Июль',
        8: 'Август',
        9: 'Сентябрь',
        10: 'Октябрь',
        11: 'Ноябрь',
        12: 'Декабрь'
    }
df['month'] = df['month'].apply(lambda x: months[x])

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
сount_responds = (
    df.query('platform != "''"')
    .pivot_table(index=["month"], values='count_responds', aggfunc='sum'))
сount_responds = сount_responds.reset_index()

# %%
сount_prematch = (
    df.query('platform != "''"')
    .pivot_table(index=["month"], values='count_prematch', aggfunc='sum'))
сount_prematch = сount_prematch.reset_index()

# %%
percentage_tasks_with_response = (
    df.query('platform != "''" & count_responds > 0')
    .pivot_table(index=["month"], values='count_prematch', aggfunc='count'))
percentage_tasks_with_response = percentage_tasks_with_response.reset_index()



percentage_tasks_with_response = percentage_tasks_with_response.merge(all_task_month, left_on='month', right_on='month')
percentage_tasks_with_response = percentage_tasks_with_response.rename(columns={'offer_id': 'count_no_prematch'})


# рассчет процентов задач через приложение
percentage_tasks_with_response['percentage_otklik'] = percentage_tasks_with_response['count_prematch'] * 100 / percentage_tasks_with_response['count_no_prematch']
percentage_tasks_with_response['percentage_otklik'] = percentage_tasks_with_response['percentage_otklik'].round(2)

# %%
################################### графики и отображаемые элементы ###################################

# %%
# bar "Количество созданных офферов в месяц"

cx = px.bar(offers_count_month, x='month', y='offer_id',
            color='platform',
            height=700,
            width=1200,
            title="Количество созданных офферов в месяц",
            labels={'offer_id':'Количество созданных офферов', 'platform':'Платформа создания', 'month':'Месяц'},
            barmode = 'group',
            text_auto=True)
st.plotly_chart(cx)

# %%
# bar Процент офферов через приложение

cxx = px.bar(percentage_tasks_mobile, x='month', y='percentage_mobile',
            height=700,
            width=1200,
            title="Процент офферов через приложение",
            labels={'month':'Месяц', 'percentage_mobile':'Процент задач через приложение'},
            text_auto=True)
st.plotly_chart(cxx)

# %%
# bar Процент офферов через приложение

cxxx = px.bar(сount_responds, x='month', y='count_responds',
            height=700,
            width=1200,
            title="Процент офферов через приложение",
            labels={'month':'Месяц', 'count_responds':'Количество откликов'},
            text_auto=True)
st.plotly_chart(cxxx)

# %%
# bar Процент офферов через приложение

cxxxx = px.bar(сount_prematch, x='month', y='count_prematch',
            height=700,
            width=1200,
            title="Количество матчей",
            labels={'month':'Месяц', 'count_prematch':'Количество матчей'},
            text_auto=True)
st.plotly_chart(cxxxx)

# %%
percentage_tasks_with_response


# bar Процент офферов через приложение

cxxxxx = px.bar(percentage_tasks_with_response, x='month', y='percentage_otklik',
            height=700,
            width=1200,
            title="Процент задач с откликом",
            labels={'month':'Месяц', 'percentage_otklik':'Процент задач с откликом'},
            text_auto=True)
st.plotly_chart(cxxxxx)

# %%



