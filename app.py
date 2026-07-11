import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration for a professional look
st.set_page_config(page_title="Sales Performance Dashboard", layout="wide")

st.title("📊 Interactive Sales Dashboard")
st.markdown("## Global Revenue & Data Analysis Report")

# 2. Cached Data Loading Function
@st.cache_data
def load_data():
    # Reads the Excel file uploaded in the same GitHub repository folder
    df = pd.read_excel("Sale_Report.xlsx")
    return df

try:
    df = load_data()
    
    # 3. INTERACTIVE SIDEBAR: Dynamic Filtering
    st.sidebar.header("Filter Controls")
    
    # Dynamic Filter 1: Category (Fallback if column name is lowercase or capitalized)
    category_col = [col for col in df.columns if col.lower() in ['category', 'kategori']]
    if category_col:
        selected_category = st.sidebar.multiselect(
            "Select Category:",
            options=df[category_col[0]].unique(),
            default=df[category_col[0]].unique()
        )
        df_selection = df[df[category_col[0]].isin(selected_category)]
    else:
        df_selection = df

    # 4. KEY PERFORMANCE INDICATORS (KPIs)
    # Automatically detects numeric revenue columns
    sales_col = [col for col in df.columns if col.lower() in ['total_penjualan', 'sales', 'revenue', 'total']]
    
    if sales_col:
        total_sales = float(df_selection[sales_col[0]].sum())
        average_sales = float(df_selection[sales_col[0]].mean())
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="💰 Total Revenue", value=f"${total_sales:,.2f}")
        with col2:
            st.metric(label="📈 Average Transaction Value", value=f"${average_sales:,.2f}")
            
    st.markdown("""---""")

    # 5. INTERACTIVE VISUALIZATION (Plotly Express)
    st.subheader("Sales Distribution & Trends")
    
    # Automatically matches product/item column against sales column
    product_col = [col for col in df.columns if col.lower() in ['produk', 'product', 'item']]
    
    if product_col and sales_col:
        fig_product_sales = px.bar(
            df_selection,
            x=product_col[0],
            y=sales_col[0],
            title=f"<b>Revenue Generated per {str(product_col[0]).capitalize()}</b>",
            color_discrete_sequence=["#0083B0"] * len(df_selection),
            template="plotly_white",
        )
        st.plotly_chart(fig_product_sales, use_container_width=True)

    # 6. RAW DATA INSPECTION
    st.subheader("Dataset Viewer")
    st.dataframe(df_selection, use_container_width=True)

except Exception as e:
    st.error(f"Error loading system configuration. Please verify your spreadsheet column headers match the setup. Details: {e}")
