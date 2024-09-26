import streamlit as st 
import math 
import time

st.title('Solar Club ')
st.write('Do your project calculation seamlesly ')
load = st.number_input("Input the Running Load in 'KWh'", min_value= 100)
Back_up_time =st.number_input("How many hours of Autonomy do you want", min_value= 2)
Battery_volt = st.selectbox('What Battery voltage system do you want, 12V,24V,48V', [12,24,48])
panel_rating = st.number_input('What is the rating of your panel in Watts', min_value= 100)
sunshine = st.number_input('Input hours of sunshine to be considered (Default: 5Hours)', min_value= 4,  )

# Lets calculate the Number of battery Needed for this system 
storage = load * Back_up_time * 1.6 
if Battery_volt == 12:
    capacity = storage/2640
elif Battery_volt == 24:
    capacity = storage/5280
else:
    capacity = storage/ 10560
 
 
 # Sizing the inverter is a very good thing todo
Inverter_capacity = load + (load * .25)   

# Lets talk about the number of solar panels needed 
#Using 5 hours of sunshine 

panel_array = storage/sunshine
number_of_panels = panel_array/panel_rating

if st.button('Calculate '):
     progress_text = "Analyzing your Data  Please wait....."
     my_bar = st.progress(0, text=progress_text)

     for percent_complete in range(100):
         time.sleep(0.01)
         my_bar.progress(percent_complete + 1, text=progress_text)
            
     time.sleep(1)
     my_bar.empty()
     
     st.write("BATTERY INFO:")
     st.write("Number of battery needed: ", round(capacity),  "of", Battery_volt,  "V 220Ah")
     st.write('INVERTER CAPACITY')
     st.write('The size of Inverter for this project is: ', round(Inverter_capacity), "kVA")
     st.write('SOLAR PANEL INFO:')
     st.write(round(number_of_panels)," Panels")
     st.write("Rating in Watts : ", panel_rating)
    