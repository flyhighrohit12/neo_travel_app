import streamlit as st
import os
import json
from PIL import Image
import base64
from pathlib import Path
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="N.E.O - North East Odyssey",
    layout="wide"
)

# Custom CSS for styling
def load_css():
    st.markdown("""
        <style>
        /* Main theme colors */
        :root {
            --primary-color: #2D5A27;
            --secondary-color: #8B9D77;
            --background-color: #F4F1DE;
            --text-color: #2C3E50;
            --accent-color: #E07A5F;
        }
        
        /* Global styles */
        .stApp {
            background-color: var(--background-color);
            color: var(--text-color);
        }
        
        /* Custom container */
        .custom-container {
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Header styling */
        .header {
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        
        /* Image grid styling */
        .image-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            padding: 20px;
        }
        
        .image-card {
            position: relative;
            overflow: hidden;
            border-radius: 10px;
            transition: transform 0.3s ease;
            aspect-ratio: 4/3;
            width: 100%;
            margin-bottom: 20px;
        }
        
        .image-card img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        .image-card:hover {
            transform: scale(1.05);
            z-index: 1;
        }
        
        .image-caption {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 10px;
            text-align: center;
        }
        
        /* Login form styling */
        .login-form {
            max-width: 300px;
            margin: 50px auto;
            padding: 25px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Input field styling */
        .stTextInput > div {
            width: 100% !important;
            max-width: 250px !important;
        }
        
        .stTextInput input {
            width: 100% !important;
            border-radius: 5px !important;
            border: 1px solid #e0e0e0 !important;
            padding: 8px 12px !important;
        }
        
        /* Admin caption input styling */
        .caption-input .stTextInput > div {
            width: 100% !important;
            max-width: 100% !important;
        }
        
        /* Remove extra white space in login form */
        .login-form .stMarkdown {
            display: none;
        }
        
        /* Adjust contact info input width */
        .contact-info-input .stTextInput > div {
            width: 100% !important;
            max-width: 400px !important;
        }
        
        /* Center align login elements */
        .login-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
        }
        
        /* Button styling */
        .stButton>button {
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            transition: background-color 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: var(--secondary-color);
        }
        </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'login_status' not in st.session_state:
    st.session_state.login_status = None
if 'user_type' not in st.session_state:
    st.session_state.user_type = None

# Load user credentials from JSON file
def load_credentials():
    try:
        with open('credentials.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create default admin credentials if file doesn't exist
        default_credentials = {
            "admin": {
                "username": "admin",
                "password": "admin123"
            },
            "users": [
                {"username": "user1", "password": "user123"}
            ]
        }
        with open('credentials.json', 'w') as f:
            json.dump(default_credentials, f)
        return default_credentials

# Load image captions from JSON file
def load_captions():
    try:
        with open('captions.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save image captions to JSON file
def save_captions(captions):
    with open('captions.json', 'w') as f:
        json.dump(captions, f)

# Load contact information
def load_contact_info():
    try:
        with open('contact_info.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        default_info = {
            "address": "123 Nature Street, Northeast City",
            "phone": "+1 (555) 123-4567",
            "email": "contact@neo-odyssey.com"
        }
        with open('contact_info.json', 'w') as f:
            json.dump(default_info, f)
        return default_info

# Save contact information
def save_contact_info(info):
    with open('contact_info.json', 'w') as f:
        json.dump(info, f)

# Login page
def login_page():
    # Remove any default padding
    st.markdown("""
        <style>
        .stApp {
            padding-top: 0;
        }
        .css-18e3th9 {
            padding-top: 0;
        }
        .css-1d391kg {
            padding-top: 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Create header only
    st.markdown("""
        <div class="header">
            <h1> N.E.O - North East Odyssey</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Login inputs directly without container
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        username = st.text_input("", placeholder="Enter username", key="login_username")
        password = st.text_input("", type="password", placeholder="Enter password", key="login_password")
        with st.container():
            st.markdown('<div class="login-button">', unsafe_allow_html=True)
            login_button = st.button("Login")
            st.markdown('</div>', unsafe_allow_html=True)
            
        if login_button:
            credentials = load_credentials()
            if username == credentials["admin"]["username"] and password == credentials["admin"]["password"]:
                st.session_state.login_status = True
                st.session_state.user_type = "admin"
                st.experimental_rerun()
            elif any(user["username"] == username and user["password"] == password for user in credentials["users"]):
                st.session_state.login_status = True
                st.session_state.user_type = "user"
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")
        st.markdown('</div>', unsafe_allow_html=True)

# Display images in grid
def display_image_grid(image_files, captions):
    col1, col2, col3 = st.columns(3)
    columns = [col1, col2, col3]
    
    for idx, img_file in enumerate(image_files):
        with columns[idx % 3]:
            try:
                img_path = os.path.join("images", img_file)
                img = Image.open(img_path)
                caption = captions.get(img_file, "")
                
                st.markdown(f'''
                    <div class="image-card">
                        <img src="data:image/png;base64,{base64.b64encode(open(img_path, "rb").read()).decode()}" 
                             style="width:100%; height:100%; object-fit:cover; border-radius:10px;">
                        <div class="image-caption">{caption}</div>
                    </div>
                ''', unsafe_allow_html=True)
                
                if st.session_state.user_type == "admin":
                    with st.container():
                        st.markdown('<div class="caption-input">', unsafe_allow_html=True)
                        new_caption = st.text_input(f"Edit caption for {img_file}", caption)
                        st.markdown('</div>', unsafe_allow_html=True)
                        if new_caption != caption:
                            captions[img_file] = new_caption
                            save_captions(captions)
            except Exception as e:
                st.warning(f"Could not load image: {img_file}")

# Main app
def main_app():
    st.markdown('<div class="header"><h1> N.E.O - North East Odyssey</h1></div>', unsafe_allow_html=True)
    
    # Logout button
    if st.button("Logout"):
        st.session_state.login_status = None
        st.session_state.user_type = None
        st.experimental_rerun()
    
    # Check if images directory exists, if not create it
    if not os.path.exists("images"):
        os.makedirs("images")
        st.warning("Images directory was created. Please add your images to the 'images' folder.")
        image_files = []
    else:
        # Load images from the images folder
        image_files = [f for f in os.listdir("images") if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        if not image_files:
            st.warning("No images found in the 'images' folder. Please add some images.")
    
    # Load captions
    captions = load_captions()
    
    # Display images
    if image_files:
        display_image_grid(image_files, captions)
    
    # Footer with contact information
    st.markdown("---")
    contact_info = load_contact_info()
    
    if st.session_state.user_type == "admin":
        st.subheader("Edit Contact Information")
        st.markdown('<div class="contact-info-input">', unsafe_allow_html=True)
        new_address = st.text_input("Address", contact_info["address"])
        new_phone = st.text_input("Phone", contact_info["phone"])
        new_email = st.text_input("Email", contact_info["email"])
        st.markdown('</div>', unsafe_allow_html=True)
        
        if (new_address != contact_info["address"] or 
            new_phone != contact_info["phone"] or 
            new_email != contact_info["email"]):
            contact_info.update({
                "address": new_address,
                "phone": new_phone,
                "email": new_email
            })
            save_contact_info(contact_info)
    
    st.markdown(f'''
        <div class="custom-container">
            <h3>Contact Us</h3>
            <p>Address: {contact_info["address"]}</p>
            <p>Phone: {contact_info["phone"]}</p>
            <p>Email: {contact_info["email"]}</p>
        </div>
    ''', unsafe_allow_html=True)

# Main execution
def main():
    load_css()
    
    if st.session_state.login_status:
        main_app()
    else:
        login_page()

if __name__ == "__main__":
    main()