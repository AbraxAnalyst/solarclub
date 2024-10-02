import streamlit as st
import time
import pandas as pd
import numpy as np

# Set the page layout to wide mode
st.set_page_config(layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        .title {
            text-align: center;
            color: #4CAF50;
            font-size: 48px;
        }
        .subtitle {
            text-align: center;
            color: #FF5733;
            font-size: 24px;
        }
        .sidebar .sidebar-content {
            background-color: #f4f4f4;
        }
        .results {
            background-color: #e8f5e9;
            padding: 10px;
            border-radius: 5px;
        }
        .footer {
            text-align: center;
            font-size: 14px;
            color: #555;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar for general settings
with st.sidebar:
    st.title("Solar Club ⚡")
    st.markdown("### Seamless Solar Project Calculator")
    st.write("Input your project details and get a quick estimate.")
    st.image("sol.jpg", use_column_width=True)  # Add a relevant solar image URL here

# Header area
st.markdown("<h1 class='title'>Solar Energy Project Calculator</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='subtitle'>Plan your solar installation effortlessly</h4>", unsafe_allow_html=True)

# Appliance options with power ratings
appliance_options = {
    "Television": 150,  
    "Freezer": 200,     
    "Bulb": 60,         
    "Fan": 75,          
    "Laptop": 50,       
    "Air Conditioner": 1000,  
    "Refrigerator": 150, 
    "Washing Machine": 500,   
    "Microwave": 1200,        
}

# Initialize session state variables
if 'calculation_type' not in st.session_state:
    st.session_state.calculation_type = "Load Calculation"
if 'solar_data' not in st.session_state:
    st.session_state.solar_data = {}
if 'cost_benefit_data' not in st.session_state:
    st.session_state.cost_benefit_data = {}

def load_calculation():
    """Calculate the total load based on selected appliances."""
    st.markdown("## 🏠 Household Load Calculator")
    selected_appliances = {}

    for appliance, power in appliance_options.items():
        quantity = st.number_input(f"How many {appliance}s?", min_value=0, value=0, step=1)
        if quantity > 0:
            selected_appliances[appliance] = quantity

    total_load = sum(appliance_options[appliance] * quantity for appliance, quantity in selected_appliances.items())
    st.write(f"### Total Load from selected appliances: {total_load} Watts")
    return total_load

def solar_installation_calculation():
    """Calculate the solar installation requirements."""
    st.markdown("## ☀️ Solar System Specifications")

    col1, col2, col3 = st.columns(3)

    with col1:
        load_in_kWh = st.number_input("Input the Running Load in KWh", min_value=0.1, value=1.0, step=0.1)
        backup_time = st.number_input("Autonomy Hours", min_value=2, value=4, step=1)

    with col2:
        battery_voltage = st.selectbox('Battery Voltage System', [12, 24, 48], index=1)
        panel_rating = st.number_input('Solar Panel Rating (Watts)', min_value=100, value=300, step=50)

    with col3:
        sunshine = st.number_input('Sunshine Hours', min_value=4, value=5)
        seasonal_option = st.checkbox('Seasonal Variation')

    if seasonal_option:
        winter_sunshine = st.number_input('Winter Sunshine Hours', min_value=2, value=4)
        summer_sunshine = st.number_input('Summer Sunshine Hours', min_value=4, value=6)
        sunshine = (winter_sunshine + summer_sunshine) / 2  # Average seasonal sunshine

    # Calculate the project requirements based on load
    storage = load_in_kWh * backup_time * 1.6  # Safety factor
    capacity = storage / {12: 2640, 24: 5280, 48: 10560}[battery_voltage]  # Battery capacity based on voltage

    inverter_capacity = load_in_kWh + (load_in_kWh * 0.25)  # 25% buffer
    panel_array = storage / sunshine  # Required solar array
    number_of_panels = panel_array / panel_rating  # Number of panels

    # Cost estimations
    battery_cost = 300000
    panel_cost = 100000
    inverter_cost = 2000000

    total_battery_cost = round(capacity) * battery_cost
    total_panel_cost = round(number_of_panels) * panel_cost
    total_inverter_cost = inverter_cost

    if st.button('🔍 Calculate Solar', key="calculate_solar"):
        with st.spinner("Calculating..."):
            time.sleep(0.5)  # Simulating processing time
            display_results(capacity, battery_voltage, total_battery_cost, inverter_capacity, total_inverter_cost, number_of_panels, total_panel_cost, panel_rating)

def display_results(capacity, battery_voltage, total_battery_cost, inverter_capacity, total_inverter_cost, number_of_panels, total_panel_cost, panel_rating):
    """Display the calculation results."""
    st.markdown("<h2 style='text-align: center;' class='results'>Results</h2>", unsafe_allow_html=True)

    st.markdown("<h4 style='color: #1F618D;'>Battery Information</h4>", unsafe_allow_html=True)
    st.write("Number of batteries needed:", round(capacity), f"({battery_voltage}V 220Ah)")
    st.write(f"Estimated battery cost: # {total_battery_cost}")

    st.markdown("<h4 style='color: #1F618D;'>Inverter Information</h4>", unsafe_allow_html=True)
    st.write("Inverter capacity needed:", round(inverter_capacity), "kVA")
    st.write(f"Estimated inverter cost: # {total_inverter_cost}")

    st.markdown("<h4 style='color: #1F618D;'>Solar Panel Information</h4>", unsafe_allow_html=True)
    st.write(round(number_of_panels), "panels required")
    st.write(f"Panel rating: {panel_rating}W")
    st.write(f"Estimated panel cost: # {total_panel_cost}")

    st.markdown("<h3 style='color: #117A65;'>Total Estimated Cost</h3>", unsafe_allow_html=True)
    st.write(f"Total cost: # {total_battery_cost + total_panel_cost + total_inverter_cost}")

def cost_benefit_analysis():
    """Display cost-benefit analysis for solar vs. fuel costs."""
    st.markdown("<h2 style='text-align: center;'>Cost-Benefit Analysis</h2>", unsafe_allow_html=True)

    installation_cost = st.number_input("Enter the estimated cost for solar installation (currency)", min_value=0, value=10000, step=500)
    
    if 'fuel_consumption_per_hour' not in st.session_state:
        st.session_state.fuel_consumption_per_hour = 2.0
    if 'fuel_price_per_liter' not in st.session_state:
        st.session_state.fuel_price_per_liter = 1.0
    if 'usage_hours_per_day' not in st.session_state:
        st.session_state.usage_hours_per_day = 8.0

    fuel_consumption_per_hour = st.number_input("Enter fuel consumption of current system (liters/hour)", min_value=0.0, value=st.session_state.fuel_consumption_per_hour, step=1.0)
    fuel_price_per_liter = st.number_input("Enter current fuel price (currency per liter)", min_value=0.0, value=st.session_state.fuel_price_per_liter, step=1.0)
    usage_hours_per_day = st.number_input("Enter usage hours per day", min_value=0.0, value=st.session_state.usage_hours_per_day, step=1.0)

    st.session_state.fuel_consumption_per_hour = fuel_consumption_per_hour
    st.session_state.fuel_price_per_liter = fuel_price_per_liter
    st.session_state.usage_hours_per_day = usage_hours_per_day

    days_per_month = 30
    monthly_fuel_cost = fuel_consumption_per_hour * fuel_price_per_liter * usage_hours_per_day * days_per_month

    total_solar_system_cost = installation_cost

    if st.button('🔍 Calculate Cost-Benefit', key="calculate_cost_benefit"):
        with st.spinner("Calculating..."):
            time.sleep(0.5)  # Simulating processing time
            st.write("### Total Solar System Cost: #", total_solar_system_cost)
            st.write("### Monthly Fuel Cost: #", monthly_fuel_cost)

            payback_period_months = total_solar_system_cost / monthly_fuel_cost if monthly_fuel_cost > 0 else float('inf')
            st.write("### Estimated Payback Period (in months):", round(payback_period_months))

            annual_savings = monthly_fuel_cost * 12
            st.write("### Estimated Annual Savings from Solar: #", annual_savings)

# Main logic to choose calculation type
st.session_state.calculation_type = st.radio("Choose a Calculation Type", ("Home", "Load Calculation", "Solar Installation Calculation", "Cost-Benefit Analysis"))

if st.session_state.calculation_type == "Home":
    st.markdown("## Welcome to the Solar Club! 🌞")
    st.write("This application helps you calculate and analyze the cost and benefits of solar energy installations. Choose a calculation type from the navigation bar on the left.")
    st.write("### Features:")
    st.write("- **Load Calculation**: Estimate your household energy load.")
    st.write("- **Solar Installation Calculation**: Determine the specifications for your solar setup.")
    st.write("- **Cost-Benefit Analysis**: Analyze the financial benefits of solar energy.")
elif st.session_state.calculation_type == "Load Calculation":
    load_calculation()
elif st.session_state.calculation_type == "Solar Installation Calculation":
    solar_installation_calculation()
elif st.session_state.calculation_type == "Cost-Benefit Analysis":
    cost_benefit_analysis()

# Footer with contact info
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<footer class='footer'>"
    "<p><strong>Solar Club</strong> - Making your solar projects easier. For more information, visit our website or contact support.</p>"
    "</footer>", 
    unsafe_allow_html=True
)
