import streamlit as st
from graph import app

st.title("Admin Review Dashboard")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = "1"
    
config = {"configurable": {"thread_id": st.session_state.thread_id}}

st.sidebar.header("Tạo yêu cầu mới")
customer_id = st.sidebar.text_input("Customer ID", value="CUST123")
proposed_action = st.sidebar.selectbox("Action", ["send_email", "increase_credit_limit"])
confidence_score = st.sidebar.slider("Confidence", 0.0, 1.0, 0.9)
reasoning = st.sidebar.text_area("Reasoning", value="Customer meets all criteria.")

if st.sidebar.button("Submit Request"):
    st.session_state.thread_id = str(int(st.session_state.thread_id) + 1)
    config = {"configurable": {"thread_id": st.session_state.thread_id}}
    app.invoke({
        "customer_id": customer_id,
        "proposed_action": proposed_action,
        "confidence_score": confidence_score,
        "reasoning": reasoning,
        "human_decision": None
    }, config)

st.header("Yêu cầu chờ duyệt")
state = app.get_state(config)

if state.next:
    st.info("Có một yêu cầu đang chờ duyệt.")
    current_state = state.values
    st.write(f"**Customer ID:** {current_state.get('customer_id')}")
    st.write(f"**Proposed Action:** {current_state.get('proposed_action')}")
    st.write(f"**Confidence Score:** {current_state.get('confidence_score')}")
    st.write(f"**Reasoning:** {current_state.get('reasoning')}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Approve"):
            app.update_state(config, {"human_decision": "approved"})
            app.invoke(None, config)
            st.rerun()
            
    with col2:
        if st.button("Reject"):
            app.update_state(config, {"human_decision": "rejected"})
            app.invoke(None, config)
            st.rerun()
            
    with col3:
        if st.button("Edit Action"):
            new_action = "send_email" if current_state.get('proposed_action') == "increase_credit_limit" else "increase_credit_limit"
            app.update_state(config, {"human_decision": f"edited to {new_action}", "proposed_action": new_action})
            app.invoke(None, config)
            st.rerun()
else:
    st.success("Không có yêu cầu nào đang chờ.")
    if state.values:
         st.write("Yêu cầu gần nhất đã được xử lý xong.")
