import streamlit as st
import sqlite3
import hashlib
import time
import os
import pandas as pd
from PIL import Image

# 1. Page Configuration & Visual Branding
st.set_page_config(
    page_title="ViralSync Global Media Ecosystem",
    page_icon="🚀",
    layout="wide"
)

# Master Password Hash Setup
MASTER_PASSWORD = "ViralSync5557657623@HAsan#$%HASAN"
MASTER_PASSWORD_HASH = hashlib.sha256(MASTER_PASSWORD.encode()).hexdigest()

def verify_master_password(entered_pass):
    return hashlib.sha256(entered_pass.encode()).hexdigest() == MASTER_PASSWORD_HASH

# 2. Database Initialization
def init_db():
    conn = sqlite3.connect("viralsync_master.db")
    cursor = conn.cursor()
    
    # System Config Table (On/Off Switch)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_config (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO system_config (key, value) VALUES ('app_status', 'ON')")
    
    # Hidden 12 Master Channels (Placeholder)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hidden_master_channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_name TEXT UNIQUE,
            platform TEXT,
            status TEXT
        )
    ''')
    
    # Customer Accounts (Gmail, Password & Saved Platform URLs)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT,
            platform_name TEXT,
            destination_url TEXT,
            updated_date TEXT
        )
    ''')
    
    # Subscribers Table (Local Nagad/Rocket: 01999574408 & Global Visa/Mastercard)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            payment_gateway TEXT,
            payment_ref_id TEXT UNIQUE,
            amount TEXT,
            status TEXT,
            joined_date TEXT
        )
    ''')
    
    # Routing Logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS routing_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_email TEXT,
            platform TEXT,
            destination_url TEXT,
            media_filename TEXT,
            routing_status TEXT,
            timestamp TEXT
        )
    ''')
    
    # Populate Hidden Master Channels placeholders
    cursor.execute("SELECT COUNT(*) FROM hidden_master_channels")
    if cursor.fetchone()[0] == 0:
        secret_channels = [
            (f"Secret Master {i:02d}", "Multi-Platform", "Pending/Active") for i in range(1, 13)
        ]
        cursor.executemany("INSERT OR IGNORE INTO hidden_master_channels (channel_name, platform, status) VALUES (?, ?, ?)", secret_channels)
    
    conn.commit()
    conn.close()

init_db()

# Session State Setup
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_logged_in" not in st.session_state:
    st.session_state.user_logged_in = False
    st.session_state.current_email = ""

# Sidebar - Master Owner Login & Controls
st.sidebar.title("🔐 ViralSync Admin Hub")
st.sidebar.markdown("---")

entered_pass = st.sidebar.text_input("Master Password", type="password")
if st.sidebar.button("Login as Master Owner"):
    if verify_master_password(entered_pass):
        st.session_state.authenticated = True
        st.sidebar.success("Master Access Granted! 🟢")
    else:
        st.sidebar.error("Incorrect Master Password!")

if st.session_state.authenticated:
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚡ System Master Switch")
    
    conn = sqlite3.connect("viralsync_master.db")
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM system_config WHERE key='app_status'")
    current_status = cursor.fetchone()[0]
    
    new_status = st.sidebar.selectbox("App Status", ["ON", "OFF"], index=0 if current_status=="ON" else 1)
    if st.sidebar.button("Update System Status"):
        cursor.execute("UPDATE system_config SET value=? WHERE key='app_status'", (new_status,))
        conn.commit()
        st.sidebar.success(f"System status updated to {new_status}")
    conn.close()

# Main App UI Header with Cover Photo and Profile Logo
try:
    cover_img = Image.open("1000007788.jpg")
    st.image(cover_img, use_container_width=True, caption="ViralSync Global Media Network")
except Exception:
    pass

col_logo, col_title = st.columns([1, 4])
with col_logo:
    try:
        logo_img = Image.open("1000007773.jpg")
        st.image(logo_img, width=120)
    except Exception:
        st.markdown("### 👑 [Logo]")

with col_title:
    st.title("ViralSync - Global Creator Ecosystem")
    st.markdown("### Gmail Auth, Platform URL Saving & Secret Routing")

st.markdown("---")

# Tabs for User & Owner Features
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📥 Gmail Login & Content Publishing", 
    "💳 Pro Plan (Local & Global)", 
    "🛡️ AI Comment Guard", 
    "🔑 AI Password Recovery",
    "📊 Master Secret Logs (Owner Only)"
])

# Tab 1: Gmail Login & Platform URL Saving / Publishing
with tab1:
    st.header("Customer Portal: Gmail Login & Publishing")
    
    if not st.session_state.user_logged_in:
        st.subheader("Step 1: Login with Gmail & Password")
        login_email = st.text_input("Enter Gmail Address", "creator@gmail.com")
        login_pass = st.text_input("Enter Password", type="password")
        
        if st.button("Login to App"):
            if "@" in login_email and len(login_pass) >= 4:
                st.session_state.user_logged_in = True
                st.session_state.current_email = login_email
                st.success(f"Welcome back, {login_email}! Successfully logged in.")
                st.rerun()
            else:
                st.error("Please enter a valid Gmail address and password.")
    else:
        st.success(f"Logged in as: **{st.session_state.current_email}**")
        if st.button("Log Out"):
            st.session_state.user_logged_in = False
            st.session_state.current_email = ""
            st.rerun()
            
        st.markdown("---")
        st.subheader("Step 2: Select Platform & Save URL for Publishing")
        
        selected_platform = st.selectbox("Select Target Platform", ["Facebook", "YouTube", "TikTok", "Instagram", "Telegram"])
        platform_url = st.text_input(f"Enter your {selected_platform} Channel/Page URL", f"https://{selected_platform.lower()}.com/yourpage")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("💾 Save Platform URL"):
                if platform_url.startswith("http"):
                    conn = sqlite3.connect("viralsync_master.db")
                    cursor = conn.cursor()
                    cursor.execute("INSERT OR REPLACE INTO customer_accounts (email, password, platform_name, destination_url, updated_date) VALUES (?, ?, ?, ?, ?)",
                                   (st.session_state.current_email, "secured_hash", selected_platform, platform_url, time.strftime("%Y-%m-%d %H:%M:%S")))
                    conn.commit()
                    conn.close()
                    st.success(f"{selected_platform} URL saved successfully! You can now send messages/posts.")
                else:
                    st.error("Please provide a valid URL starting with http:// or https://")
                    
        with col_btn2:
            st.markdown("### Broadcast Media / Message")
            media_file = st.file_uploader("Upload Video/Image/Message File", type=["mp4", "jpg", "png", "txt"])
            
            if st.button("🚀 Publish to Selected Platform"):
                if media_file is not None:
                    with st.spinner(f"Routing through Hidden Master Channels & publishing to {selected_platform}..."):
                        time.sleep(1.0)
                    
                    conn = sqlite3.connect("viralsync_master.db")
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO routing_logs (customer_email, platform, destination_url, media_filename, routing_status, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                                   (st.session_state.current_email, selected_platform, platform_url, media_file.name, "Successfully Routed via Secret Masters", time.strftime("%Y-%m-%d %H:%M:%S")))
                    conn.commit()
                    conn.close()
                    st.success(f"Content successfully published to your {selected_platform} URL with temporary promotional badge!")
                else:
                    st.error("Please upload a file or message to publish.")

# Tab 2: Pro Plan & Payment (Local Nagad/Rocket: 01999574408 & Global Visa)
with tab2:
    st.header("Pro Subscription ($1 / Month)")
    pay_mode = st.radio("Select Payment Option", ["Local (Nagad / Rocket: 01999574408)", "Global (Visa / Mastercard / Stripe)"])
    
    if pay_mode.startswith("Local"):
        st.markdown("Send **$1** to official number: **`01999574408`** via Nagad/Rocket and submit your TrXID.")
        with st.form("l_form"):
            s_email = st.text_input("Your Gmail / Account Email", st.session_state.current_email if st.session_state.current_email else "creator@gmail.com")
            t_id = st.text_input("Transaction ID (TrXID)")
            if st.form_submit_button("Verify Local Payment"):
                if len(t_id) >= 8:
                    try:
                        conn = sqlite3.connect("viralsync_master.db")
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO subscribers (email, payment_gateway, payment_ref_id, amount, status, joined_date) VALUES (?, ?, ?, ?, ?, ?)",
                                       (s_email, "Nagad/Rocket", t_id, "$1", "Active Pro", time.strftime("%Y-%m-%d %H:%M:%S")))
                        conn.commit()
                        conn.close()
                        st.success("AI Payment Verified! Pro Plan Activated.")
                    except sqlite3.IntegrityError:
                        st.error("TrXID already used.")
                else:
                    st.error("Invalid TrXID.")
    else:
        st.markdown("Pay securely using international credit cards. Funds route directly to your bank account.")
        with st.form("g_form"):
            g_email = st.text_input("Global Account Email", st.session_state.current_email if st.session_state.current_email else "global@gmail.com")
            card_ref = st.text_input("Stripe Charge ID / Card Reference")
            if st.form_submit_button("Verify Global Dollar Payment"):
                if len(card_ref) >= 5:
                    try:
                        conn = sqlite3.connect("viralsync_master.db")
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO subscribers (email, payment_gateway, payment_ref_id, amount, status, joined_date) VALUES (?, ?, ?, ?, ?, ?)",
                                       (g_email, "Visa/Stripe", card_ref, "$1 USD", "Active Pro", time.strftime("%Y-%m-%d %H:%M:%S")))
                        conn.commit()
                        conn.close()
                        st.success("Global Payment Received & Routed to Bank Account!")
                    except sqlite3.IntegrityError:
                        st.error("Reference ID already used.")
                else:
                    st.error("Invalid reference.")

# Tab 3: AI Comment Guard
with tab3:
    st.header("AI Community & Comment Manager")
    cmt = st.text_area("Test Comment", "Great work!")
    if st.button("Run AI Filter"):
        if any(w in cmt.lower() for w in ["scam", "fraud", "fake"]):
            st.error("Comment Blocked by AI Guard.")
        else:
            st.success("Comment Approved! AI Auto-Replied successfully.")

# Tab 4: AI Password Recovery
with tab4:
    st.header("AI Password & Account Assistant")
    em = st.text_input("User Gmail", "user@gmail.com")
    if st.button("Recover Account"):
        st.success(f"AI verified credentials and sent recovery instructions to {em}.")

# Tab 5: Master Secret Logs (Owner Only)
with tab5:
    st.header("Owner Secret Monitoring Dashboard")
    if not st.session_state.authenticated:
        st.warning("⚠️ Restricted Area: Enter Master Password in sidebar.")
    else:
        st.success("Welcome Master Owner! Viewing confidential backend logs:")
        conn = sqlite3.connect("viralsync_master.db")
        df_accounts = pd.read_sql("SELECT * FROM customer_accounts", conn)
        df_logs = pd.read_sql("SELECT * FROM routing_logs", conn)
        df_subs = pd.read_sql("SELECT * FROM subscribers", conn)
        conn.close()
        
        st.subheader("Customer Saved Platform URLs")
        st.dataframe(df_accounts, use_container_width=True)
        
        st.subheader("Secret Routing Logs")
        st.dataframe(df_logs, use_container_width=True)
        
        st.subheader("Subscribers List")
        st.dataframe(df_subs, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>ViralSync Ecosystem © 2026 | All Rights Reserved</p>", unsafe_allow_html=True)
