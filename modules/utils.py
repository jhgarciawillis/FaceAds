# modules/utils.py
import streamlit as st
import pandas as pd
import json

def display_instructions(text):
    """Display instructions in a clean info box"""
    st.info(text)

def preview_dataframe(df, rows=5):
    """Display a preview of a dataframe with option to see more"""
    st.dataframe(df.head(rows))
    
    with st.expander("See all data"):
        st.dataframe(df)

def preview_json(json_data):
    """Display a preview of JSON data"""
    # Show first level keys
    st.write("Campaign Structure Overview:")
    
    for key in json_data:
        st.write(f"Campaign: {json_data[key]['name']}")
        
        # Expandable section for each campaign
        with st.expander(f"View details for {json_data[key]['name']}"):
            st.write(f"- Objective: {json_data[key]['objective']}")
            st.write(f"- Number of ad sets: {len(json_data[key]['ad_sets'])}")
            
            # Ad sets
            for ad_set_key, ad_set in json_data[key]['ad_sets'].items():
                st.write(f"  - Ad Set: {ad_set['name']}")
                st.write(f"    - Targeting: {ad_set['targeting']}")
                
                # Count total ads
                total_ads = sum(len(location['ads']) for location in ad_set['locations'].values())
                st.write(f"    - Total ads: {total_ads}")

def create_directory_if_not_exists(directory):
    """Create directory if it doesn't exist"""
    import os
    if not os.path.exists(directory):
        os.makedirs(directory)
        return True
    return False

def validate_csv_format(df, required_columns):
    """Validate that a DataFrame has the required columns"""
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    return True, "CSV format is valid"