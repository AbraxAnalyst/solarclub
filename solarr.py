import streamlit as st
import time

# Set the page layout to wide mode
st.set_page_config(layout="wide")

# Sidebar for general settings
with st.sidebar:
    st.title("Solar Club ⚡")
    st.markdown("### Seamless Solar Project Calculator")
    st.write("Input your project details and get a quick estimate.")
    st.image("sol.jpg", use_column_width=True)  # Add a relevant solar image URL here

# Header area
st.markdown("<h1 style='text-align: center; color: green;'>Solar Energy Project Calculator</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #FF5733;'>Plan your solar installation effortlessly</h4>", unsafe_allow_html=True)

# Dividing layout into columns for better organization
col1, col2, col3 = st.columns(3)

with col1:
    load = st.number_input("Load in KWh", min_value=100, value=500, step=50, help="Total energy consumption in kilowatt-hours")
    Back_up_time = st.number_input("Autonomy Hours", min_value=2, value=4, step=1, help="How many hours of backup you want")
    
with col2:
    Battery_volt = st.selectbox('Battery Voltage System', [12, 24, 48], index=1, help="Choose the voltage system for your battery")
    panel_rating = st.number_input('Solar Panel Rating (Watts)', min_value=100, value=300, step=50, help="Input your solar panel wattage")

with col3:
    sunshine = st.number_input('Sunshine Hours', min_value=4, value=5, help="Number of hours of sunlight in your region")
    seasonal_option = st.checkbox('Seasonal Variation', help="Check this box if you want to account for sunshine variations")

# Additional inputs for seasonal sunshine variation
if seasonal_option:
    winter_sunshine = st.number_input('Winter Sunshine Hours', min_value=2, value=4)
    summer_sunshine = st.number_input('Summer Sunshine Hours', min_value=4, value=6)
    avg_seasonal_sunshine = (winter_sunshine + summer_sunshine) / 2
    sunshine = avg_seasonal_sunshine

# Calculate the project requirements
storage = load * Back_up_time * 1.6
if Battery_volt == 12:
    capacity = storage / 2640
elif Battery_volt == 24:
    capacity = storage / 5280
else:
    capacity = storage / 10560

Inverter_capacity = load + (load * 0.25)
panel_array = storage / sunshine
number_of_panels = panel_array / panel_rating

# Cost estimations (optional)
battery_cost = 220
panel_cost = 150
inverter_cost = 1000

total_battery_cost = round(capacity) * battery_cost
total_panel_cost = round(number_of_panels) * panel_cost
total_inverter_cost = inverter_cost

# Calculation button
if st.button('Calculate'):
    # Progress bar for better user experience
    progress_text = "Analyzing your data, please wait..."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)

    my_bar.empty()

    # Output area with formatted results
    st.markdown("<h2 style='text-align: center;'>Results</h2>", unsafe_allow_html=True)

    st.markdown("<h4 style='color: #1F618D;'>Battery Information</h4>", unsafe_allow_html=True)
    st.write("Number of batteries needed:", round(capacity), f"({Battery_volt}V 220Ah)")
    st.write(f"Estimated battery cost: ${total_battery_cost}")

    st.markdown("<h4 style='color: #1F618D;'>Inverter Information</h4>", unsafe_allow_html=True)
    st.write("Inverter capacity needed:", round(Inverter_capacity), "kVA")
    st.write(f"Estimated inverter cost: ${total_inverter_cost}")

    st.markdown("<h4 style='color: #1F618D;'>Solar Panel Information</h4>", unsafe_allow_html=True)
    st.write(round(number_of_panels), "panels required")
    st.write(f"Panel rating: {panel_rating}W")
    st.write(f"Estimated panel cost: ${total_panel_cost}")

    st.markdown("<h3 style='color: #117A65;'>Total Estimated Cost</h3>", unsafe_allow_html=True)
    st.write(f"Total cost: ${total_battery_cost + total_panel_cost + total_inverter_cost}")

# Footer with contact info
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<footer style='text-align: center;'>"
    "<p><strong>Solar Club</strong> - Making your solar projects easier. For more information, visit our website or contact support.</p>"
    "</footer>", 
    unsafe_allow_html=True
)
