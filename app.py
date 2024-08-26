import streamlit as st
import pandas as pd
import io
import zipfile

def process_file(df):
    return df.melt(id_vars=df.columns[:2], var_name='Attribute', value_name='Value')

def main():
    st.set_page_config(layout="wide")
    st.title("Excel File Processor")
    
    uploaded_file = st.file_uploader("Upload a zip file containing Excel files", type="zip")
    
    if uploaded_file is not None:
        with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
            excel_files = [f for f in zip_ref.namelist() if f.endswith('.xlsx')]
            
            if not excel_files:
                st.warning("No Excel files found in the uploaded zip.")
                return
            
            output_zip_buffer = io.BytesIO()
            with zipfile.ZipFile(output_zip_buffer, 'w', zipfile.ZIP_DEFLATED) as out_zip:
                for filename in excel_files:
                    with zip_ref.open(filename) as excel_file:
                        df = pd.read_excel(excel_file)
                        processed_df = process_file(df)
                        
                        excel_buffer = io.BytesIO()
                        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                            processed_df.to_excel(writer, index=False)
                        out_zip.writestr(filename, excel_buffer.getvalue())
            
            st.success(f"All {len(excel_files)} files processed successfully!")
            
            st.download_button(
                label="Download processed files",
                data=output_zip_buffer.getvalue(),
                file_name="processed_files.zip",
                mime="application/zip"
            )

if __name__ == "__main__":
    main()
