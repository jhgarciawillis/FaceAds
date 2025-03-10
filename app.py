# app.py
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from io import StringIO

# Import modules
from modules.matrix import define_matrix_structure
from modules.copy_generator import get_claude_prompt, display_copy_generation_instructions
from modules.csv_generator import create_master_csv
from modules.campaign_generator import generate_facebook_campaign_structure
from modules.utils import display_instructions, preview_dataframe, preview_json, create_directory_if_not_exists, validate_csv_format

# Page config
st.set_page_config(
    page_title="Facebook Ad Generator",
    page_icon="📊",
    layout="wide"
)

# Create assets directory if it doesn't exist
create_directory_if_not_exists("assets")

# Ensure the claude prompt file exists
claude_prompt_file = "assets/claude_prompt.txt"
if not os.path.exists(claude_prompt_file):
    with open(claude_prompt_file, "w") as f:
        f.write(get_claude_prompt())

# Initialize session state variables
if "matrix_data" not in st.session_state:
    st.session_state.matrix_data = None
if "copy_data" not in st.session_state:
    st.session_state.copy_data = None
if "master_csv" not in st.session_state:
    st.session_state.master_csv = None
if "campaign_json" not in st.session_state:
    st.session_state.campaign_json = None

# App title
st.title("Facebook Ad Generator")
st.write("Generate targeted Facebook ads for property valuation")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Instructions", "Step 1: Matrix Structure", "Step 2: Copy Generation", 
     "Step 3: Master CSV", "Step 4: Campaign Structure", "All-in-One Workflow"]
)

# Main content
if page == "Instructions":
    st.header("How to Use This Tool")
    
    # Load instructions from file
    with open("assets/instructions.txt", "r") as f:
        instructions = f.read()
    
    # Format the instructions with Markdown
    st.markdown(instructions)
    
    # Add a quick navigation section
    st.subheader("Quick Navigation")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("Start Workflow"):
            st.session_state.page = "All-in-One Workflow"
            st.experimental_rerun()
    with col2:
        if st.button("Step 1"):
            st.session_state.page = "Step 1: Matrix Structure"
            st.experimental_rerun()
    with col3:
        if st.button("Step 2"):
            st.session_state.page = "Step 2: Copy Generation"
            st.experimental_rerun()
    with col4:
        if st.button("Step 3"):
            st.session_state.page = "Step 3: Master CSV"
            st.experimental_rerun()
    with col5:
        if st.button("Step 4"):
            st.session_state.page = "Step 4: Campaign Structure"
            st.experimental_rerun()

elif page == "Step 1: Matrix Structure":
    st.header("Step 1: Define Matrix Structure")
    
    display_instructions("Define the core structure for your ad campaigns, including personas, funnel stages, property types, and locations.")
    
    # Option to customize matrix structure
    with st.expander("Customize Matrix Structure"):
        # Personas
        st.subheader("Personas")
        persona1_name = st.text_input("Persona 1 Name", "Manuel")
        persona1_id = st.text_input("Persona 1 ID", "retiree")
        persona1_age = st.text_input("Persona 1 Age Range", "50-65")
        persona1_situation = st.text_input("Persona 1 Situation", "retirement planning")
        
        st.markdown("---")
        
        persona2_name = st.text_input("Persona 2 Name", "Sofía")
        persona2_id = st.text_input("Persona 2 ID", "family")
        persona2_age = st.text_input("Persona 2 Age Range", "30-45")
        persona2_situation = st.text_input("Persona 2 Situation", "family upgrading")
        
        st.markdown("---")
        
        persona3_name = st.text_input("Persona 3 Name", "Carlos")
        persona3_id = st.text_input("Persona 3 ID", "investor")
        persona3_age = st.text_input("Persona 3 Age Range", "35-55")
        persona3_situation = st.text_input("Persona 3 Situation", "investment properties")
        
        # Property types
        st.subheader("Property Types")
        property_types_text = st.text_area("Enter property types (one per line)", "casa\ndepartamento\nterreno\nlocal comercial")
        
        # Locations
        st.subheader("Locations")
        locations_text = st.text_area("Enter locations (one per line)", "Tampico\nCiudad Madero\nAltamira\nTamaulipas")
    
    if st.button("Generate Matrix Structure"):
        # Parse custom input
        personas = [
            {"id": persona1_id, "name": persona1_name, "age": persona1_age, "situation": persona1_situation},
            {"id": persona2_id, "name": persona2_name, "age": persona2_age, "situation": persona2_situation},
            {"id": persona3_id, "name": persona3_name, "age": persona3_age, "situation": persona3_situation}
        ]
        
        property_types = [p.strip() for p in property_types_text.strip().split("\n") if p.strip()]
        locations = [l.strip() for l in locations_text.strip().split("\n") if l.strip()]
        
        # Create custom matrix
        matrix_data = define_matrix_structure(
            personas=personas,
            property_types=property_types,
            locations=locations
        )
        
        st.session_state.matrix_data = matrix_data
        
        st.success(f"Matrix structure generated with {len(matrix_data['matrix'])} combinations!")
        
        # Preview
        st.subheader("Preview")
        preview_df = pd.DataFrame(matrix_data["matrix"][:5])
        st.dataframe(preview_df)
        
        # Download option
        matrix_json = json.dumps(matrix_data, indent=2)
        st.download_button(
            label="Download Matrix Structure (JSON)",
            data=matrix_json,
            file_name="matrix_structure.json",
            mime="application/json"
        )
        
        # Next steps
        st.info("Next: Go to 'Step 2: Copy Generation' to create ad copy with Claude")

elif page == "Step 2: Copy Generation":
    st.header("Step 2: Generate Copy with Claude")
    
    display_copy_generation_instructions()
    
    # Load Claude prompt template
    with open(claude_prompt_file, "r") as f:
        claude_prompt = f.read()
    
    # Display prompt for Claude
    st.subheader("Claude Prompt")
    st.text_area("Copy this prompt and paste it into Claude:", claude_prompt, height=300)
    
    # Allow direct CSV upload (in case user already has it)
    st.subheader("Upload Copy CSV")
    st.write("If you already have the CSV from Claude, you can upload it here:")
    
    uploaded_file = st.file_uploader("Upload CSV from Claude", type=["csv"])
    if uploaded_file is not None:
        try:
            copy_data = pd.read_csv(uploaded_file)
            
            # Validate CSV format
            required_columns = ["persona_id", "funnel_stage", "headline", "description", "cta_text"]
            is_valid, message = validate_csv_format(copy_data, required_columns)
            
            if is_valid:
                st.session_state.copy_data = copy_data
                st.success("Copy data uploaded successfully!")
                
                # Preview
                st.subheader("Preview")
                st.dataframe(copy_data)
                
                # Next steps
                st.info("Next: Go to 'Step 3: Master CSV' to generate all ad variations")
            else:
                st.error(f"Invalid CSV format: {message}")
        except Exception as e:
            st.error(f"Error loading CSV: {str(e)}")

elif page == "Step 3: Master CSV":
    st.header("Step 3: Create Master CSV")
    
    display_instructions("""
    This step combines your matrix structure with the ad copy to create a comprehensive master CSV 
    containing all ad variations.
    
    You need:
    1. Matrix structure (from Step 1)
    2. Copy data CSV (from Step 2)
    """)
    
    # Check if previous steps are completed
    matrix_ready = st.session_state.matrix_data is not None
    copy_ready = st.session_state.copy_data is not None
    
    if not matrix_ready:
        st.warning("Matrix structure not found. Please complete Step 1 first.")
        if st.button("Go to Step 1"):
            st.session_state.page = "Step 1: Matrix Structure"
            st.experimental_rerun()
    
    if not copy_ready:
        st.warning("Copy data not found. Please complete Step 2 first.")
        # Allow CSV upload here as well
        uploaded_file = st.file_uploader("Upload Copy CSV", type=["csv"])
        if uploaded_file is not None:
            try:
                copy_data = pd.read_csv(uploaded_file)
                
                # Validate CSV format
                required_columns = ["persona_id", "funnel_stage", "headline", "description", "cta_text"]
                is_valid, message = validate_csv_format(copy_data, required_columns)
                
                if is_valid:
                    st.session_state.copy_data = copy_data
                    copy_ready = True
                    st.success("Copy data uploaded successfully!")
                else:
                    st.error(f"Invalid CSV format: {message}")
            except Exception as e:
                st.error(f"Error loading CSV: {str(e)}")
    
    if matrix_ready and copy_ready:
        st.success("All required data is available!")
        
        if st.button("Generate Master CSV"):
            # Create a temporary directory for files
            create_directory_if_not_exists("temp")
            
            # Create a temporary file for the copy data
            temp_csv_path = "temp/temp_copy_data.csv"
            st.session_state.copy_data.to_csv(temp_csv_path, index=False)
            
            # Generate master CSV
            output_file = f"facebook_ads_master_{datetime.now().strftime('%Y%m%d')}.csv"
            master_csv = create_master_csv(
                st.session_state.matrix_data,
                temp_csv_path,
                output_file=f"temp/{output_file}"
            )
            
            # Load the master CSV
            st.session_state.master_csv = pd.read_csv(master_csv)
            
            st.success(f"Master CSV generated with {len(st.session_state.master_csv)} ad variations!")
            
            # Preview
            st.subheader("Preview")
            preview_dataframe(st.session_state.master_csv, 5)
            
            # Download option
            csv_data = st.session_state.master_csv.to_csv(index=False)
            st.download_button(
                label="Download Master CSV",
                data=csv_data,
                file_name=output_file,
                mime="text/csv"
            )
            
            # Next steps
            st.info("Next: Go to 'Step 4: Campaign Structure' to generate Facebook campaign structure")

elif page == "Step 4: Campaign Structure":
    st.header("Step 4: Generate Campaign Structure")
    
    display_instructions("""
    This final step generates a Facebook campaign structure based on your master CSV.
    The structure organizes your ads into campaigns, ad sets, and ad groups for efficient management.
    
    You need:
    1. Master CSV (from Step 3)
    """)
    
    # Check if previous step is completed
    master_csv_ready = st.session_state.master_csv is not None
    
    if not master_csv_ready:
        st.warning("Master CSV not found. Please complete Step 3 first.")
        # Allow CSV upload here as well
        uploaded_file = st.file_uploader("Upload Master CSV", type=["csv"])
        if uploaded_file is not None:
            try:
                master_csv = pd.read_csv(uploaded_file)
                st.session_state.master_csv = master_csv
                master_csv_ready = True
                st.success("Master CSV uploaded successfully!")
            except Exception as e:
                st.error(f"Error loading CSV: {str(e)}")
    
    if master_csv_ready:
        st.success("Master CSV is available!")
        
        if st.button("Generate Campaign Structure"):
            # Create temp directory if it doesn't exist
            create_directory_if_not_exists("temp")
            
            # Create a temporary file for the master CSV
            temp_master_csv = "temp/temp_master_csv.csv"
            st.session_state.master_csv.to_csv(temp_master_csv, index=False)
            
            # Generate campaign structure
            output_file = f"facebook_campaign_structure_{datetime.now().strftime('%Y%m%d')}.json"
            campaign_json = generate_facebook_campaign_structure(temp_master_csv, f"temp/{output_file}")
            
            # Load the campaign JSON
            with open(campaign_json, "r") as f:
                st.session_state.campaign_json = json.load(f)
            
            st.success("Facebook campaign structure generated successfully!")
            
            # Preview
            st.subheader("Preview")
            preview_json(st.session_state.campaign_json)
            
            # Download option
            json_data = json.dumps(st.session_state.campaign_json, indent=2)
            st.download_button(
                label="Download Campaign Structure (JSON)",
                data=json_data,
                file_name=output_file,
                mime="application/json"
            )
            
            # Final instructions
            st.info("""
            ### Next Steps:
            1. Use the master CSV to create images for your ads
            2. Upload the campaign structure to Facebook Ads Manager
            3. Assign your images to the corresponding ads
            """)

elif page == "All-in-One Workflow":
    st.header("Complete Facebook Ad Generation Workflow")
    
    display_instructions("""
    This page allows you to run the entire workflow in one go:
    1. Define matrix structure
    2. Upload copy data from Claude
    3. Generate master CSV
    4. Create Facebook campaign structure
    """)
    
    # Step 1: Matrix Structure
    st.subheader("Step 1: Matrix Structure")
    if st.button("Generate Matrix Structure"):
        st.session_state.matrix_data = define_matrix_structure()
        st.success(f"Matrix structure generated with {len(st.session_state.matrix_data['matrix'])} combinations!")
        
        # Preview
        preview_df = pd.DataFrame(st.session_state.matrix_data["matrix"][:3])
        st.dataframe(preview_df)
    
    # Step 2: Copy Data
    st.subheader("Step 2: Copy Data")
    st.write("Upload the CSV file generated with Claude:")
    uploaded_file = st.file_uploader("Upload Copy CSV", type=["csv"])
    if uploaded_file is not None:
        try:
            copy_data = pd.read_csv(uploaded_file)
            
            # Validate CSV format
            required_columns = ["persona_id", "funnel_stage", "headline", "description", "cta_text"]
            is_valid, message = validate_csv_format(copy_data, required_columns)
            
            if is_valid:
                st.session_state.copy_data = copy_data
                st.success("Copy data uploaded successfully!")
                
                # Preview
                st.dataframe(copy_data)
            else:
                st.error(f"Invalid CSV format: {message}")
        except Exception as e:
            st.error(f"Error loading CSV: {str(e)}")
    
    # Steps 3 & 4: Run if ready
    if st.session_state.matrix_data is not None and st.session_state.copy_data is not None:
        # Create temp directory if it doesn't exist
        create_directory_if_not_exists("temp")
        
        # Step 3: Master CSV
        st.subheader("Step 3: Generate Master CSV")
        if st.button("Generate Master CSV"):
            # Create a temporary file for the copy data
            temp_csv_path = "temp/temp_copy_data.csv"
            st.session_state.copy_data.to_csv(temp_csv_path, index=False)
            
            # Generate master CSV
            output_file = f"facebook_ads_master_{datetime.now().strftime('%Y%m%d')}.csv"
            master_csv = create_master_csv(
                st.session_state.matrix_data,
                temp_csv_path,
                output_file=f"temp/{output_file}"
            )
            
            # Load the master CSV
            st.session_state.master_csv = pd.read_csv(master_csv)
            
            st.success(f"Master CSV generated with {len(st.session_state.master_csv)} ad variations!")
            
            # Preview
            preview_dataframe(st.session_state.master_csv, 3)
            
            # Download option
            csv_data = st.session_state.master_csv.to_csv(index=False)
            st.download_button(
                label="Download Master CSV",
                data=csv_data,
                file_name=output_file,
                mime="text/csv"
            )
    
    # Step 4: Campaign Structure
    if st.session_state.master_csv is not None:
        st.subheader("Step 4: Generate Campaign Structure")
        if st.button("Generate Campaign Structure"):
            # Create a temporary file for the master CSV
            temp_master_csv = "temp/temp_master_csv.csv"
            st.session_state.master_csv.to_csv(temp_master_csv, index=False)
            
            # Generate campaign structure
            output_file = f"facebook_campaign_structure_{datetime.now().strftime('%Y%m%d')}.json"
            campaign_json = generate_facebook_campaign_structure(temp_master_csv, f"temp/{output_file}")
            
            # Load the campaign JSON
            with open(campaign_json, "r") as f:
                st.session_state.campaign_json = json.load(f)
            
            st.success("Facebook campaign structure generated successfully!")
            
            # Preview
            preview_json(st.session_state.campaign_json)
            
            # Download option
            json_data = json.dumps(st.session_state.campaign_json, indent=2)
            st.download_button(
                label="Download Campaign Structure (JSON)",
                data=json_data,
                file_name=output_file,
                mime="application/json"
            )
            
            # Final instructions
            st.success("""
            ### Workflow Complete! Next Steps:
            1. Use the master CSV to create images for your ads
            2. Upload the campaign structure to Facebook Ads Manager
            3. Assign your images to the corresponding ads
            """)