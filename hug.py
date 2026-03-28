# ==========================================================
# MADE IN GEMINI AI GEMS BY ENRIQUE PALMA GRANADOS
# RESIDING IN THE PHILIPPINES | VIBE CODED
# LICENSE: Subject to Google's Open Source/Service Policies
# ==========================================================

import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="The Wrangler's Costing Vault", page_icon="🐍")

def main():
    st.title("🐍 Python's Hug: Online Costing System")
    st.markdown("*Yodel-ay-hee-hooo!* Welcome to your digital ledger.")

    # --- SIDEBAR: OVERHEAD & MARGIN ---
    st.sidebar.header("Global Settings")
    servings = st.sidebar.number_input("Total Servings", min_value=1, value=10)
    overhead = st.sidebar.number_input("Operating Expenses (Fixed)", min_value=0.0, value=50.0)
    margin = st.sidebar.slider("Desired Profit Margin (%)", 5, 95, 30)

    # --- MAIN AREA: INGREDIENTS ---
    st.subheader("Itemized Ingredients")
    
    # Using a clever session state to keep track of ingredients dynamically
    if 'ingredients' not in st.session_state:
        st.session_state.ingredients = []

    col1, col2 = st.columns([2, 1])
    with col1:
        new_item = st.text_input("Ingredient Name", placeholder="e.g. Flour")
    with col2:
        new_cost = st.number_input("Cost", min_value=0.0, value=0.0)

    if st.button("Add Ingredient to Batch"):
        if new_item:
            st.session_state.ingredients.append({"Name": new_item, "Cost": new_cost})
            st.rerun()

    # Display current list
    if st.session_state.ingredients:
        df_ing = pd.DataFrame(st.session_state.ingredients)
        st.table(df_ing)
        total_ing_cost = df_ing['Cost'].sum()
        
        if st.button("Clear Ingredients"):
            st.session_state.ingredients = []
            st.rerun()
    else:
        total_ing_cost = 0.0
        st.info("Start adding ingredients to see the magic happen!")

    # --- CALCULATIONS ---
    total_capital = total_ing_cost + overhead
    cost_per_serving = total_capital / servings
    
    # The Wrangler's Margin Formula
    selling_price = cost_per_serving / (1 - (margin / 100))
    total_revenue = selling_price * servings
    net_profit = total_revenue - total_capital

    # --- RESULTS DASHBOARD ---
    st.divider()
    st.header("Financial Breakdown")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Cost per Serving", f"{cost_per_serving:,.2f}")
    m2.metric("Target Sale Price", f"{selling_price:,.2f}")
    m3.metric("Projected Profit", f"{net_profit:,.2f}")

    # --- DATABASE ACTION ---
    if st.button("🔒 Save Batch to Vault (CSV)"):
        report_data = {
            'Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Servings': servings,
            'Ingredient_Cost': round(total_ing_cost, 2),
            'Total_Capital': round(total_capital, 2),
            'Selling_Price': round(selling_price, 2),
            'Net_Profit': round(net_profit, 2)
        }
        
        df_log = pd.DataFrame([report_data])
        file_name = 'food_business_vault.csv'
        
        # Append logic
        if not os.path.isfile(file_name):
            df_log.to_csv(file_name, index=False)
        else:
            df_log.to_csv(file_name, mode='a', header=False, index=False)
            
        st.success("Batch successfully yodeled into the database!")

    # --- VIEW HISTORY ---
    if os.path.isfile('food_business_vault.csv'):
        with st.expander("View Historical Vault"):
            history = pd.read_csv('food_business_vault.csv')
            st.dataframe(history)

if __name__ == "__main__":
    main()
