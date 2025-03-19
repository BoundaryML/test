import streamlit as st
import requests
import io
import os
import base64
from PIL import Image
import json
from datetime import datetime

# Set the title and description
st.title("PDF and Image Data Extraction")
st.write("Upload a PDF or image file to extract data using BAML")

# File uploader
uploaded_file = st.file_uploader("Choose a file", type=["pdf", "png", "jpg", "jpeg"])

# API endpoint URL - update this to your actual API URL
API_URL = "http://localhost:8000/extract"  # Change this to your actual API URL

# Create a directory for saving images if it doesn't exist
SAVE_DIR = "extracted_images"
os.makedirs(SAVE_DIR, exist_ok=True)

if uploaded_file is not None:
    # Display the uploaded file
    if uploaded_file.type.startswith('image'):
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    else:
        st.write(f"Uploaded: {uploaded_file.name}")
    
    # Add a button to process the file
    if st.button("Extract Data"):
        with st.spinner("Processing..."):
            try:
                # Create a files dictionary for the request
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                
                # Make the API request
                response = requests.post(API_URL, files=files)
                
                # Check if the request was successful
                if response.status_code == 200:
                    # Get the result
                    result = response.json()
                    
                    # Display the extraction result
                    st.success("Data extracted successfully!")
                    st.subheader("Extracted Data")
                    
                    # Handle the new multi-page results format
                    if "results" in result:
                        # Create tabs for each page's extraction results
                        if len(result["results"]) > 1:
                            tabs = st.tabs([f"Page {item['page']}" for item in result["results"]])
                            for i, tab in enumerate(tabs):
                                with tab:
                                    st.json(result["results"][i]["data"])
                        else:
                            # Just one page, no need for tabs
                            st.json(result["results"][0]["data"])
                    else:
                        # Fallback for old API format
                        st.json(result.get("result", {}))
                    
                    # Handle the images
                    if "images" in result:
                        st.subheader("Extracted Images")
                        
                        # Create a timestamp for unique filenames
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        base_filename = os.path.splitext(uploaded_file.name)[0]
                        
                        # Save each image and display it
                        saved_files = []
                        for img_data in result["images"]:
                            page_num = img_data["page"]
                            img_bytes = base64.b64decode(img_data["image"])
                            
                            # Save the image
                            filename = f"{base_filename}_page{page_num}.png"
                            filepath = os.path.join(SAVE_DIR, filename)
                            
                            with open(filepath, "wb") as f:
                                f.write(img_bytes)
                            
                            saved_files.append(filepath)
                            
                            # Display the image
                            img = Image.open(io.BytesIO(img_bytes))
                            st.image(img, caption=f"Page {page_num}", use_container_width=True)
                        
                        # Provide download links
                        st.subheader("Saved Images")
                        st.write(f"Images saved to directory: {SAVE_DIR}")
                        for filepath in saved_files:
                            st.write(f"- {filepath}")
                    
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Add some instructions and information
st.markdown("""
### How to use this app:
1. Upload a PDF or image file using the file uploader above
2. Click the "Extract Data" button
3. View the extracted data and images below
4. Images are automatically saved to the 'extracted_images' directory

The extraction is powered by BAML and processes all pages of PDF files.
""")