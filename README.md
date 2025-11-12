# Bike Sharing Dashboard

<img width="1024" height="768" alt="image" src="https://github.com/user-attachments/assets/609965d4-c233-4758-ab8a-bbba27829a11" />

Bike Sharing Analysis aims to explore usage patterns, identify key factors and derive actionable insigts that can help improve service efficiency, inform marketing strategies, and predict demand.

The dataset is open source from kaggle, and this project is to fulfill Bangkit Academy's assignment.


**Key Features Analyzed**

- registered: Registered renter
- casual: Casual Renter
- temp: Temperature
- hum: Humidity
- windspeed: Kecepatan angin
- cnt: Count (Total bike rentals)
- weathersit: Weather condition
- season

**Technologies Used**

This project was built using standard Python data science libraries.

Python 3.11
Pandas: For data cleaning, manipulation, and analysis.
NumPy: For numerical operations.
Matplotlib, Seaborn: For data visualization and generating insights.
Jupyter Notebook: For exploratory data analysis (EDA) and documentation.
Streamlit: For web deploy

**Result**
<img width="1460" height="870" alt="image" src="https://github.com/user-attachments/assets/98f0a129-5240-4afd-935f-1e7797210f87" />

Registered and casual are the most important feature, this correlation is naturally high because 'cnt' is the summation of registered and casual user bike rentals.
Weathersit and windspeed are the most negative correlation, the higher the value of bad weather or high intensity of windpseed indicators the lower the number of rentals.

<img width="864" height="543" alt="image" src="https://github.com/user-attachments/assets/e351f2db-71b3-4a5f-ae16-1002014353f4" />

Rentals are higher on weekend more than weekday, it's likely that on weekends, more people rent bikes for recreational purposes.

# Bike Sharing Dashboard

How to run this code, the instruction below :

## Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_bike
cd proyek_analisis_bike
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run steamlit app
```
python -m streamlit run dashboard-bike.py
```
