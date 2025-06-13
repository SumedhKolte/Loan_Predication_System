import streamlit as st
from PIL import Image
import os

def main():
    st.set_page_config(page_title="Document Verification", page_icon="📄")
    
    # Add custom CSS
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .upload-box {
            border: 2px dashed #aaa;
            padding: 20px;  
            text-align: center;
            margin: 20px 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("📄 Document Verification")
    st.markdown("---")
    
    # Document type selection
    doc_type = st.selectbox(
        "Select Document Type",
        ["Select Document Type", "Identity Proof", "Address Proof", "Income Proof", "Bank Statement"],
        help="Choose the type of document you want to verify"
    )
    
    if doc_type != "Select Document Type":
        st.markdown("### Upload Documents")
        
        # File uploader
        uploaded_file = st.file_uploader(
            f"Upload your {doc_type}",
            type=["pdf", "png", "jpg", "jpeg"],
            help=f"Upload your {doc_type} in PDF or image format"
        )
        
        if uploaded_file is not None:
            if uploaded_file.type.startswith('image'):
                st.image(uploaded_file, caption=f"Uploaded {doc_type}", use_column_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Verify Document", key="verify_btn"):
                    with st.spinner("Verifying document..."):
                        # Simulated verification process
                        st.success("✅ Document verified successfully!")
                        st.markdown("### Verification Details")
                        st.json({
                            "Document Type": doc_type,
                            "Verification Status": "Verified",
                            "Verification Date": "2025-05-07",
                            "Document ID": "DOC" + str(hash(uploaded_file.name))[:8],
                            "Verification Score": "98%"
                        })
            
            with col2:
                if st.button("Clear", key="clear_btn"):
                    st.rerun()
    
    # Help section
    with st.expander("ℹ️ Help & Guidelines"):
        st.markdown("""
        ### Acceptable Document Formats
        - Identity Proof: Passport, Driver's License, Aadhar Card
        - Address Proof: Utility Bill, Rental Agreement
        - Income Proof: Salary Slips, Form 16
        - Bank Statement: Last 6 months statement
        
        ### Document Requirements
        - File size should be less than 5MB
        - Supported formats: PDF, PNG, JPG, JPEG
        - Documents should be clear and readable
        """)

if __name__ == "__main__":
    main()