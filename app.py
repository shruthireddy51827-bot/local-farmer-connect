
import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Smart Local Farmer Connect",
    page_icon="🌱",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #f5faf3;
}
.hero {
    background: linear-gradient(120deg, #14532d, #4d9b55);
    padding: 35px;
    border-radius: 18px;
    color: white;
    text-align: center;
}
.hero h1 {
    color: white;
    font-size: 38px;
}
.hero p {
    font-size: 18px;
}
.product-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #dcebd9;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🌱 FarmerConnect")
st.sidebar.caption("Local Farmer Market Information System")

menu = st.sidebar.radio(
    "Navigation",
    ["Home", "Explore Products", "Market Prices",
     "Farmer Registration", "About Us"]
)

st.sidebar.markdown("---")
st.sidebar.info("Connecting Farmers and Customers")

# Home page
if menu == "Home":

    st.markdown("""
    <div class="hero">
        <h1>🌾 Smart Local Farmer Connect</h1>
        <p>Fresh from local farms, closer to you.</p>
        <p>Empowering Farmers | Supporting Customers</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.subheader("Welcome to our Farmer Marketplace!")

    st.write(
        "Discover fresh agricultural products, "
        "connect directly with local farmers and "
        "explore market price information."
    )

    # Dashboard metrics
    col1, col2, col3 = st.columns(3)

    col1.metric("Farmers", "0")
    col2.metric("Products", "0")
    col3.metric("Local Markets", "0")

    st.markdown("---")

    st.subheader("🌿 Explore Product Categories")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("### 🥕")
        st.write("Vegetables")

    with c2:
        st.markdown("### 🍎")
        st.write("Fruits")

    with c3:
        st.markdown("### 🌾")
        st.write("Grains")

    with c4:
        st.markdown("### 🌱")
        st.write("Other Crops")

    st.markdown("---")

    st.subheader("⭐ Why Choose FarmerConnect?")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **👨‍🌾 For Farmers**
        - Display agricultural products.
        - Share product availability.
        - Reach local customers.
        - View market information.
        """)

    with col2:
        st.markdown("""
        **🛒 For Customers**
        - Discover fresh products.
        - Find local farmers.
        - Compare listed prices.
        - Send product enquiries.
        """)

    st.markdown("---")
    st.caption("© 2026 Smart Local Farmer Connect | Community Project")

# Other navigation pages - temporary placeholders
elif menu == "Explore Products":
    st.title("🛒 Explore Agricultural Products")
    st.info("Product marketplace will be developed in our next stage.")

elif menu == "Market Prices":
    st.title("📊 Local Market Prices")
    st.info("Market price dashboard will be developed soon.")

elif menu == "Farmer Registration":
    st.title("👨‍🌾 Farmer Registration")
    st.info("Farmer registration system is coming in the next stage.")

elif menu == "About Us":
    st.title("🌱 About Smart Local Farmer Connect")
    st.write(
        "Our mission is to connect local farmers "
        "and customers through digital technology."
    )