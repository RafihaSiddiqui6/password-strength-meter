import streamlit as st
# import pandas as pd
# import numpy as np
from pyzxcvbn import zxcvbn
# import csv
import os
import json
from fpdf import FPDF
from datetime import datetime
import time
# import base64
# from PIL import Image
import io
import re
import string
import random

# Set page configuration
st.set_page_config(
    page_title="Password Strength Meter & Manager",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #7C3AED;
        --secondary-color: #A78BFA;
        --background-color: #F5F7FF;
        --card-bg-color: #FFFFFF;
        --success-color: #10B981;
        --warning-color: #F59E0B;
        --danger-color: #EF4444;
        --text-color: #1F2937;
        --text-muted: #6B7280;
    }
    
    /* Main container styling */
    .main {
        background-color: var(--background-color);
        padding: 1rem;
        border-radius: 10px;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: var(--primary-color);
        font-weight: 700;
    }
    
    /* Card styling */
    .css-1r6slb0, .css-keje6w {
        background-color: var(--card-bg-color);
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid #E5E7EB;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
        padding: 0.5rem 1rem;
    }
    
    .primary-btn {
        background-color: var(--primary-color);
        color: white;
    }
    
    .primary-btn:hover {
        background-color: #6D28D9;
        box-shadow: 0 4px 6px rgba(109, 40, 217, 0.2);
    }
    
    .secondary-btn {
        background-color: var(--secondary-color);
        color: white;
    }
    
    .danger-btn {
        background-color: var(--danger-color);
        color: white;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #E5E7EB;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background-color: #E5E7EB;
        height: 10px;
        border-radius: 10px;
    }
    
    .strength-0 > div > div > div > div {
        background-color: #9CA3AF !important;
    }
    
    .strength-1 > div > div > div > div {
        background-color: #EF4444 !important;
    }
    
    .strength-2 > div > div > div > div {
        background-color: #F59E0B !important;
    }
    
    .strength-3 > div > div > div > div {
        background-color: #10B981 !important;
    }
    
    .strength-4 > div > div > div > div {
        background-color: #059669 !important;
    }
    
    /* Password card styling */
    .password-card {
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        border: 1px solid #E5E7EB;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .password-card:hover {
        border-color: var(--primary-color);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Badge styling */
    .badge {
        padding: 0.25rem 0.5rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .badge-danger {
        background-color: #FEE2E2;
        color: #B91C1C;
    }
    
    .badge-warning {
        background-color: #FEF3C7;
        color: #92400E;
    }
    
    .badge-success {
        background-color: #D1FAE5;
        color: #065F46;
    }
    
    /* Tooltip styling */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 120px;
        background-color: #333;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.5s ease-in-out;
    }
    
    /* Toggle switch styling */
    .toggle-container {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .toggle-label {
        margin-left: 0.5rem;
        font-weight: 500;
    }
    
    /* Requirements list styling */
    .requirements-list {
        list-style-type: none;
        padding-left: 0;
    }
    
    .requirements-list li {
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
    }
    
    .requirements-list li::before {
        content: "•";
        color: var(--primary-color);
        font-weight: bold;
        display: inline-block;
        width: 1em;
        margin-left: 0.5em;
    }
    
    .requirement-met {
        color: var(--success-color);
    }
    
    .requirement-unmet {
        color: var(--text-muted);
    }
    
    /* Password generator styling */
    .generator-container {
        background-color: #F9FAFB;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1rem;
        border: 1px dashed #E5E7EB;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #E5E7EB;
        color: var(--text-muted);
        font-size: 0.875rem;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: var(--primary-color);
    }
    
    /* Custom alert styling */
    .custom-alert {
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        font-weight: 500;
    }
    
    .alert-info {
        background-color: #EFF6FF;
        border-left: 4px solid #3B82F6;
        color: #1E40AF;
    }
    
    .alert-success {
        background-color: #ECFDF5;
        border-left: 4px solid #10B981;
        color: #065F46;
    }
    
    .alert-warning {
        background-color: #FFFBEB;
        border-left: 4px solid #F59E0B;
        color: #92400E;
    }
    
    .alert-danger {
        background-color: #FEF2F2;
        border-left: 4px solid #EF4444;
        color: #B91C1C;
    }
    
    /* Metrics styling */
    .metric-container {
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary-color);
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: var(--text-muted);
    }
</style>
""", unsafe_allow_html=True)

# Constants
PASSWORD_FILE = "saved_passwords.json"
MAX_PASSWORDS = 50

# Initialize session state variables if they don't exist
if 'show_history' not in st.session_state:
    st.session_state.show_history = False
if 'show_generator' not in st.session_state:
    st.session_state.show_generator = False
if 'password_length' not in st.session_state:
    st.session_state.password_length = 12
if 'use_uppercase' not in st.session_state:
    st.session_state.use_uppercase = True
if 'use_lowercase' not in st.session_state:
    st.session_state.use_lowercase = True
if 'use_numbers' not in st.session_state:
    st.session_state.use_numbers = True
if 'use_symbols' not in st.session_state:
    st.session_state.use_symbols = True
if 'generated_password' not in st.session_state:
    st.session_state.generated_password = ""

# Function to check password strength with enhanced feedback
def check_password_strength(password):
    if not password:
        return 0, []
    
    result = zxcvbn(password)
    score = result['score']
    suggestions = result['feedback']['suggestions']
    
    # Enhanced feedback
    feedback = []
    if suggestions:
        feedback.extend(suggestions)
    
    # Additional checks
    if len(password) < 8:
        feedback.append("Use at least 8 characters")
    if not any(c.isupper() for c in password):
        feedback.append("Add uppercase letters (A-Z)")
    if not any(c.islower() for c in password):
        feedback.append("Add lowercase letters (a-z)")
    if not any(c.isdigit() for c in password):
        feedback.append("Add numbers (0-9)")
    if not any(c in string.punctuation for c in password):
        feedback.append("Add special characters (!@#$%^&*)")
    
    # Check for common patterns
    if re.search(r'(.)\1\1', password):  # Repeated characters
        feedback.append("Avoid repeated characters (e.g., 'aaa')")
    if re.search(r'(12345|qwerty|password|admin)', password.lower()):
        feedback.append("Avoid common password patterns")
    
    return score, list(set(feedback))  # Remove duplicates

# Function to get strength label and color
def get_strength_label(score):
    if score == 0:
        return "Very Weak", "badge-danger"
    elif score == 1:
        return "Weak", "badge-danger"
    elif score == 2:
        return "Fair", "badge-warning"
    elif score == 3:
        return "Good", "badge-success"
    else:
        return "Strong", "badge-success"

# Function to load saved passwords
def load_saved_passwords():
    if os.path.exists(PASSWORD_FILE):
        try:
            with open(PASSWORD_FILE, "r") as file:
                return json.load(file)
        except:
            return []
    return []

# Function to save password
def save_password(password):
    passwords = load_saved_passwords()
    
    # Check if we've reached the limit
    if len(passwords) >= MAX_PASSWORDS:
        return False
    
    # Get password strength
    score, _ = check_password_strength(password)
    
    # Add new password
    passwords.append({
        "password": password,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "strength": score
    })
    
    # Save to file
    with open(PASSWORD_FILE, "w") as file:
        json.dump(passwords, file)
    
    return True

# Function to delete a password
def delete_password(index):
    passwords = load_saved_passwords()
    if 0 <= index < len(passwords):
        del passwords[index]
        with open(PASSWORD_FILE, "w") as file:
            json.dump(passwords, file)
        return True
    return False

# Function to delete all passwords
def delete_all_passwords():
    with open(PASSWORD_FILE, "w") as file:
        json.dump([], file)
    return True

# Function to generate PDF
def generate_pdf(passwords):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Add header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Password Manager - Saved Passwords", ln=True, align='C')
    pdf.ln(10)
    
    # Add timestamp
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='R')
    pdf.ln(5)
    
    # Add table header
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(10, 10, "#", border=1)
    pdf.cell(80, 10, "Password", border=1)
    pdf.cell(60, 10, "Date Saved", border=1)
    pdf.cell(40, 10, "Strength", border=1)
    pdf.ln()
    
    # Add passwords
    pdf.set_font("Arial", '', 12)
    for i, item in enumerate(passwords, start=1):
        pdf.cell(10, 10, str(i), border=1)
        pdf.cell(80, 10, item["password"], border=1)
        pdf.cell(60, 10, item["timestamp"], border=1)
        
        strength_label, _ = get_strength_label(item["strength"])
        pdf.cell(40, 10, strength_label, border=1)
        pdf.ln()
    
    # Save to file
    pdf_file = "saved_passwords.pdf"
    pdf.output(pdf_file)
    return pdf_file

# Function to generate a random password
def generate_password(length=12, use_uppercase=True, use_lowercase=True, use_numbers=True, use_symbols=True):
    chars = ""
    if use_lowercase:
        chars += string.ascii_lowercase
    if use_uppercase:
        chars += string.ascii_uppercase
    if use_numbers:
        chars += string.digits
    if use_symbols:
        chars += string.punctuation
    
    if not chars:  # Fallback if no options selected
        chars = string.ascii_lowercase
    
    # Generate password
    password = ''.join(random.choice(chars) for _ in range(length))
    
    # Ensure at least one character from each selected type
    final_password = list(password)
    
    if use_lowercase and not any(c.islower() for c in password):
        final_password[0] = random.choice(string.ascii_lowercase)
    
    if use_uppercase and not any(c.isupper() for c in password):
        final_password[min(1, length-1)] = random.choice(string.ascii_uppercase)
    
    if use_numbers and not any(c.isdigit() for c in password):
        final_password[min(2, length-1)] = random.choice(string.digits)
    
    if use_symbols and not any(c in string.punctuation for c in password):
        final_password[min(3, length-1)] = random.choice(string.punctuation)
    
    # Shuffle to avoid predictable pattern
    random.shuffle(final_password)
    
    return ''.join(final_password)

# Function to create a visual strength meter
def create_strength_meter(score):
    # Create a visual representation of password strength
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Define colors for each level
    colors = ["#E5E7EB", "#E5E7EB", "#E5E7EB", "#E5E7EB", "#E5E7EB"]
    
    # Fill in colors based on score
    for i in range(score + 1):
        if i == 1:
            colors[i-1] = "#EF4444"  # Red
        elif i == 2:
            colors[i-1] = "#F59E0B"  # Orange
        elif i == 3:
            colors[i-1] = "#10B981"  # Green
        elif i == 4:
            colors[i-1] = "#059669"  # Dark Green
    
    # Display the meter
    col1.markdown(f'<div style="background-color: {colors[0]}; height: 8px; border-radius: 4px 0 0 4px;"></div>', unsafe_allow_html=True)
    col2.markdown(f'<div style="background-color: {colors[1]}; height: 8px;"></div>', unsafe_allow_html=True)
    col3.markdown(f'<div style="background-color: {colors[2]}; height: 8px;"></div>', unsafe_allow_html=True)
    col4.markdown(f'<div style="background-color: {colors[3]}; height: 8px;"></div>', unsafe_allow_html=True)
    col5.markdown(f'<div style="background-color: {colors[4]}; height: 8px; border-radius: 0 4px 4px 0;"></div>', unsafe_allow_html=True)

# Function to display password requirements
def display_password_requirements(password):
    st.markdown("### Password Requirements")
    
    # Check each requirement
    has_length = len(password) >= 8
    has_uppercase = any(c.isupper() for c in password)
    has_lowercase = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    
    # Display requirements with checkmarks or x marks
    requirements = [
        (has_length, "At least 8 characters"),
        (has_uppercase, "Contains uppercase letters (A-Z)"),
        (has_lowercase, "Contains lowercase letters (a-z)"),
        (has_digit, "Contains numbers (0-9)"),
        (has_special, "Contains special characters (!@#$%^&*)")
    ]
    
    for is_met, req_text in requirements:
        if is_met:
            st.markdown(f"✅ {req_text}")
        else:
            st.markdown(f"❌ {req_text}")

# Main App Header
st.title("🔐 IronLock Advanced Password Manager")
st.markdown("Your Ultimate Tool for Strong & Secure Passwords")

# Create tabs for better organization
tab1, tab2, tab3 = st.tabs(["Password Analyzer", "Password Generator", "Password History"])

with tab1:
    # Password input section
    st.markdown("### Enter Password to Analyze")
    
    # Password input with show/hide toggle
    col1, col2 = st.columns([4, 1])
    with col1:
        password = st.text_input("Enter Password:", type="password" if not st.session_state.get('show_password', False) else "password", key="password_input")
 
    
    if password:
        # Check password strength
        score, suggestions = check_password_strength(password)
        
        # Get strength label and class
        strength_label, badge_class = get_strength_label(score)
        
        # Display strength score with custom styling
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <h3 style="margin: 0; margin-right: 1rem;">Strength: </h3>
            <span class="badge {badge_class}">{strength_label}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Display visual strength meter
        create_strength_meter(score)
        
        # Display password requirements
        display_password_requirements(password)
        
        # Display suggestions if any
        if suggestions:
            st.markdown("### Suggestions for Improvement")
            for suggestion in suggestions:
                st.markdown(f"- {suggestion}")
        
        # Save password button
        if st.button("💾 Save Password", key="save_btn"):
            # Check if we've reached the limit
            saved_passwords = load_saved_passwords()
            if len(saved_passwords) >= MAX_PASSWORDS:
                st.error(f"You've reached the maximum limit of {MAX_PASSWORDS} saved passwords. Please delete some passwords before saving new ones.")
            else:
                # Save the password
                with st.spinner("Saving password..."):
                    time.sleep(0.8)  # UI effect
                    save_password(password)
                st.success("✅ Password saved successfully!")
                time.sleep(1)
                st.rerun()

with tab2:
    st.markdown("### Password Generator")
    st.markdown("Create strong, random passwords based on your requirements")
    
    # Password length slider
    st.session_state.password_length = st.slider(
        "Password Length", 
        min_value=4, 
        max_value=32, 
        value=st.session_state.password_length,
        step=1
    )
    
    # Character options
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.use_uppercase = st.checkbox("Include Uppercase Letters (A-Z)", value=st.session_state.use_uppercase)
        st.session_state.use_lowercase = st.checkbox("Include Lowercase Letters (a-z)", value=st.session_state.use_lowercase)
    with col2:
        st.session_state.use_numbers = st.checkbox("Include Numbers (0-9)", value=st.session_state.use_numbers)
        st.session_state.use_symbols = st.checkbox("Include Special Characters (!@#$)", value=st.session_state.use_symbols)
    
    # Generate button
    if st.button("🔄 Generate Password", key="generate_btn"):
        with st.spinner("Generating secure password..."):
            time.sleep(0.5)  # UI effect
            st.session_state.generated_password = generate_password(
                length=st.session_state.password_length,
                use_uppercase=st.session_state.use_uppercase,
                use_lowercase=st.session_state.use_lowercase,
                use_numbers=st.session_state.use_numbers,
                use_symbols=st.session_state.use_symbols
            )
    
    # Display generated password
    if st.session_state.generated_password:
        st.markdown("### Generated Password")
        
        # Display password with copy button
        col1, col2 = st.columns([4, 1])
        with col1:
            st.code(st.session_state.generated_password, language=None)
        with col2:
            if st.button("📋 Copy", key="copy_btn"):
                st.success("Password copied to clipboard!")
        
        # Check and display strength of generated password
        score, _ = check_password_strength(st.session_state.generated_password)
        strength_label, badge_class = get_strength_label(score)
        
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <span style="margin-right: 0.5rem;">Strength: </span>
            <span class="badge {badge_class}">{strength_label}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Create visual strength meter
        create_strength_meter(score)
        
        # Use this password button
        if st.button("✅ Use This Password", key="use_generated_btn"):
            st.session_state.password_input = st.session_state.generated_password
            st.rerun()

with tab3:
    # Password history section
    st.markdown("### Password History")
    
    # Load saved passwords
    saved_passwords = load_saved_passwords()
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Passwords", len(saved_passwords))
    with col2:
        # Calculate average strength
        avg_strength = 0
        if saved_passwords:
            avg_strength = sum(p["strength"] for p in saved_passwords) / len(saved_passwords)
        st.metric("Average Strength", f"{avg_strength:.1f}/4")
    with col3:
        # Calculate remaining capacity
        remaining = MAX_PASSWORDS - len(saved_passwords)
        st.metric("Storage Remaining", f"{remaining}/{MAX_PASSWORDS}")
    
    # Actions for password history
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Download as PDF", key="download_pdf_btn", disabled=len(saved_passwords) == 0):
            with st.spinner("Generating PDF..."):
                pdf_path = generate_pdf(saved_passwords)
                with open(pdf_path, "rb") as pdf_file:
                    pdf_bytes = pdf_file.read()
                
                st.download_button(
                    label="Download PDF",
                    data=pdf_bytes,
                    file_name="password_manager_export.pdf",
                    mime="application/pdf",
                    key="download_pdf"
                )
    with col2:
        if st.button("🗑️ Clear All Passwords", key="clear_all_btn", disabled=len(saved_passwords) == 0):
            if st.session_state.get('confirm_delete_all', False):
                with st.spinner("Deleting all passwords..."):
                    delete_all_passwords()
                st.success("All passwords have been deleted!")
                st.session_state.confirm_delete_all = False
                time.sleep(1)
                st.rerun()
            else:
                st.session_state.confirm_delete_all = True
                st.warning("⚠️ Are you sure? Click again to confirm deletion of all passwords.")
    
    # Display saved passwords
    if not saved_passwords:
        st.info("No passwords saved yet. Use the Password Analyzer tab to save passwords.")
    else:
        # Toggle to show/hide passwords
        show_passwords = st.toggle("Show Password Content", value=False)
        
        # Display each password with delete option
        for i, item in enumerate(saved_passwords):
            strength_label, badge_class = get_strength_label(item["strength"])
            
            # Create a card-like container for each password
            st.markdown(f"""
            <div class="password-card">
                <div>
                    <div style="font-weight: 500;">
                        {i+1}. {"•" * 8 if not show_passwords else item["password"]}
                    </div>
                    <div style="font-size: 0.75rem; color: #6B7280;">
                        Saved on: {item["timestamp"]}
                    </div>
                </div>
                <span class="badge {badge_class}">{strength_label}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Delete button for each password
            if st.button(f"🗑️ Delete", key=f"delete_btn_{i}"):
                with st.spinner("Deleting password..."):
                    delete_password(i)
                st.success("Password deleted successfully!")
                time.sleep(0.5)
                st.rerun()
        
        # Warning if approaching limit
        if len(saved_passwords) >= MAX_PASSWORDS * 0.8:
            st.warning(f"⚠️ You're approaching the maximum limit of {MAX_PASSWORDS} saved passwords. Consider deleting some old passwords.")

# Footer
st.markdown("""
<div class="footer">
<p>🔐 IronLock Advanced Password Manager | Developed by Rafiha Siddiqui | © 2025</p>
</div>
""", unsafe_allow_html=True)

# Initialize the password file if it doesn't exist
if not os.path.exists(PASSWORD_FILE):
    with open(PASSWORD_FILE, "w") as file:
        json.dump([], file)