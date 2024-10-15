import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Load data
day_df_cleaned = pd.read_csv('day_df_cleaned.csv')
hour_df_cleaned = pd.read_csv('hour_df_cleaned.csv')

# Map categorical values to names
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
    5: 'Jumat',
    6: 'Sabtu'
})

# Title
st.title('Analisis Rental Sepeda berdasarkan Faktor Cuaca dan Waktu')

# Interactive filters
st.sidebar.header('Filter Data')

# Filter by season
selected_season = st.sidebar.selectbox(
    'Pilih Musim:', 
    options=['Semua'] + day_df_cleaned['season'].unique().tolist(),
    index=0
)

# Filter by weekday
selected_weekday = st.sidebar.selectbox(
    'Pilih Hari dalam Minggu:',
    options=['Semua'] + day_df_cleaned['weekday'].unique().tolist(),
    index=0
)

# Apply filters
filtered_data = day_df_cleaned.copy()

if selected_season != 'Semua':
    filtered_data = filtered_data[filtered_data['season'] == selected_season]

if selected_weekday != 'Semua':
    filtered_data = filtered_data[filtered_data['weekday'] == selected_weekday]


# --- Visualisasi Day Data ---
st.header('Visualisasi Data Berdasarkan Faktor Cuaca')

# Grouped data by season
grouped_season_df = filtered_data.groupby('season').agg({
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

# --- Plot Hubungan Feeling Temperature dengan Jumlah Rental Per Hari ---
st.subheader('Hubungan Feeling Temperature(atemp) dengan Jumlah Rental(cnt) Per Hari')
fig, ax = plt.subplots()
sns.regplot(x='atemp', y='cnt', data=filtered_data)
ax.set_title('Hubungan Feeling Temperature dengan Jumlah Rental Per Hari')
st.pyplot(fig)

# --- Plot Hubungan Kecepatan Angin dengan Jumlah Rental Per Hari ---
st.subheader('Hubungan Kecepatan Angin(windspeed) dengan Jumlah Rental(cnt) Per Hari')
fig, ax = plt.subplots()
sns.regplot(x='windspeed', y='cnt', data=filtered_data)
ax.set_title('Hubungan Kondisi Cuaca dengan Jumlah Rental Per Hari')
y_min = filtered_data['cnt'].min()
y_max = filtered_data['cnt'].max()
ax.set_ylim(y_min, y_max)
st.pyplot(fig)

# --- Plot Hubungan Kondisi Cuaca dengan Jumlah Rental Per Hari ---
st.subheader('Hubungan Kondisi Cuaca(weathersit) dengan Jumlah Rental(cnt) Per Hari')
fig, ax = plt.subplots()
sns.scatterplot(x='weathersit', y='cnt', data=filtered_data, s=10)
ax.set_title('Hubungan Kondisi Cuaca dengan Jumlah Rental Per Hari')
ax.set_ylim(y_min, y_max)
st.pyplot(fig)

# --- Visualisasi Berdasarkan Waktu ---
st.header('Visualisasi Data Berdasarkan Waktu')

grouped_weekday_df = filtered_data.groupby('weekday').agg({
    'cnt': ['mean', 'max', 'min']
}).reset_index()

grouped_weekday_df.columns = ['weekday', 'Rata-Rata', 'Maksimum', 'Minimum']
urutan = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']

grouped_weekday_df['weekday'] = pd.Categorical(grouped_weekday_df['weekday'], categories=urutan, ordered=True)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=grouped_weekday_df.melt(id_vars='weekday', var_name='statistic', value_name='cnt_value'),
            x='weekday', y='cnt_value', hue='statistic')
ax.set_title('Rata-rata, Maksimum, dan Minimum Jumlah Rental per Hari dalam Seminggu')
ax.set_xlabel('Hari dalam Minggu')
ax.set_ylabel('Jumlah Rental')
st.pyplot(fig)

# --- Distribusi Jumlah Rental Berdasarkan Jam ---
st.subheader('Distribusi Jumlah Rental(cnt) Berdasarkan Jam(hr)')
fig, ax = plt.subplots()
sns.lineplot(x='hr', y='cnt', data=hour_df_cleaned, ax=ax)
ax.set_title('Distribusi Jumlah Rental Berdasarkan Jam')
st.pyplot(fig)
