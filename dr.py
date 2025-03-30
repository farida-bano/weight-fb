import streamlit as st
from datetime import datetime

# Unit symbols dictionary
unit_symbols = {
    "Meters": "m",
    "Kilometers": "km",
    "Miles": "mi",
    "Inches": "in",
    "Centimeters": "cm",
    "Kilograms": "kg",
    "Pounds": "lbs",
    "Grams": "g",
    "Ounces": "oz",
}

# Conversion categories
conversion_categories = {
    "Baby Weight Estimation": ["Baby Weight Estimation"],
    "Length/Distance": ["Meters to Kilometers", "Miles to Kilometers", "Inches to Centimeters"],
    "Mass/Weight": ["Kilograms to Pounds", "Grams to Ounces"],
}

# Conversion functions
def CONVERSIONS(conversion_type):
    def meters_to_kilometers(value):
        return value / 1000
    
    def miles_to_kilometers(value):
        return value * 1.60934  # Corrected conversion
    
    def inches_to_centimeters(value):
        return value * 2.54
    
    def kilograms_to_pounds(value):
        return value * 2.20462
    
    def grams_to_ounces(value):
        return value / 28.3495
    
    return {
        "Meters to Kilometers": meters_to_kilometers,
        "Miles to Kilometers": miles_to_kilometers,
        "Inches to Centimeters": inches_to_centimeters,
        "Kilograms to Pounds": kilograms_to_pounds,
        "Grams to Ounces": grams_to_ounces,
    }.get(conversion_type)

# Baby weight estimation (improved formula)
def estimated_baby_weight(mother_weight, gestational_weeks):
    base_weight = 3.0  # kg (average base weight)
    weekly_gain = 0.15  # kg per week after 24 weeks
    return base_weight + (gestational_weeks - 24) * weekly_gain

def main():
    # Set page config
    st.set_page_config(page_title="Baby & Baba Weight Converter")

    # Custom CSS
    st.markdown("""
    <style>
    .reportview-container {
        background:rgb(240, 99, 167);
    }
    .sidebar .sidebar-content {
        background:rgb(233, 140, 186);
    }
    .reportview-container {
    background:rgb(97, 146, 190);
    }
    </style>
    """, unsafe_allow_html=True)

    # Header Section
    st.image("baby.jpg", 
             width=300, caption="Little Wonders 🍼")
    st.title("Baby &  Baba Unit Converter Pro")
    st.markdown("---")

    # Initialize session state
    if 'history' not in st.session_state:
        st.session_state.history = []

    # User Inputs
    category = st.selectbox("📚 Category", list(conversion_categories.keys()))
    
    conversion_type = st.selectbox(
        "🔄 Conversion Type",
        conversion_categories[category],
        format_func=lambda x: (
            x if ' to ' not in x 
            else f"{x.split(' to ')[0]} ({unit_symbols[x.split(' to ')[0]]}) → {x.split(' to ')[1]} ({unit_symbols[x.split(' to ')[1]]})"
        )
    )

    # Conversion Logic
    result = None
    if category == "Baby Weight Estimation":
        col1, col2 = st.columns(2)
        with col1:
            mother_weight = st.number_input("Mother's Weight (kg)", 40.0, 150.0, 65.0)
        with col2:
            gestational_weeks = st.number_input("Gestational Weeks", 24, 42, 40)
        
        if st.button("Estimate Baby Weight 👶"):
            result = estimated_baby_weight(mother_weight, gestational_weeks)
    else:
        value = st.number_input(f"📥 Enter {conversion_type.split(' to ')[0]}", 0.0, format="%.4f")
        if st.button("🔁 Convert Now!"):
            conversion_function = CONVERSIONS(conversion_type)
            if conversion_function:
                result = conversion_function(value)
            else:
                st.error("⚠️ Conversion not available")

    # Display Results
    if result is not None:
        if category == "Baby Weight Estimation":
            st.success(f"Estimated Birth Weight: {result:.2f} kg 🎉")
            entry = f"Baby Weight: {mother_weight}kg mom + {gestational_weeks}wks → {result:.2f}kg"
        else:
            from_unit, to_unit = conversion_type.split(' to ')
            st.success(f"✨ {value:.2f}{unit_symbols[from_unit]} = {result:.2f}{unit_symbols[to_unit]}")
            entry = f"{value:.2f}{unit_symbols[from_unit]} → {result:.2f}{unit_symbols[to_unit]}"
        
        # Update history
        st.session_state.history.insert(0, {
            "entry": entry,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
        st.session_state.history = st.session_state.history[:5]  # Keep only last 5 entries

    # History Section
    if st.session_state.history:
        st.markdown("---")
        st.subheader("📜 Conversion History")
        for idx, item in enumerate(st.session_state.history, 1):
            st.markdown(f"{idx}. 🕒 {item['timestamp']} - {item['entry']}")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        Made with ❤️ by Farida Bano<br>
        🚀 For All Little Miracles of Life!
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()