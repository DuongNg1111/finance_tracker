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

### Add new category

st.header("➕ Add new category")

with st.form("add_category_form"):
    col1, col2, col3 = st.columns([3, 3, 1])

    with col1:
        # category_type = st.selectbox("Type", ['Expense', 'Income'])
        category_type = st.selectbox("Type", config.TRANSACTION_TYPES)

    with col2:
        category_name = st.text_input("Category Name",
                                      placeholder = "e.g, Groceries, Rent, KPI bonus")
        
    with col3:
        st.write("")
        st.write("")
        submited = st.form_submit_button("▶", use_container_width=True)

    if submited:
        if not category_type:
            st.error("Please choose Category Type")
        if not category_name:
            st.error("Please enter a Category Name")
        else:
            # print(f"Category type: {category_type}")
            # print(f"Category name: {category_name}")
            new_category = category_model.add_category(type = category_type,
                                                    category_name=category_name)

            if new_category:
                st.success(f"Category added {category_name} successfully !")
                st.rerun() # Refresh the page to load data
            else:
                st.error("Failed to add new category")

st.divider()

# TODO: make categories detail

st.subheader("Category detail")
tab1, tab2 = st.tabs(config.TRANSACTION_TYPES)

with tab1:
    expense_lst = category_model.get_category_by_type(type = "Expense")