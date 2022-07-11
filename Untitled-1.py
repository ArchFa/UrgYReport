# %%
import pandas as pd
import streamlit as st

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
    count_task = "offers_statuses (3).txt"

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
    st.dataframe(df.head())

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

if not uploaded_file or not use_example_file:
        st.stop()

# %%



