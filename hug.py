# ==========================================================
# MADE IN GEMINI AI GEMS BY ENRIQUE PALMA GRANADOS
# RESIDING IN THE PHILIPPINES | VIBE CODED
# LICENSE: Subject to Google's Open Source/Service Policies
# ==========================================================

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Cloud Costing Vault", page_icon="☁️")

def main():
    st.title("☁️ Python's Hug: The Pruning Wrangler")
    st.markdown("Edit your list with surgical precision! *Yodel-ay-hee-hooo!*")

    # Establish Connection (Requires st.secrets)
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
    except Exception:
        st.warning("Google Sheets not connected. Running in local-only mode!")
        conn = None

    # --- SIDEBAR ---
    st.sidebar.header("Batch Configuration")
    servings = st.sidebar.number_input("Total Servings", min_value=1, value=10)
    overhead = st.sidebar.number_input("Operating Expenses", min_value=0.0, value=50.0)
    
    # REQUIREMENT: Change minimum margin to 1%
    margin = st.sidebar.slider("Margin (%)", min_value=1, max_value=95, value=30)

    # --- INGREDIENTS LIST MANAGEMENT ---
    if 'ingredients' not in st.session_state:
        st.session_state.ingredients = []

    st.subheader("Manage Ingredients")
    
    # Input area
    with st.expander("➕ Add New Ingredient", expanded=True):
        c1, c2 = st.columns([2, 1])
        new_item = c1.text_input("Ingredient Name")
        new_cost = c2.number_input("Cost", min_value=0.0, key="new_cost_input")
        if st.button("Add to Batch"):
            if new_item:
                st.session_state.ingredients.append({"Name": new_item, "Cost": new_cost})
                st.rerun()

    # REQUIREMENT: Delete item feature
    if st.session_state.ingredients:
        st.write("Current Ingredients:")
        for idx, item in enumerate(st.session_state.ingredients):
            col_name, col_cost, col_del = st.columns([3, 2, 1])
            col_name.text(item['Name'])
            col_cost.text(f"{item['Cost']:,.2f}")
            # The Delete Button
            if col_del.button("❌", key=f"del_{idx}"):
                st.session_state.ingredients.pop(idx)
                st.rerun()
    
    total_ing_cost = sum(i['Cost'] for i in st.session_state.ingredients)
    
    # --- CALCULATIONS ---
    total_cap = total_ing_cost + overhead
    cost_per = total_cap / servings
    # Logic check to prevent division by zero if margin is 100%
    denom = (1 - (margin / 100))
    sell_price = cost_per / denom if denom > 0 else 0
    profit = (sell_price * servings) - total_cap

    # --- RESULTS ---
    st.divider()
    res1, res2 = st.columns(2)
    res1.metric("Cost Per Serving", f"{cost_per:,.2f}")
    res2.metric("Target Sale Price", f"{sell_price:,.2f}", delta=f"Margin: {margin}%")

    # --- SYNC ---
    if st.button("🚀 Sync to Google Sheets"):
        if conn:
            new_row = pd.DataFrame([{
                'Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'Servings': servings,
                'Ingredient_Cost': round(total_ing_cost, 2),
                'Total_Capital': round(total_cap, 2),
                'Selling_Price': round(sell_price, 2),
                'Net_Profit': round(profit, 2)
            }])
            # This logic assumes the sheet 'Sheet1' exists with headers
            existing_data = conn.read(worksheet="Sheet1")
            updated_df = pd.concat([existing_data, new_row], ignore_index=True)
            conn.update(worksheet="Sheet1", data=updated_df)
            st.success("Yodeled to the cloud!")
        else:
            st.error("No cloud connection found, mate!")

if __name__ == "__main__":
    main()
