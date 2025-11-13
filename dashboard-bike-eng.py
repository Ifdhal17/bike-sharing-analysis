import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Page configurations
st.set_page_config(
    page_title="Bike Sharing Analysis",
    page_icon="🚴",
    layout="wide"
)

# Application Title
st.title("🚴 Bike Sharing Analysis")

# Short Description
st.markdown("""
### 📊 The Analysis Covers:
1. **Factors** influencing bike rental counts
2. **Comparison** of average rentals on weekdays vs weekends
3. **Trend** of bike rentals over time with interactive date selection
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

# Sidebar for dataset information
with st.sidebar:
    start_date = df['dteday'].min().strftime('%Y-%m-%d')
    end_date = df['dteday'].max().strftime('%Y-%m-%d')
    st.header("Dataset Info")
    st.metric("Total Records", len(df))
    st.markdown("Data Period:")
    st.markdown(f"**{start_date} - \n{end_date}**")
    st.metric("Total Rentals", f"{df['cnt'].sum():,}")
    
    with st.expander("📖 Feature Explanation"):
        st.markdown("""
        - **registered**: Registered users
        - **casual**: Casual users
        - **temp**: Normalized temperature
        - **hum**: Normalized humidity
        - **windspeed**: Normalized wind speed
        - **cnt**: Total bike rentals
        - **weathersit**: Weather situation
        - **season**: Season 
        """)

# Main Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📈 Average Rentals/Day", f"{df['cnt'].mean():.0f}")
with col2:
    st.metric("📊 Median Rentals", f"{df['cnt'].median():.0f}")
with col3:
    st.metric("🔝 Highest Rentals", f"{df['cnt'].max():,}")

st.markdown("---")

# Visualization 1: Factors Influencing the Number of Bike Rentals
st.subheader("1. Factors Influencing the Number of Bike Rentals")

col1, col2 = st.columns([2, 1])

with col1:
    # Selecting only numeric columns to calculate correlation
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    correlation = df[numeric_columns].corr()['cnt'].drop('cnt').sort_values(ascending=False)
    
    # Creating a barplot for correlation
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['green' if x > 0 else 'red' for x in correlation.values]
    sns.barplot(x=correlation.values, y=correlation.index, palette=colors, ax=ax)
    ax.set_title('Feature Correlation with Total Bike Rentals', fontsize=14, fontweight='bold')
    ax.set_ylabel('Feature')
    ax.set_xlabel('Correlation Coefficient')
    ax.axvline(x=0, color='black', linestyle='--', linewidth=0.8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with col2:
    st.markdown("### 💡 Insight")
    top_factor = correlation.idxmax()
    top_value = correlation.max()
    st.success(f"**Strongest Factor:** `{top_factor}` with a correlation of **{top_value:.3f}**")
    
    st.markdown("""
    **Interpretation:**
    - Positive correlation (green) = increases rentals
    - Negative correlation (red) = decreases rentals
    - The longer the bar, the stronger the influence
    """)

st.markdown("---")

# Visualization 2: Average Bike Rentals on Weekdays vs Weekends
st.subheader("2. Average Bike Rentals: Weekdays vs Weekends")

col1, col2 = st.columns([2, 1])

with col1:
    # Adding 'is_weekend' column (weekday 0-6: 0=Sun, 6=Sat. Weekends usually [6, 0])
    # Based on the user's initial code, it seems the definition of weekend is [5, 6] (Fri, Sat) or perhaps [6, 0] (Sat, Sun) where 0=Sun, 1=Mon... 6=Sat.
    # I will assume standard definition where 0=Sun, 1=Mon, ..., 6=Sat. Weekday is 1-5, Weekend is 0 (Sun) and 6 (Sat).
    # Based on the code: `df['weekday'].apply(lambda x: 1 if x in [5, 6] else 0)` where 5=Fri, 6=Sat. Let's stick to the original logic [5, 6] for weekend for consistency.
    # Note: If the dataset uses 0=Sunday, 1=Monday, ... 6=Saturday, then [5, 6] means Friday and Saturday. 
    df['is_weekend'] = df['weekday'].apply(lambda x: 1 if x in [5, 6] else 0)
    
    # Calculating average rentals
    avg_rentals = df.groupby('is_weekend')['cnt'].mean().reset_index()
    avg_rentals['category'] = avg_rentals['is_weekend'].map({0: 'Weekday', 1: 'Weekend'})
    
    # Creating a barplot
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = sns.barplot(x='category', y='cnt', data=avg_rentals, palette=['#3498db', '#e74c3c'], ax=ax)
    ax.set_title('Comparison of Average Bike Rentals', fontsize=14, fontweight='bold')
    ax.set_ylabel('Average Rental Count')
    ax.set_xlabel('')
    
    # Add value labels
    for container in ax.containers:
        ax.bar_label(container, fmt='%.0f', padding=3)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with col2:
    st.markdown("### 📊 Statistics")
    weekday_avg = avg_rentals[avg_rentals['is_weekend'] == 0]['cnt'].values[0]
    weekend_avg = avg_rentals[avg_rentals['is_weekend'] == 1]['cnt'].values[0]
    difference = weekday_avg - weekend_avg
    pct_diff = (difference / weekend_avg) * 100
    
    st.metric("Weekday", f"{weekday_avg:.0f}")
    st.metric("Weekend", f"{weekend_avg:.0f}", 
              delta=f"{difference:.0f} ({pct_diff:+.1f}%)", 
              delta_color="inverse")
    
    if weekday_avg > weekend_avg:
        st.info("✅ Rentals are higher on **weekdays**, likely used for commuting to work/school.")
    else:
        st.info("✅ Rentals are higher on **weekends**, likely used for leisure activities.")

st.markdown("---")

# Interactive Feature: Change in Bike Rentals per Month
st.subheader("3. Trend of Bike Rentals Over Time")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input(
        '📅 Select Start Date', 
        value=df['dteday'].min().date(), 
        min_value=df['dteday'].min().date(), 
        max_value=df['dteday'].max().date()
    )
with col2:
    end_date = st.date_input(
        '📅 Select End Date', 
        value=df['dteday'].max().date(), 
        min_value=df['dteday'].min().date(), 
        max_value=df['dteday'].max().date()
    )

# Date input validation
if start_date > end_date:
    st.error("⚠️ Start date cannot be later than end date!")
    st.stop()

# Filter data based on selected dates
filtered_df = df[(df['dteday'] >= pd.to_datetime(start_date)) & 
                 (df['dteday'] <= pd.to_datetime(end_date))]

if filtered_df.empty:
    st.warning("📭 No data available for the selected date range.")
else:
    # Statistics for the selected period
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Days", len(filtered_df))
    with col2:
        st.metric("Total Rentals", f"{filtered_df['cnt'].sum():,}")
    with col3:
        st.metric("Average/Day", f"{filtered_df['cnt'].mean():.0f}")
    with col4:
        st.metric("Peak Day", f"{filtered_df['cnt'].max():,}")
    
    # Creating a graph of changes in bike rentals per month
    filtered_df['month'] = filtered_df['dteday'].dt.to_period('M').astype(str)
    monthly_rentals = filtered_df.groupby('month')['cnt'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='month', y='cnt', data=monthly_rentals, marker='o', 
                 linewidth=2.5, markersize=8, color='#2ecc71', ax=ax)
    ax.fill_between(range(len(monthly_rentals)), monthly_rentals['cnt'], alpha=0.3, color='#2ecc71')
    ax.set_title('Trend of Total Bike Rentals per Month', fontsize=14, fontweight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Total Rental Count', fontsize=12)
    ax.grid(True, alpha=0.3, linestyle='--')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    # Trend insight
    if len(monthly_rentals) > 1:
        trend = "increased" if monthly_rentals['cnt'].iloc[-1] > monthly_rentals['cnt'].iloc[0] else "decreased"
        st.info(f"📈 The bike rental trend has **{trend}** from {monthly_rentals['month'].iloc[0]} to {monthly_rentals['month'].iloc[-1]}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>📊 Bike Sharing Analysis Dashboard | Bangkit Academy Assignment</p>
</div>
""", unsafe_allow_html=True)