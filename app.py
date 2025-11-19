import streamlit as st
import config
from category_models import CategoryModel


# initialize models
@st.cache_resource
def init_models():
    """Initialize and cached models"""
    return CategoryModel()


category_model = init_models()

# Page configuration
st.set_page_config(
    page_title = "Category Manager",
    layout = "wide"
)

# =============================================
# MAIN APP
# =============================================


# App tile
st.title(config.APP_NAME)

# Overall
st.header("Categories Overall")

col1, col2, col3 = st.columns(3)

with col1:
    st.text("Total Categories")
    total = category_model.get_total()
    st.text(f"{len(total)}")

with col2:
    st.text("Expense Categories")
    expense = category_model.get_category_by_type(type = "Expense")
    st.text(f"{len(expense)}")

with col3:
    st.text("Income Categories")
    income = category_model.get_category_by_type(type = "Income")
    st.text(f"{len(income)}")

st.divider()