import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt


st.title('Загрузить датасет')

uploaded_file = st.file_uploader('Загрузите файл CSV', type = 'csv')

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.sidebar.warning('Загрузите файл CSV')

if 'df' in locals():

    df['year']=df['month'].str.split('-').str[0]
    y = df['year'].unique().astype(int)
    
    year = st.selectbox('Год', options = range(min(y), max(y)), index=0)

    filtered_df  = df[pd.to_datetime(df['month']).dt.year == year]
    top_states = filtered_df.groupby('state')['totals'].sum().nlargest(10)

    fig, ax = plt.subplots(figsize=(10, 8))
    top_states.plot.pie(autopct='%1.1f%%', ax=ax)
    ax.set_ylabel('')
    st.pyplot(fig)

    state = st.selectbox('Штат', df['state'].unique())
    state_df = df[df['state'] == state] 


    button = st.button('Скачать CSV')
    if button:
        state_df.to_csv(f'{state}_data.csv', index=False)
