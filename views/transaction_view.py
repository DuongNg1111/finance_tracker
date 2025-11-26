import streamlit as st
import config
from datetime import date

def _render_add_transaction(transaction_model, category_model):
    st.subheader("Add Transaction")
    
    # Move transaction_type outside the form so it can trigger re-renders
    transaction_type = st.selectbox(
        "Transaction Type",
        config.TRANSACTION_TYPES,
        key="transaction_type_selector"
    )
    
    # Get categories based on selected transaction type
    categories = category_model.get_category_by_type(transaction_type)
    category_names = [item['name'] for item in categories]

    # Check if categories exist before showing the form
    if not category_names:
        st.warning(f"No categories for {transaction_type}. Please add new category!")
        # Exit early, don't show the form
        return 
    
    # Create form with remaining fields
    with st.form("add_new_transaction"):
        
        category = st.selectbox(
            "Category",
            category_names
        )

        col1, col2 = st.columns(2)

        with col1:
            amount = st.number_input("Amount ($)",  
                                     min_value=0.01,
                                     step=0.01)
        with col2:
            transaction_date = st.date_input(
                "Transaction Date",
                date.today()
            )

        description = st.text_input(
            "Description (Optional)",
            ""
        )

        submitted = st.form_submit_button("Submit")

        if submitted:
            st.balloons()

            # TODO:
            # call transaction_model.add_new_transaction(**args, **kwargs)


def render_transactions(transaction_model, category_model):
    st.title("💳 Transaction Management")

    # Add transaction
    _render_add_transaction(transaction_model, category_model)