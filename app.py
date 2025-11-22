import streamlit as st
import config

# import model
from database import CategoryModel

# import view module
from views import render_categories

# initialize models
@st.cache_resource
def init_models():
    """Initialize and cached models"""
    return {
        "category": CategoryModel(),
        # "user": UserModel(),
        # "transaction": TransactionModel()
    }

# initialize models
models = init_models()

# Page configuration
st.set_page_config(
    page_title = "Finance Tracker",
    page_icon = "🤑",
    layout = "wide"
)

# =============================================
# 1. Navigation
# =============================================

page = st.sidebar.radio(
    "Navigation",
    ["Home", "Category", "Transaction"]
)

# =============================================
# 2. Router
# =============================================
if page == "Home":
    st.title("Home")

elif page == "Category":
    # get category_model from models
    category_model = models['category']

    # display category views
    render_categories(category_model=category_model)