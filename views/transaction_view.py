import streamlit as st
import config
from datetime import date
import time

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
            # st.balloons()

            result = transaction_model.add_new_transaction(
                transaction_type,
                category,
                amount,
                transaction_date,
                description
            )
            if result:
                st.success(f"Transaction has been added !!!")
                time.sleep(2) # Manually extend message display duration
                st.rerun()
            else:
                st.error("Failed to add transaction")
                time.sleep(1)

def _render_transaction_detail(item, transaction_model):
    transaction_date = item.get("transaction_date")
    if not transaction_date:
        transaction_date = "Unknown"
    else:
        transaction_date = transaction_date.strftime("%d/%m/%Y")

    with st.expander(
        f"{transaction_date} -"
        f"{item.get("amount")} $"
    ):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"***Transaction type: {item.get("type")}**")
            st.write(f"***Category: {item.get("category")}**")
            st.write(f"***Amount: {item.get("amount")} USD**")
            st.caption(f"***Description: {item.get("description")}**")
        with col2:
            delete_button = st.button("❌", key = f"transaction_delete_{item["_id"]}")
            if delete_button:
                # TODO: call delete transaction
                delete_result = transaction_model.delete_transaction(item["_id"])
                if delete_result:
                    st.success("Transaction delete")
                    time.sleep(2)
                    st.rerun()
        with col3:
            if st.button("✏️", key=f"transaction_edit_{item['_id']}"):
                st.warning("Edit transaction")
                time.sleep(2)

                # TODO:
                #. 1 Display modal contains transaction detail
                # 1.1 trigger for show_edit_modal = True
                # 2.2 .get_transaction_by_id
                st.session_state['show_edit_modal'] = True
                st.rerun()


                # 2. change properties and clicked save
                # call .update_transaction

def _render_list_transaction(transaction_model):
    st.subheader("List transaction")

    results = transaction_model.get_all_transactions(filters = {})
    if results:
        # transactions = results['transactions']
        for item in results:
            _render_transaction_detail(item, transaction_model)

@st.dialog("Edit Transaction")
def _render_edit_modal(transaction_model):
    st.title(f"Edit transaction section")

def render_transactions(transaction_model, category_model):
    st.title("💳 Transaction Management")

    # check if any edit button is clicked
    if st.session_state.get("show_edit_modal", False):
        _render_edit_modal(transaction_model)

    # Display list of transactions:
    _render_list_transaction(transaction_model)

    # Add transaction
    _render_add_transaction(transaction_model, category_model)