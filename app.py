import streamlit as st

# In-memory storage
products = []
users = {"farmers": set(), "buyers": set()}

# Product structure: {"farmer": str, "name": str, "price": float, "category": str, "feedback": []}

# --- Navigation ---
st.title("🌱 AgriConnect - Farmer to Buyer Platform")
role = st.sidebar.radio("Select Role", ["Admin", "Farmer", "Buyer"])

# --- Admin Section ---
if role == "Admin":
    st.header("👨‍💼 Admin Dashboard")
    st.write("Manage user accounts and oversee transactions.")

    if st.button("View All Users"):
        st.subheader("Farmers")
        st.write(list(users["farmers"]) if users["farmers"] else "No farmers yet.")
        st.subheader("Buyers")
        st.write(list(users["buyers"]) if users["buyers"] else "No buyers yet.")

# --- Farmer Section ---
elif role == "Farmer":
    st.header("🚜 Farmer Dashboard")
    farmer_name = st.text_input("Enter your name")
    product_name = st.text_input("Product Name")
    category = st.selectbox("Category", ["Crops", "Processed Food", "Handicrafts"])
    price = st.number_input("Price (₹)", min_value=1.0, step=1.0)

    if st.button("Add Product"):
        if farmer_name and product_name:
            product = {
                "farmer": farmer_name,
                "name": product_name,
                "price": price,
                "category": category,
                "feedback": []
            }
            products.append(product)
            users["farmers"].add(farmer_name)
            st.success(f"✅ {product_name} added under {category}")
        else:
            st.error("Please enter your name and product details.")

    # Show farmer’s products
    if farmer_name:
        st.subheader("Your Products")
        farmer_products = [p for p in products if p["farmer"] == farmer_name]
        for p in farmer_products:
            st.write(f"📦 {p['name']} - ₹{p['price']} ({p['category']})")

# --- Buyer Section ---
elif role == "Buyer":
    st.header("🛒 Buyer Dashboard")
    buyer_name = st.text_input("Enter your name")

    # Search bar
    search = st.text_input("🔍 Search Products")
    filtered = [p for p in products if search.lower() in p["name"].lower()] if search else products

    if filtered:
        for idx, p in enumerate(filtered):
            st.write(f"📦 **{p['name']}** - ₹{p['price']} ({p['category']}) | Farmer: {p['farmer']}")
            if st.button(f"Order {p['name']}", key=f"order{idx}"):
                if buyer_name:
                    users["buyers"].add(buyer_name)
                    st.success(f"✅ {buyer_name} placed an order for {p['name']}")
                else:
                    st.error("Please enter your name before ordering.")

            # Feedback option
            feedback = st.text_input(f"Leave feedback for {p['name']}", key=f"fb{idx}")
            if st.button(f"Submit Feedback for {p['name']}", key=f"fbbtn{idx}"):
                if feedback:
                    p["feedback"].append(f"{buyer_name if buyer_name else 'Anonymous'}: {feedback}")
                    st.success("✅ Feedback submitted!")

            # Show feedback
            if p["feedback"]:
                st.write("💬 Feedback:")
                for fb in p["feedback"]:
                    st.write(f"- {fb}")
    else:
        st.info("No products available.")
