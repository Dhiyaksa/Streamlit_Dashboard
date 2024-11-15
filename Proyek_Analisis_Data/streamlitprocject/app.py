import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

#Memanggil data yang sudah dibersihkan dan menyimpannya ke dalam variable df

df = pd.read_csv('C:/Proyek_Analisis_Data/streamlitprocject/Sharing_Bike_Clean.csv')

#Mengubah tipe data kolom dteday menjadi tipe data datetime 
df['dteday'] = pd.to_datetime(df['dteday'])

#Membuat pivot table dengan mengelompokan jumlah perental sepeda berdasarkan
#Musim dan cuaca dan menyimpannya ke dalam variable season_corr
season_corr = df.groupby([df['season'], df['weathersit']]).agg({'cnt': 'sum'})


#Membuat tabel perbandingan jumlah perental sepeda casual dan teregistrasi berdasarkan
#Musim dan menyimpannya ke dalam variabel user_comparison
user_comparison = df.groupby('season').agg({'casual': 'sum', 'registered': 'sum'}).reset_index()


#Membuat tabel perbandingan pengguna rental sepeda casual dan registered beradasarkan
# Hari libur dan hari kerja dan menyimpannya ke dalam variabel workingday_comparison
workingday_comparison = df.groupby('workingday').agg({'casual': 'sum', 'registered': 'sum'}).reset_index()


#menngambil bulan dari kolom dteaday
df['month'] = df['dteday'].dt.to_period('M')

#mengelompokan jumlah penyewa casual dan registered berdasarkan 24 bulan dan menyimpannya dalam variable user_trend
user_trend = df.groupby('month').agg({'casual': 'sum', 'registered': 'sum'}).reset_index()

#mengubah format yyyy-mm menjadi bulan saja dari 1-24
user_trend['month'] = range(1, len(user_trend) + 1)

#mengatur ulang kolom yang berada dalam variabel user_trend
user_trend = user_trend[['month', 'casual', 'registered']]


#Membuat Judul
st.header('Bike Sharing Dashboard')

#Membuat penjelasan mengenai value dalam variabel season
with st.expander('Explanation for season'):
   st.caption('1 (Springer), 2(Summer), 3(Fall), 4(Winter)')

#Membuat penjelasan mengenai value dalam variabel weathersit
with st.expander('Explanation for Weathersit'):
   st.caption('''1 (Clear, Few clouds, Partly cloudy, Partly cloudy),
           2 (Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist),
           3 (Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds)
           4 (Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog)
            ''')

#Membuat penjelasan mengenai value dari variabel workingday
with st.expander('Explanation for workingday'):
   st.caption('0 (Holiday), 1 (Workingday)')

#Membuat tiga kolom
col1, col2, col3 = st.columns(3)

#Membuat kolom pertama
with col1:
   #Menampilkan jumlah total user casual
   casual_users = df['casual'].sum()
   st.metric('Total Casual Users', value=casual_users)

   ##Membuat Scatterplot untuk melihat pengaruh Musim dan Cuaca terhadap Jumlah Penyewa Sepeda
   fig, ax = plt.subplots()
   sns.scatterplot(x='season', y='cnt', hue='weathersit', data=season_corr, ax=ax)
   plt.title('Correlation Between Season and Weather to Bik Rental')
   plt.xlabel('Season')
   plt.ylabel('Bike Rental')
   st.pyplot(fig)

   #Memberi penjelasan insight dari grafik di atas
   with st.expander('See Explanantion'):
      st.markdown('''Most of users rent bikes when the weather is
               Clear, Few clouds, Partly cloudy, Partly cloudy, especially in fall.
               ''')

#Membuat kolom ke-2
with col2:
   #Menampilkan jumlah total user registered
   registered_users = df['registered'].sum()
   st.metric('Total Regsitered Users', value=registered_users)

   #Membuat grafik perbandingan jumlah penyewa casual dan registrered berdasarkan musim
   fig, ax = plt.subplots()
   width = 0.35
   ax.bar(user_comparison['season'] - width/2, user_comparison['casual'], width, label='Casual')
   ax.bar(user_comparison['season'] + width/2, user_comparison['registered'], width, label='Registered')
   ax.set_xlabel('Season')
   ax.set_ylabel('User Bike Rental')
   ax.set_title('User Comparison Based on Season')
   ax.set_xticks(user_comparison['season'])
   ax.legend()
   st.pyplot(fig)

   #Membuat penjelasan insight dari grafik di atas
   with st.expander('See Explanation'):
      st.markdown('Both of users mostly rent bike in fall season.')
   
#Membuat kolom ke-3
with col3:
   #Menampilkan jumlah total dari user
   cnt_users = df['cnt'].sum()
   st.metric('Total Users', value=cnt_users)

   #Membuat grafik perbandingan jumlah penyewa casual dan registrered berdasarkan
   #hari libur dan hari kerja
   fig, ax = plt.subplots()
   width = 0.35
   ax.bar(workingday_comparison['workingday'] - width/2, workingday_comparison['casual'], width, label='Casual')
   ax.bar(workingday_comparison['workingday'] + width/2, workingday_comparison['registered'], width, label='Registered')
   ax.set_xlabel('Season')
   ax.set_ylabel('User Bike Rental')
   ax.set_title('Workingday Comparison Based on Season')
   ax.set_xticks(workingday_comparison['workingday'])
   ax.legend()
   st.pyplot(fig)

   #Membuat penjelasan insight dari grafik di atas
   with st.expander('See Explanation'):
      st.markdown('''There is a differences behaviour of users. Most of casual users rent
                  bike on holiday, and most of registered users rent biks on workingday.
                  ''')

#Membuat Container
with st.container():
   #Membuat line chart untuk melihat trend jumlah user selama 24 bulan
   fig, ax = plt.subplots()
   ax.plot(user_trend['month'], user_trend['casual'], user_trend['registered'])
   ax.set_xlabel('Month')
   ax.set_ylabel('Users Bike Rental')
   ax.set_title('Users Bike Rental Trend in 24 Months')
   ax.legend(['casual', 'registered'])
   ax.set_xticks(range(1,28,3))
   st.pyplot(fig)

   #Membuat penjelasan insight dari grafik di atas
   with st.expander('See Explanation'):
      st.markdown('''Trend of both of users is still fluctuating
                  with the same pattern
                  ''')

#Membuat sidebar
with st.sidebar:
  #Menentukan tanggal awal dan tanggal akhir
  min_date = df['dteday'].min()
  max_date = df['dteday'].max()
  
  #Membuat inputan tanggal
  selected_date = st.date_input("Select a date:", min_value=min_date, max_value=max_date, value=min_date)
  
  # Memfilter data berdasarkan tanggal yang dipilih
  user_filtered = df[df['dteday'] == pd.to_datetime(selected_date)]
  
  #Menampilkan jumlah user casual dan registered berdasarkan tanggal yang dipilih
  if not user_filtered.empty:
    casual_count = user_filtered['casual'].iloc[0]
    registered_count = user_filtered['registered'].iloc[0]
    st.metric('Casual Users', value=casual_count)
    st.metric('Registered Users', value=registered_count)
  else:
     st.write('Choose the right date')
