import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

day_df_cleaned = pd.read_csv('day_df_cleaned.csv')
hour_df_cleaned = pd.read_csv('hour_df_cleaned.csv')
day_df_cleaned['season'] = day_df_cleaned['season'].map({
    1: 'Semi',
    2: 'Panas',
    3: 'Gugur',
    4: 'Salju'
})


day_df_cleaned['yr'] = day_df_cleaned['yr'].map({
    0: 2011,
    1: 2012
})

day_df_cleaned['weathersit'] = day_df_cleaned['weathersit'].map({
    1: 'Cerah/Sedikit Berawan',
    2: 'Berkabut/Berawan',
    3: 'Salju Ringan/Hujan Ringan',
    4: 'Hujan Deras/Salju'
})

day_df_cleaned['weekday'] = day_df_cleaned['weekday'].map({
    0: 'Minggu',
    1: 'Senin',
    2: 'Selasa',
    3: 'Rabu',
    4: 'Kamis',
    5 : 'Jumat',
    6 : 'Sabtu'
})

st.title('Analisis Rental Sepeda berdasarkan Faktor Cuaca dan Waktu')

# Visualisasi Day Data
st.header('Visualisasi Data Berdasarkan Faktor Cuaca')

# Analisis Berdasarkan Musim 
st.header('Analisis Berdasarkan Musim')

grouped_season_df = day_df_cleaned.groupby('season').agg({
    'cnt': ['mean', 'max', 'min'],
    'windspeed': 'mean',
    'hum': 'mean',
    'atemp': 'mean',
    'temp': 'mean'
}).reset_index()

grouped_season_df.columns = ['season', 'mean_cnt', 'max_cnt', 'min_cnt', 
                             'Kecepatan_angin', 'Kelembapan', 'Feeling Temperature', 'Temperature Aktual']

fig, axes = plt.subplots(2, 1, figsize=(10, 10))

# Plot 1: Rata-rata jumlah rental per musim
sns.barplot(data=grouped_season_df, x='season', y='mean_cnt', ax=axes[0])
axes[0].set_title('Rata-rata Jumlah Rental per Musim (cnt)')
axes[0].set_xlabel('Musim')
axes[0].set_ylabel('Jumlah Rental')

# Plot 2: Rata-rata windspeed, hum, atemp, dan temp per musim
sns.barplot(data=grouped_season_df.melt(id_vars='season', 
                                         value_vars=['Kecepatan_angin', 'Kelembapan', 'Feeling Temperature', 'Temperature Aktual'],
                                         var_name='variable', value_name='value'),
            x='season', y='value', hue='variable', ax=axes[1])
axes[1].set_title('Rata-rata Kecepatan Angin, Kelembapan, Feeling Temperature, dan Temperature Aktual per Musim')
axes[1].set_xlabel('Musim')
axes[1].set_ylabel('Rata-rata')
axes[1].legend(title='Variabel')

plt.tight_layout()
st.pyplot(fig)

st.markdown("""
Analisis ini menunjukkan bagaimana jumlah rental sepeda berfluktuasi berdasarkan musim. Rata-rata kondisi cuaca seperti kecepatan angin, kelembapan, dan suhu juga mempengaruhi tren.
""")


#Hubungan Feeling Temperature dengan Jumlah Rental Per Hari
st.subheader('Hubungan Feeling Temperature(atemp) dengan Jumlah Rental(cnt) Per Hari')
fig, ax = plt.subplots()
sns.regplot(x='atemp', y='cnt', data=day_df_cleaned)
ax.set_title('Hubungan Feeling Temperature dengan Jumlah Rental Per Hari')
st.pyplot(fig)

# Analisis untuk plot 1
st.markdown("""
Dari grafik tersebut, terlihat adanya korelasi positif antara `feeling temperature` (atemp) dan jumlah rental sepeda per hari (`cnt`).
""")

st.subheader('Hubungan Kecepatan Angin(windspeed) dengan Jumlah Rental(cnt) Per Hari')
fig, ax = plt.subplots()
sns.regplot(x='windspeed', y='cnt', data=day_df_cleaned)
ax.set_title('Hubungan Kondisi Cuaca dengan Jumlah Rental Per Hari')
y_min = day_df_cleaned['cnt'].min()
y_max = day_df_cleaned['cnt'].max()
ax.set_ylim(y_min, y_max)
st.pyplot(fig)

st.markdown("""
Kecepatan angin (`windspeed`) per hari  memiliki dampak negatif pada jumlah rental sepeda, terutama pada kecepatan angin yang lebih tinggi.
""")


st.subheader('Hubungan Kondisi Cuaca(weathersit) dengan Jumlah Rental(cnt) Per Hari')
fig, ax = plt.subplots()
sns.scatterplot(x='weathersit', y='cnt', data=day_df_cleaned,s=10)
ax.set_title('Hubungan Kondisi Cuaca dengan Jumlah Rental Per Hari')
y_min = day_df_cleaned['cnt'].min()
y_max = day_df_cleaned['cnt'].max()
ax.set_ylim(y_min, y_max)
st.pyplot(fig)

st.markdown("""
Kondisi Cuaca (`weathersit`) per hari memiliki pengaruh terhadap jumlah peminjaman sepeda. Kondisi cuaca yang cerah cenderung meningkatkan jumlah peminjaman,
sedangkan cuaca yang cenderung mendung dan hujan akan menurunkan jumlah peminjaman sepeda per harinya.
""")



st.header('Visualisasi Data Berdasarkan Waktu')

grouped_weekday_df = day_df_cleaned.groupby('weekday').agg({
    'cnt': ['mean', 'max', 'min']
}).reset_index()

grouped_weekday_df.columns = ['weekday', 'Rata-Rata', 'Maksimum', 'Minimum']
urutan = [ 'Minggu','Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']


grouped_weekday_df['weekday'] = pd.Categorical(grouped_weekday_df['weekday'], categories=urutan, ordered=True)
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=grouped_weekday_df.melt(id_vars='weekday', var_name='statistic', value_name='cnt_value'),
            x='weekday', y='cnt_value', hue='statistic')
ax.set_title('Rata-rata, Maksimum, dan Minimum Jumlah Rental per Hari dalam Seminggu')
ax.set_xlabel('Hari dalam Minggu')
ax.set_ylabel('Jumlah Rental')
st.pyplot(fig)
st.markdown("""
Distribusi jumlah rental sepeda berdasarkan hari menunjukkan adanya puncak pada hari-hari tertentu,terutama di hari kerja (senin-jumat ), yang mencerminkan kebiasaan bersepeda pada jam kerja.
""")

# Distribusi Jumlah Rental Berdasarkan Jam
st.subheader('Distribusi Jumlah Rental(cnt) Berdasarkan Jam(hr)')
fig, ax = plt.subplots()
sns.lineplot(x='hr', y='cnt', data=hour_df_cleaned, ax=ax)
ax.set_title('Distribusi Jumlah Rental Berdasarkan Jam')
st.pyplot(fig)
st.markdown("""
Distribusi jumlah rental sepeda berdasarkan jam menunjukkan adanya puncak pada jam-jam tertentu, misalnya pada pagi dan sore hari, yang mungkin mencerminkan kebiasaan berangkat dan pulang kerja menggunakan sepeda.
""")