import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Judul Aplikasi
st.title("Analisis Data Bike-Sharing")

# Deskripsi singkat
st.markdown("""
### Analisis ini mencakup dua visualisasi:
1. Faktor-faktor yang Mempengaruhi Jumlah Penyewaan Sepeda.
2. Perbandingan rata-rata penyewaan sepeda pada hari kerja vs akhir pekan.
""")

# Load dataset
@st.cache_data
def load_data():
    day_df = pd.read_csv("https://raw.githubusercontent.com/Ifdhal17/assignment-bangkit/refs/heads/main/day.csv")
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])  # Convert 'dteday' to datetime
    return day_df

df = load_data()

# Visualisasi 1: Faktor-faktor yang Mempengaruhi Jumlah Penyewaan Sepeda.
st.subheader("Faktor-faktor yang Mempengaruhi Jumlah Penyewaan Sepeda.")

# Memilih hanya kolom numerik untuk menghitung korelasi
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
correlation = df[numeric_columns].corr()['cnt'].sort_values(ascending=False)

# Membuat barplot untuk korelasi
plt.figure(figsize=(10, 6))
sns.barplot(x=correlation.index, y=correlation.values)
plt.title('Korelasi antara Fitur dan Jumlah Penyewaan Sepeda')
plt.xticks(rotation=45)
st.pyplot(plt)

# Visualisasi 2: Rata-rata Penyewaan Sepeda pada Hari Kerja vs Akhir Pekan
st.subheader("Rata-rata Penyewaan Sepeda: Hari Kerja vs Akhir Pekan")

# Menambahkan kolom 'is_weekend' untuk membedakan hari kerja dan akhir pekan
df['is_weekend'] = df['weekday'].apply(lambda x: 1 if x in [5, 6] else 0)

# Menghitung rata-rata penyewaan sepeda untuk hari kerja dan akhir pekan
avg_rentals = df.groupby('is_weekend')['cnt'].mean().reset_index()

# Membuat barplot untuk rata-rata penyewaan sepeda
plt.figure(figsize=(6, 4))
sns.barplot(x='is_weekend', y='cnt', data=avg_rentals)
plt.title('Rata-rata Penyewaan Sepeda: Hari Kerja vs Akhir Pekan')
plt.xticks(ticks=[0, 1], labels=['Hari Kerja', 'Akhir Pekan'])
plt.ylabel('Rata-rata Jumlah Penyewaan')
st.pyplot(plt)

# Fitur Interaktif: Perubahan Penyewaan Sepeda per Bulan
st.subheader("Perubahan Jumlah Penyewaan Sepeda per Bulan")

# Pilihan tanggal menggunakan widget kalender
start_date = st.date_input('Pilih tanggal mulai', value=df['dteday'].min(), min_value=df['dteday'].min(), max_value=df['dteday'].max())
end_date = st.date_input('Pilih tanggal akhir', value=df['dteday'].max(), min_value=df['dteday'].min(), max_value=df['dteday'].max())

# Filter data berdasarkan tanggal yang dipilih
filtered_df = df[(df['dteday'] >= pd.to_datetime(start_date)) & (df['dteday'] <= pd.to_datetime(end_date))]

# Membuat grafik perubahan jumlah penyewaan sepeda per bulan
filtered_df['month'] = filtered_df['dteday'].dt.strftime('%Y-%m')  # Mengubah 'month' menjadi string
monthly_rentals = filtered_df.groupby('month')['cnt'].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(x='month', y='cnt', data=monthly_rentals)
plt.title('Perubahan Jumlah Penyewaan Sepeda per Bulan')
plt.xticks(rotation=45)
plt.ylabel('Total Jumlah Penyewaan')
st.pyplot(plt)
