# ==========================================================
# MADE IN GEMINI AI GEMS BY ENRIQUE PALMA GRANADOS
# RESIDING IN THE PHILIPPINES | VIBE CODED
# LICENSE: Subject to Google's Open Source/Service Policies
# ==========================================================

import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Local Costing Vault", page_icon="📝")

# --- FILE CONFIG ---
CSV_FILE = 'food_business_vault.csv'

def main():
    st.title("📝 Python's Hug: The Local Food Costing Calculator")
    st.markdown("Calculate your food costs Now!*")

    # --- SIDEBAR ---
    st.sidebar.header("Batch Configuration")
    servings = st.sidebar.number_input("Total Servings", min_value=1, value=10)
    overhead = st.sidebar.number_input("Operating Expenses", min_value=0.0, value=50.0)
    margin = st.sidebar.slider("Margin (%)", min_value=1, max_value=95, value=30)

    # --- INGREDIENTS MANAGEMENT ---
    if 'ingredients' not in st.session_state:
        st.session_state.ingredients = []

    st.subheader("Manage Ingredients")
    
    with st.expander("➕ Add New Ingredient", expanded=True):
        c1, c2 = st.columns([2, 1])
        new_item = c1.text_input("Ingredient Name")
        new_cost = c2.number_input("Cost", min_value=0.0)
        if st.button("Add to Batch"):
            if new_item:
                st.session_state.ingredients.append({"Name": new_item, "Cost": new_cost})
                st.rerun()

    # Delete Feature
    if st.session_state.ingredients:
        for idx, item in enumerate(st.session_state.ingredients):
            col_n, col_c, col_d = st.columns([3, 2, 1])
            col_n.text(item['Name'])
            col_c.text(f"{item['Cost']:,.2f}")
            if col_d.button("❌", key=f"del_{idx}"):
                st.session_state.ingredients.pop(idx)
                st.rerun()
    
    total_ing_cost = sum(i['Cost'] for i in st.session_state.ingredients)
    
    # --- CALCULATIONS ---
    total_cap = total_ing_cost + overhead
    cost_per = total_cap / servings
    denom = (1 - (margin / 100))
    sell_price = cost_per / denom if denom > 0 else 0
    profit = (sell_price * servings) - total_cap

    st.divider()
    m1, m2 = st.columns(2)
    m1.metric("Cost Per Serving", f"{cost_per:,.2f}")
    m2.metric("Target Sale Price", f"{sell_price:,.2f}")

    # --- DATABASE ACTIONS ---
    st.subheader("Vault Actions")
    col_save, col_reset = st.columns(2)

    if col_save.button("💾 Save to CSV"):
        new_data = pd.DataFrame([{
            'Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Servings': servings,
            'Total_Capital': round(total_cap, 2),
            'Selling_Price': round(sell_price, 2),
            'Net_Profit': round(profit, 2)
        }])
        
        # Append to CSV
        if not os.path.isfile(CSV_FILE):
            new_data.to_csv(CSV_FILE, index=False)
        else:
            new_data.to_csv(CSV_FILE, mode='a', header=False, index=False)
        st.success("Saved to local vault!")

    # REQUIREMENT: Reset feature
    if col_reset.button("🔥 Reset CSV Database"):
        if os.path.exists(CSV_FILE):
            os.remove(CSV_FILE)
            st.warning("Vault cleared! Starting from scratch.")
        else:
            st.info("Vault is already empty, mate!")

    # --- VIEW HISTORY ---
    if os.path.isfile(CSV_FILE):
        with st.expander("View Historical Ledger"):
            history = pd.read_csv(CSV_FILE)
            st.dataframe(history)

if __name__ == "__main__":
    main()
