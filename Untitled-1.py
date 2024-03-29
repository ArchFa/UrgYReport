# %%
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import plotly.graph_objects as go


# %%
################################### параметры страницы ###################################

# %%
st.title("Дашборд UrgY")

# %%
################################### основные вычисления ###################################

# %%
count_task = st.file_uploader("Выбирете файл")


use_example_file = st.checkbox(
    "Использовать пример выгрузки", False, help="Будет использована базовая выгрузка, c 1 апреля по 1 августа"
)

# использование примера файла
if use_example_file:
    count_task = "tasks_report(2022-08-09T09_17_08.636Z).csv"


# использование загруженного файла
if count_task:
    df = pd.read_csv(count_task, sep='|')
    df = df.dropna()

    df.rename(columns = {'id задачи' : 'offer_id',
                     'Дата создания' : 'offer_created_at',
                     'Платформа': 'platform',
                     'Способ связи': 'communication_type',
                     'Кол-во откликов': 'count_responds',
                     'Кол-во прематчей': 'count_prematch'}, inplace = True)

    df['offer_created_at'] = pd.to_datetime(df['offer_created_at'])
    df.offer_created_at = df.offer_created_at.values.astype('M8[D]')

    df['count_responds'] = df['count_responds'].astype(int)
    df['count_prematch'] = df['count_prematch'].astype(int)

    df['platform'] = df['platform'].str.strip()


with st.expander("Требования к загружаемому файлу"):
     st.info(
        """
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

#
# %%
# df = pd.read_csv("/Users/arturfattahov/Downloads/tasks_report(2022-08-08T12_16_42.719Z).csv", sep='|')

# df = df.dropna()

# df.rename(columns = {'id задачи' : 'offer_id',
#                      'Дата создания' : 'offer_created_at',
#                      'Платформа': 'platform',
#                      'Способ связи': 'communication_type',
#                      'Кол-во откликов': 'count_responds',
#                      'Кол-во матчей': 'count_prematch'}, inplace = True)

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
df['month_name'] = df['month'].apply(lambda x: months[x])


monthss = {
        'Январь': 1,
        'Февраль': 2,
        'Март': 3,
        'Апрель': 4,
        'Май': 5,
        'Июнь': 6,
        'Июль': 7,
        'Август': 8,
        'Сентябрь': 9,
        'Октябрь': 10,
        'Ноябрь': 11,
        'Декабрь': 12
    }

# %%
################################## информация о текущем месяце, сравнение с предыдущем


last_month = df['month'].max()
pre_last_month = df['month'].max() - 1

df_mob = df.query('platform == "ios" | platform == "android"')

# общее количество задач
count_task_last_month_all = df.query('month == @last_month').count()[0]
count_task_pre_last_month_all = df.query('month == @pre_last_month').count()[0]
difference_all = str(count_task_last_month_all - count_task_pre_last_month_all)


# задачи через Android
count_task_last_month_android = df.query('month == @last_month & platform == "android"').count()[0]
count_task_pre_last_month_android = df.query('month == @pre_last_month & platform == "android"').count()[0]
difference_android = str(count_task_last_month_android - count_task_pre_last_month_android)


# задачи через Admins
count_task_last_month_admins = df.query('month == @last_month & platform == "admins"').count()[0]
count_task_pre_last_month_admins = df.query('month == @pre_last_month & platform == "admins"').count()[0]
difference_admins = str(count_task_last_month_admins - count_task_pre_last_month_admins)


# задачи через iOS
count_task_last_month_ios = df.query('month == @last_month & platform == "ios"').count()[0]
count_task_pre_last_month_ios = df.query('month == @pre_last_month & platform == "ios"').count()[0]
difference_ios = str(count_task_last_month_ios - count_task_pre_last_month_ios)

# задачи через web
count_task_last_month_web = df.query('month == @last_month & platform == "web"').count()[0]
count_task_pre_last_month_web = df.query('month == @pre_last_month & platform == "web"').count()[0]
difference_web = str(count_task_last_month_web - count_task_pre_last_month_web)

# задачи через mobile
count_task_last_month_mob = df_mob.query('month == @last_month').count()[0]
count_task_pre_last_month_mob = df_mob.query('month == @pre_last_month').count()[0]
difference_mob = str(count_task_last_month_mob - count_task_pre_last_month_mob)

# %%
################################## вычисления для построения pie за последний месяц


count_task_platform_last_monht = (
    df.query('month == @last_month & platform != "-"')
    .pivot_table(index=["platform"], values='offer_id', aggfunc='count'))

count_task_platform_last_monht = count_task_platform_last_monht.reset_index()
count_task_platform_last_monht.columns = ['platformm', 'count_task']


count_task_platform_last_monht['all'] = df.query('month == @last_month').count()[0]
count_task_platform_last_monht['persent'] = (count_task_platform_last_monht['count_task'] * 100 / count_task_platform_last_monht['all']).round(2)
count_task_platform_last_monht['persent'] = count_task_platform_last_monht['persent'].astype(str)
count_task_platform_last_monht['platform'] = count_task_platform_last_monht['platformm'] + ' ' + count_task_platform_last_monht['persent'] + '%'

# %%
# ################################## Количество созданных офферов в месяц с разделением по платформе
# # создание датафрейма для графика "Количество созданных офферов в месяц"

# offers_count_month = (
#     df.query('platform != "''"')
#     .pivot_table(index=["month_name", "platform"], values='offer_id', aggfunc='count'))

# offers_count_month = offers_count_month.reset_index()

# %%
df_mobile = df
################################## Процент офферов через приложение
# меняем ios и android на mobile

df_mobile['platform'] = np.where((df_mobile.platform == "ios"), "mobile", df_mobile.platform)
df_mobile['platform'] = np.where((df_mobile.platform == "android"), "mobile", df_mobile.platform)


# датафрейм со всеми задачами в месяц, без разделения по платформам
all_task_month = (
    df_mobile.query('platform != "-"')
    .pivot_table(index=["month_name"], values='offer_id', aggfunc='count'))
all_task_month = all_task_month.reset_index()


# датафрейм с задачами через мобильное приложение
percentage_tasks_mobile = (
    df_mobile.query('platform == "mobile"')
    .pivot_table(index=["month_name"], values='offer_id', aggfunc='count'))
percentage_tasks_mobile = percentage_tasks_mobile.reset_index()


# мердж двух таблиц
percentage_tasks_mobile = percentage_tasks_mobile.merge(all_task_month, left_on='month_name', right_on='month_name')
percentage_tasks_mobile.columns = ['month_name', 'mobile', 'all']


# рассчет процентов задач через приложение
percentage_tasks_mobile['percentage_mobile'] = percentage_tasks_mobile['mobile'] * 100 / percentage_tasks_mobile['all']
percentage_tasks_mobile['percentage_mobile'] = percentage_tasks_mobile['percentage_mobile'].round(2)


percentage_tasks_mobile['monthh'] = percentage_tasks_mobile['month_name'].apply(lambda x: monthss[x])
percentage_tasks_mobile = percentage_tasks_mobile.sort_values(by=['monthh'])
percentage_tasks_mobile = percentage_tasks_mobile.reset_index()

####
last_m = max(percentage_tasks_mobile.index)
pre_last_m = last_m - 1

persent_mob_last = str(percentage_tasks_mobile['percentage_mobile'][last_m]) + '%'
dif = percentage_tasks_mobile['percentage_mobile'][last_m] - percentage_tasks_mobile['percentage_mobile'][pre_last_m]
dif = dif.round(2)


# %%
# рассчеты для графика количества откликов и прематчей

сount_responds = (
    df.query('platform != "-"')
    .pivot_table(index=["month_name"], values='count_responds', aggfunc='sum'))
сount_responds = сount_responds.reset_index()

сount_prematch = (
    df.query('platform != "-"')
    .pivot_table(index=["month_name"], values='count_prematch', aggfunc='sum'))
сount_prematch = сount_prematch.reset_index()

сount_prematch_responds = сount_prematch.merge(сount_responds, left_on='month_name', right_on='month_name')
сount_prematch_responds['monthh'] = сount_prematch_responds['month_name'].apply(lambda x: monthss[x])
сount_prematch_responds = сount_prematch_responds.sort_values(by=['monthh'])

# %%
percentage_tasks_with_response = (
    df.query('platform != "-" & count_responds > 0')
    .pivot_table(index=["month_name"], values='count_prematch', aggfunc='count'))
percentage_tasks_with_response = percentage_tasks_with_response.reset_index()



percentage_tasks_with_response = percentage_tasks_with_response.merge(all_task_month, left_on='month_name', right_on='month_name')
percentage_tasks_with_response = percentage_tasks_with_response.rename(columns={'offer_id': 'count_no_prematch'})


# рассчет процентов задач через приложение
percentage_tasks_with_response['percentage_otklik'] = percentage_tasks_with_response['count_prematch'] * 100 / percentage_tasks_with_response['count_no_prematch']
percentage_tasks_with_response['percentage_otklik'] = percentage_tasks_with_response['percentage_otklik'].round(0)
percentage_tasks_with_response['monthh'] = percentage_tasks_with_response['month_name'].apply(lambda x: monthss[x])
percentage_tasks_with_response = percentage_tasks_with_response.sort_values(by=['monthh'])

# %%
################################### графики и отображаемые элементы ###################################

# %%
# метрики с количеством задач

col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("All", count_task_last_month_all, difference_all)
col2.metric("Android", count_task_last_month_android, difference_android)
col3.metric("iOS", count_task_last_month_ios, difference_ios)
col4.metric("Admins", count_task_last_month_admins, difference_admins)
col5.metric("WEB", count_task_last_month_web, difference_web)
col6.metric("Mobile", persent_mob_last, dif)

# %%
# pie с процентом задач по платформам


fig = px.pie(
    count_task_platform_last_monht,
    values='count_task',
    names='platform',
    title='Распределение задач по платформе',
    labels={
                "platform": "Платформа",  "count_task": "Количество задач"
            })

st.plotly_chart(fig)

# %%
# bar "Количество созданных офферов в месяц"

# cx = px.bar(offers_count_month, x='month_name', y='offer_id',
#             color='platform',
#             title="Количество созданных офферов в месяц",
#             labels={'offer_id':'Количество созданных офферов', 'platform':'Платформа создания', 'month_name':'Месяц'},
#             barmode = 'group',
#             text_auto=True)
# st.plotly_chart(cx)

# %%
# # bar Процент офферов через приложение

# cxx = px.bar(percentage_tasks_mobile, x='month_name', y='percentage_mobile',
#             title="Процент офферов через приложение",
#             labels={'month_name':'Месяц', 'percentage_mobile':'Процент задач через приложение'},
#             text_auto=True)
# st.plotly_chart(cxx)

# %%
# # bar Количество откликов

# cxxx = px.bar(сount_responds, x='month_name', y='count_responds',
#             title="Количество откликов",
#             labels={'month_name':'Месяц', 'count_responds':'Количество откликов'},
#             text_auto=True)
# st.plotly_chart(cxxx)

# %%
# # bar Процент офферов через приложение

# cxxxx = px.bar(сount_prematch, x='month_name', y='count_prematch',
#             title="Количество матчей",
#             labels={'month_name':'Месяц', 'count_prematch':'Количество матчей'},
#             text_auto=True)
# st.plotly_chart(cxxxx)

# %%
# bar отклики и прематчи

cxdd = px.bar(сount_prematch_responds, x='month_name', y=['count_prematch','count_responds'],
            title="Количество прематчей и матчей",
            labels={'variable':'Тип отклика', 'value':'Количество', 'month_name':'Месяц'},
            barmode='group',
            text_auto=True)
st.plotly_chart(cxdd)
#cxdd.show()

# %%
# bar Процент задач с откликом

figi = go.Figure([go.Bar(x=percentage_tasks_with_response['month_name'], y=percentage_tasks_with_response['percentage_otklik'], texttemplate = "%{y}%")])
figi.update_layout(
                  title="Процент задач с откликом",
                  xaxis_title="Месяц",
                  yaxis_title="Процент задач с откликом",)
st.plotly_chart(figi)


# %%
df_mobile_only = df_mobile.query('platform == "mobile"')

сount_in_app = (
    df_mobile_only.query('communication_type == "через приложение"')
    .pivot_table(index=["month_name"], values='count_responds', aggfunc='count'))
сount_in_app = сount_in_app.reset_index()

сount_in_phone = (
    df_mobile_only.query('communication_type == "через телефон"')
    .pivot_table(index=["month_name"], values='count_responds', aggfunc='count'))
сount_in_phone = сount_in_phone.reset_index()

type_comm = сount_in_app.merge(сount_in_phone, left_on='month_name', right_on='month_name')
type_comm['monthh'] = type_comm['month_name'].apply(lambda x: monthss[x])
type_comm = type_comm.sort_values(by=['monthh'])
type_comm['all'] = type_comm['count_responds_x'] + type_comm['count_responds_y']

type_comm['percent_phone'] = type_comm['count_responds_y'] * 100 / type_comm['all']
type_comm['percent_phone'] = type_comm['percent_phone'].round(2)

type_comm['percent_app'] = type_comm['count_responds_x'] * 100 / type_comm['all']
type_comm['percent_app'] = type_comm['percent_app'].round(2)


figj = go.Figure(data=[
    go.Bar(name='Через телефон', x=type_comm['month_name'], y=type_comm['percent_phone'], texttemplate = "%{y}%"),
    go.Bar(name='Через приложение',x=type_comm['month_name'], y=type_comm['percent_app'], texttemplate = "%{y}%"),
])
# Change the bar mode

figj.update_layout(
                  title="Распределение типов связи",
                  xaxis_title="Месяц",
                  yaxis_title="Процент типа связи",
                  barmode='group',)

st.plotly_chart(figj)


