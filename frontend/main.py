
import streamlit as st
import requests

# Enable wide mode
st.set_page_config(layout="wide")

# Sidebar: System Status, Features, Supported Files
st.sidebar.markdown("## 🛠️ System Status")
backend_url = "http://127.0.0.1:8000/ocr/upload"
try:
    status = requests.get("http://127.0.0.1:8000/")
    if status.status_code == 200:
        st.sidebar.success("Backend Online")
    else:
        st.sidebar.error("Backend Offline")
except Exception:
    st.sidebar.error("Backend Offline")
    st.sidebar.warning("Please start the backend server")

st.sidebar.markdown("## ⭐ Features")
st.sidebar.markdown("""
• **Seller Information** - Company details, address, GST
                    
• **Customer Information** - Customer name, billing details
                    
• **Bill/Receipt Analysis** - Items, amounts, totals
""")
st.sidebar.markdown("## 📄 Supported Files")
st.sidebar.markdown("""
• **Images** - PNG, JPG, JPEG
                    
• **Size Limit** - Up to 10MB
""")

# Main header
st.markdown("""
<div style='background: linear-gradient(90deg, #7b2ff2 0%, #f357a8 100%); padding: 2rem; border-radius: 1rem; text-align: center;'>
    <h1 style='color: white; margin-bottom: 0.5em;'>Invoice Processing System</h1>
    <p style='color: #f3f3f3; font-size: 1.2em;'>Structured Data Extraction • Seller • Customer • Bill Analysis</p>
</div>
""", unsafe_allow_html=True)

# Upload section
st.markdown("### 📤 Upload Your Invoice")
st.write("Drag and drop your invoice file here or click to browse")
uploaded_file = st.file_uploader(
    "Choose invoice file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Enforce 10MB file size limit
    uploaded_file.seek(0, 2)  # Move to end of file
    file_size = uploaded_file.tell()
    uploaded_file.seek(0)  # Reset to start
    if file_size > 10 * 1024 * 1024:
        st.error("File size exceeds 10MB limit. Please upload a smaller image.")
    else:
        st.image(uploaded_file, caption=None)
        st.caption("Uploaded Image")
        st.markdown("""
            <style>
            .full-width-btn button {
                width: 100% !important;
                display: block;
                margin-top: 1em;
            }
            </style>
            <div class='full-width-btn'></div>
        """, unsafe_allow_html=True)
        process = st.button("Process Image")
        if process:
            files = {"file": (uploaded_file.name,
                              uploaded_file, uploaded_file.type)}
            with st.spinner("Processing..."):
                try:
                    response = requests.post(backend_url, files=files)
                    if response.status_code == 200:
                        result = response.json()
                        if "output" in result:
                            st.success("OCR Result:")
                            st.code(result["output"])
                        else:
                            st.error(result.get("error", "Unknown error"))
                    else:
                        st.error(f"Backend error: {response.status_code}")
                except Exception as e:
                    st.error(f"Request failed: {e}")

# About section
st.markdown("---")
