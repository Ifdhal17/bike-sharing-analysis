import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(
    page_title="Analisis Bike Sharing",
    page_icon="🚴",
    layout="wide"
)

# Judul Aplikasi
st.title("🚴 Analisis Data Bike Sharing")

# Deskripsi singkat
st.markdown("""
### 📊 Analisis ini mencakup:
1. **Faktor-faktor** yang mempengaruhi jumlah penyewaan sepeda
2. **Perbandingan** penyewaan pada hari kerja vs akhir pekan
3. **Trend** perubahan penyewaan sepeda dari waktu ke waktu
""")

# Load dataset
@st.cache_data
def load_data():
    try:
        day_df = pd.read_csv("https://raw.githubusercontent.com/Ifdhal17/assignment-bangkit/refs/heads/main/day.csv")
        day_df['dteday'] = pd.to_datetime(day_df['dteday'])
        return day_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_data()

if df is None:
    st.stop()

# Sidebar untuk informasi dataset
with st.sidebar:
    start_date = df['dteday'].min().strftime('%Y-%m-%d')
    end_date = df['dteday'].max().strftime('%Y-%m-%d')
    st.header("Info Dataset")
    st.metric("Total Records", len(df))
    st.markdown("Periode Data:")
    st.markdown(f"**{start_date} - \n{end_date}**")
    st.metric("Total Penyewaan", f"{df['cnt'].sum():,}")
    
    with st.expander("📖 Penjelasan Fitur"):
        st.markdown("""
        - **registered**: Penyewa terdaftar
        - **casual**: Penyewa biasa
        - **temp**: Suhu 
        - **hum**: Kelembaban 
        - **windspeed**: Kecepatan angin 
        - **cnt**: Total penyewaan sepeda
        - **weathersit**: Situasi cuaca
        - **season**: Musim 
        """)

# Metrics utama
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📈 Rata-rata Penyewaan/Hari", f"{df['cnt'].mean():.0f}")
with col2:
    st.metric("📊 Median Penyewaan", f"{df['cnt'].median():.0f}")
with col3:
    st.metric("🔝 Penyewaan Tertinggi", f"{df['cnt'].max():,}")

st.markdown("---")

# Visualisasi 1: Faktor-faktor yang Mempengaruhi Jumlah Penyewaan Sepeda
st.subheader("1. Faktor-faktor yang Mempengaruhi Jumlah Penyewaan Sepeda")

col1, col2 = st.columns([2, 1])

with col1:
    # Memilih hanya kolom numerik untuk menghitung korelasi
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    correlation = df[numeric_columns].corr()['cnt'].drop('cnt').sort_values(ascending=False)
    
    # Membuat barplot untuk korelasi
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['green' if x > 0 else 'red' for x in correlation.values]
    sns.barplot(x=correlation.values, y=correlation.index, palette=colors, ax=ax)
    ax.set_title('Korelasi Fitur dengan Jumlah Penyewaan Sepeda', fontsize=14, fontweight='bold')
    ax.set_xlabel('Koefisien Korelasi')
    ax.axvline(x=0, color='black', linestyle='--', linewidth=0.8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with col2:
    st.markdown("### 💡 Insight")
    top_factor = correlation.idxmax()
    top_value = correlation.max()
    st.success(f"**Faktor terkuat:** `{top_factor}` dengan korelasi **{top_value:.3f}**")
    
    st.markdown("""
    **Interpretasi:**
    - Korelasi positif (hijau) = meningkatkan penyewaan
    - Korelasi negatif (merah) = menurunkan penyewaan
    - Semakin panjang bar, semakin kuat pengaruhnya
    """)

st.markdown("---")

# Visualisasi 2: Rata-rata Penyewaan Sepeda pada Hari Kerja vs Akhir Pekan
st.subheader("2. Rata-rata Penyewaan Sepeda: Hari Kerja vs Akhir Pekan")

col1, col2 = st.columns([2, 1])

with col1:
    # Menambahkan kolom 'is_weekend'
    df['is_weekend'] = df['weekday'].apply(lambda x: 1 if x in [5, 6] else 0)
    
    # Menghitung rata-rata penyewaan
    avg_rentals = df.groupby('is_weekend')['cnt'].mean().reset_index()
    avg_rentals['category'] = avg_rentals['is_weekend'].map({0: 'Hari Kerja', 1: 'Akhir Pekan'})
    
    # Membuat barplot
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = sns.barplot(x='category', y='cnt', data=avg_rentals, palette=['#3498db', '#e74c3c'], ax=ax)
    ax.set_title('Perbandingan Rata-rata Penyewaan Sepeda', fontsize=14, fontweight='bold')
    ax.set_ylabel('Rata-rata Jumlah Penyewaan')
    ax.set_xlabel('')
    
    # Tambahkan value labels
    for container in ax.containers:
        ax.bar_label(container, fmt='%.0f', padding=3)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with col2:
    st.markdown("### 📊 Statistik")
    weekday_avg = avg_rentals[avg_rentals['is_weekend'] == 0]['cnt'].values[0]
    weekend_avg = avg_rentals[avg_rentals['is_weekend'] == 1]['cnt'].values[0]
    difference = weekday_avg - weekend_avg
    pct_diff = (difference / weekend_avg) * 100
    
    st.metric("Hari Kerja", f"{weekday_avg:.0f}")
    st.metric("Akhir Pekan", f"{weekend_avg:.0f}", 
              delta=f"{difference:.0f} ({pct_diff:+.1f}%)", 
              delta_color="inverse")
    
    if weekday_avg > weekend_avg:
        st.info("✅ Penyewaan lebih tinggi pada **hari kerja**, kemungkinan digunakan untuk transportasi ke kantor/sekolah.")
    else:
        st.info("✅ Penyewaan lebih tinggi pada **akhir pekan**, kemungkinan untuk healing.")

st.markdown("---")

# Fitur Interaktif: Perubahan Penyewaan Sepeda per Bulan
st.subheader("3. Trend Penyewaan Sepeda dari Waktu ke Waktu")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input(
        '📅 Pilih tanggal mulai', 
        value=df['dteday'].min().date(), 
        min_value=df['dteday'].min().date(), 
        max_value=df['dteday'].max().date()
    )
with col2:
    end_date = st.date_input(
        '📅 Pilih tanggal akhir', 
        value=df['dteday'].max().date(), 
        min_value=df['dteday'].min().date(), 
        max_value=df['dteday'].max().date()
    )

# Validasi input tanggal
if start_date > end_date:
    st.error("⚠️ Tanggal mulai tidak boleh lebih besar dari tanggal akhir!")
    st.stop()

# Filter data berdasarkan tanggal yang dipilih
filtered_df = df[(df['dteday'] >= pd.to_datetime(start_date)) & 
                 (df['dteday'] <= pd.to_datetime(end_date))]

if filtered_df.empty:
    st.warning("📭 Tidak ada data untuk rentang tanggal yang dipilih.")
else:
    # Statistik periode terpilih
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Hari", len(filtered_df))
    with col2:
        st.metric("Total Penyewaan", f"{filtered_df['cnt'].sum():,}")
    with col3:
        st.metric("Rata-rata/Hari", f"{filtered_df['cnt'].mean():.0f}")
    with col4:
        st.metric("Peak Day", f"{filtered_df['cnt'].max():,}")
    
    # Membuat grafik perubahan jumlah penyewaan sepeda per bulan
    filtered_df['month'] = filtered_df['dteday'].dt.to_period('M').astype(str)
    monthly_rentals = filtered_df.groupby('month')['cnt'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='month', y='cnt', data=monthly_rentals, marker='o', 
                 linewidth=2.5, markersize=8, color='#2ecc71', ax=ax)
    ax.fill_between(range(len(monthly_rentals)), monthly_rentals['cnt'], alpha=0.3, color='#2ecc71')
    ax.set_title('Trend Jumlah Penyewaan Sepeda per Bulan', fontsize=14, fontweight='bold')
    ax.set_xlabel('Bulan', fontsize=12)
    ax.set_ylabel('Total Jumlah Penyewaan', fontsize=12)
    ax.grid(True, alpha=0.3, linestyle='--')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    # Insight trend
    if len(monthly_rentals) > 1:
        trend = "meningkat" if monthly_rentals['cnt'].iloc[-1] > monthly_rentals['cnt'].iloc[0] else "menurun"
        st.info(f"📈 Trend penyewaan sepeda **{trend}** dari {monthly_rentals['month'].iloc[0]} ke {monthly_rentals['month'].iloc[-1]}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>📊 Dashboard Analisis Bike Sharing | Assignment Bangkit Academy</p>
</div>
""", unsafe_allow_html=True)
