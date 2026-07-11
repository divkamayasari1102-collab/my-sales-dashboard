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
    df = pd.read_excel("Sale_Report.xlsx")
    return df

try:
    df = load_data()
    
    # FIX: Convert 'Design No.' column to string to prevent datetime vs str sorting error
    if "Design No." in df.columns:
        df["Design No."] = df["Design No."].astype(str)
    
    # 3. INTERACTIVE SIDEBAR: Dynamic Filtering based on your data
    st.sidebar.header("Filter Controls")
    
    # Filter based on your actual 'Design No.' column
    if "Design No." in df.columns:
        unique_designs = sorted(df["Design No."].unique())
        selected_design = st.sidebar.multiselect(
            "Select Design Number:",
            options=unique_designs,
            default=unique_designs[:5]  # Show first 5 items by default to prevent clutter
        )
        df_selection = df[df["Design No."].isin(selected_design)]
    else:
        df_selection = df

    # 4. KEY PERFORMANCE INDICATORS (KPIs)
    col1, col2 = st.columns(2)
    with col1:
        total_items = len(df_selection)
        st.metric(label="📦 Total SKU Rows Selected", value=f"{total_items:,}")
    with col2:
        total_unique_designs = df_selection["Design No."].nunique() if "Design No." in df_selection.columns else 0
        st.metric(label="🎨 Unique Designs Count", value=f"{total_unique_designs}")
            
    st.markdown("""---""")

    # 5. INTERACTIVE VISUALIZATION (Plotly Express)
    st.subheader("Sales Distribution & Trends")
    
    if "Design No." in df_selection.columns:
        # Group and count the SKU variants per Design Number
        df_chart = df_selection["Design No."].value_counts().reset_index()
        df_chart.columns = ["Design No.", "Total SKU Variants"]
        
        fig_design_sales = px.bar(
            df_chart,
            x="Design No.",
            y="Total SKU Variants",
            title="<b>Total SKU Variants per Design Number</b>",
            color="Total SKU Variants",
            color_continuous_scale="Viridis",
            template="plotly_white",
        )
        st.plotly_chart(fig_design_sales, use_container_width=True)

    # 6. RAW DATA INSPECTION
    st.subheader("Dataset Viewer")
    st.dataframe(df_selection, use_container_width=True)

except Exception as e:
    st.error(f"Error loading system configuration. Please verify your spreadsheet column headers match the setup. Details: {e}")
