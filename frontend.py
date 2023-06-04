import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

st.title("Тестовое задание MVideo")

uploaded_file = st.file_uploader('Choose file')
df = pd.read_csv(uploaded_file)
st.write(df)
days = st.slider('Выберете количество дней', 0, 8)
age = st.slider('Выберет возраст', 23, 60)

try uploaded_file is not None:
    # Eead DataFrame

    df[f'Старше {age}'] = df['Возраст'].apply(lambda x: 'Да' if x > age else 'Нет')
    
    # Plots
    fig, axs = plt.subplots(nrows=2, ncols=3, figsize = (14, 11))
    fig.tight_layout(pad=6.0)
    # Plot 0.0
    gender_counts = df[df['Количество больничных дней'] >= days].groupby('Пол')['Количество больничных дней'].sum()

    axs[0, 0].bar(gender_counts.index, gender_counts)
    axs[0, 0].set_xlabel('Пол')
    axs[0, 0].set_ylabel('Количество больничных дней')
    axs[0, 0].set_title('Сравнение количества\n больничных дней по полу\n(bar blot)')
    axs[0, 0].grid(axis='y')
    

    # Plot 0.1
    sns.boxplot(ax=axs[0, 1], x='Пол', y='Количество больничных дней', data=df[df['Количество больничных дней'] >= days])
    axs[0, 1].set_title('Распределение количества\n больничных дней по полу\n(box plot)')
    axs[0, 1].set_xlabel('Пол')
    axs[0, 1].set_ylabel('Количество больничных дней')
    axs[0, 1].grid(axis='y')
    
    # Plot 0.2
    sns.histplot(ax=axs[0, 2], data=df[df['Количество больничных дней'] >= days], x='Количество больничных дней', hue='Пол', element='step', kde=True)
    axs[0, 2].set_title('Распределение количества\n больничных дней по полу\n(hist plot)')
    axs[0, 2].grid(axis='y')

    # Plot 1.0
    age_counts = df.groupby(f'Старше {age}')['Количество больничных дней'].sum()

    axs[1, 0].bar(age_counts.index, age_counts)
    axs[1, 0].set_xlabel(f'Старше {age}')
    axs[1, 0].set_ylabel('Количество больничных дней')
    axs[1, 0].set_title('Сравнение количества\n больничных дней по возрасту\n(bar plot)')
    axs[1, 0].grid(axis='y')
    
    # Plot 1.1
    sns.boxplot(ax=axs[1, 1], x=f'Старше {age}', y='Количество больничных дней', data=df)
    axs[1, 1].set_title('Распределение количества\n больничных дней по возрасту\n(box plot)')
    axs[1, 1].set_xlabel('Пол')
    axs[1, 1].set_ylabel('Количество больничных дней')
    axs[1, 1].grid(axis='y')

    # Plot 1.2
    sns.histplot(ax=axs[1, 2], data=df, x='Количество больничных дней', hue=f'Старше {age}', element='step', kde=True)
    axs[1, 2].set_title('Распределение количества\n больничных дней по возрасту\n(hist plot)')
    axs[1, 2].grid(axis='y')

    st.pyplot(fig)

    # Разделение данных на группы по полу
    male_data = df[(df['Пол'] == 'М') & (df['Количество больничных дней'] >= days)]
    female_data = df[(df['Пол'] == 'Ж') & (df['Количество больничных дней'] >= days)]
    # Разделение данных на группы по возрасту

    older_data = df[df['Возраст'] > age]
    younger_data = df[df['Возраст'] <= age]


    # Проведение t-теста для групп по полу
    t_statistic, p_value = stats.ttest_ind(male_data['Количество больничных дней'], female_data['Количество больничных дней'])

    if p_value < 0.05:
        st.markdown(f"p_value = {p_value}:")
        st.markdown("Статистически значимая разница между мужчинами и женщинами.")
    else:
        st.markdown(f"p_value = {p_value}:")                    
        st.markdown("Нет статистически значимой разницы между мужчинами и женщинами.")
    # Проведение t-теста для групп по возрасту

    t_statistic, p_value = stats.ttest_ind(older_data['Количество больничных дней'], younger_data['Количество больничных дней'])

    if p_value < 0.05:
        st.markdown(f"p_value = {p_value}:")
        st.markdown(f"Статистически значимая разница между сотрудниками старше {age} и моложе {age}.")
    else:
        st.markdown(f"p_value = {p_value}:")
        st.markdown(f"Нет статистически значимой разницы между сотрудниками старше {age} и моложе {age}.")
catch:
    print("Wrong file")
