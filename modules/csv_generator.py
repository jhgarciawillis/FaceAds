# modules/csv_generator.py
import pandas as pd
import os
from datetime import datetime
import streamlit as st

def create_master_csv(matrix_data, copy_data_csv, output_file=None):
    """
    Create a master CSV by combining the matrix structure with copy data
    
    Parameters:
    - matrix_data: Output from define_matrix_structure()
    - copy_data_csv: Path to CSV with copy variations from Claude
    - output_file: Path to save the master CSV (optional)
    
    Returns:
    - Path to the created CSV file
    """
    # Set default output filename if not provided
    if output_file is None:
        output_file = f"facebook_ads_master_{datetime.now().strftime('%Y%m%d')}.csv"
        
    # Load the copy data
    copy_df = pd.read_csv(copy_data_csv)
    
    # Create rows for the master CSV
    rows = []
    ad_id = 1
    
    # Track missing combinations for reporting
    missing_combinations = []
    
    for item in matrix_data["matrix"]:
        # Find matching copy
        copy_match = copy_df[(copy_df["persona_id"] == item["persona_id"]) & 
                            (copy_df["funnel_stage"] == item["funnel_stage"])]
        
        if not copy_match.empty:
            copy_row = copy_match.iloc[0]
            
            # Replace placeholders in copy
            headline = copy_row["headline"].replace("{property_type}", item["property_type"]).replace("{location}", item["location"])
            description = copy_row["description"].replace("{property_type}", item["property_type"]).replace("{location}", item["location"])
            
            # Add row to master CSV
            rows.append({
                "ad_id": f"AD{ad_id:04d}",
                "persona_id": item["persona_id"],
                "persona_name": item["persona_name"],
                "funnel_stage": item["funnel_stage"],
                "property_type": item["property_type"],
                "location": item["location"],
                "headline": headline,
                "description": description,
                "cta_text": copy_row["cta_text"],
                "image_code": f"{item['persona_id']}_{item['funnel_stage']}_1"
            })
            ad_id += 1
        else:
            # Record missing combination
            missing_combinations.append(f"{item['persona_id']}_{item['funnel_stage']}")
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(rows)
    df.to_csv(output_file, index=False)
    
    # Report missing combinations if any
    if missing_combinations:
        unique_missing = list(set(missing_combinations))
        st.warning(f"Missing copy for {len(unique_missing)} persona-stage combinations: {', '.join(unique_missing)}")
    
    print(f"Generated master CSV with {len(rows)} ad variations: {output_file}")
    return output_file