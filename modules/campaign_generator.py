# modules/campaign_generator.py
import json
import os
import pandas as pd
from datetime import datetime
import streamlit as st

def generate_facebook_campaign_structure(master_csv_file, output_file=None):
    """
    Generate a JSON structure for Facebook ad campaigns based on the master CSV
    
    Parameters:
    - master_csv_file: Path to the master CSV
    - output_file: Path to save the campaign structure JSON (optional)
    
    Returns:
    - Path to the created JSON file
    """
    if output_file is None:
        output_file = f"facebook_campaign_structure_{datetime.now().strftime('%Y%m%d')}.json"
    
    # Load master CSV
    df = pd.read_csv(master_csv_file)
    
    # Create campaign structure
    campaigns = {}
    
    # Get unique funnel stages, personas, and locations
    funnel_stages = df["funnel_stage"].unique()
    personas = df[["persona_id", "persona_name"]].drop_duplicates().to_dict('records')
    locations = df["location"].unique()
    
    # Group by funnel stage (campaigns)
    for stage in funnel_stages:
        stage_df = df[df['funnel_stage'] == stage]
        
        # Group by persona (ad sets)
        ad_sets = {}
        for persona in personas:
            persona_id = persona["persona_id"]
            persona_name = persona["persona_name"]
            persona_df = stage_df[stage_df['persona_id'] == persona_id]
            
            if persona_df.empty:
                continue
            
            # Group by location (targeting variations)
            location_groups = {}
            for location in locations:
                location_df = persona_df[persona_df['location'] == location]
                
                if location_df.empty:
                    continue
                
                # List all ads for this combination
                ads = []
                for _, row in location_df.iterrows():
                    ads.append({
                        "ad_id": row['ad_id'],
                        "headline": row['headline'],
                        "description": row['description'],
                        "cta_text": row['cta_text'],
                        "image_code": row['image_code'],
                        "property_type": row['property_type']
                    })
                
                # Add location group if ads exist
                if ads:
                    location_groups[location] = {
                        "name": f"{stage.capitalize()} - {persona_name} - {location}",
                        "ads": ads
                    }
            
            # Add persona group if locations exist
            if location_groups:
                ad_sets[persona_id] = {
                    "name": f"{stage.capitalize()} - {persona_name}",
                    "targeting": get_targeting_params(persona_id),
                    "locations": location_groups
                }
        
        # Add stage campaign if ad sets exist
        if ad_sets:
            campaigns[stage] = {
                "name": f"Property Valuation - {stage.capitalize()}",
                "objective": get_campaign_objective(stage),
                "ad_sets": ad_sets
            }
    
    # Export campaign structure as JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(campaigns, f, indent=2, ensure_ascii=False)
    
    return output_file

def get_targeting_params(persona_id):
    """Generate targeting parameters based on persona"""
    targeting = {
        "retiree": {
            "age_min": 50,
            "age_max": 65,
            "interests": ["retirement planning", "investment properties", "downsizing home"]
        },
        "family": {
            "age_min": 30,
            "age_max": 45,
            "interests": ["family housing", "home upgrade", "growing family", "school districts"]
        },
        "investor": {
            "age_min": 35,
            "age_max": 55,
            "interests": ["real estate investment", "property portfolio", "rental properties"]
        }
    }
    
    return targeting.get(persona_id, {
        "age_min": 25,
        "age_max": 65,
        "interests": ["real estate", "home ownership"]
    })

def get_campaign_objective(funnel_stage):
    """Get Facebook campaign objective based on funnel stage"""
    objectives = {
        "awareness": "BRAND_AWARENESS",
        "interest": "TRAFFIC",
        "decision": "LEAD_GENERATION",
        "action": "CONVERSIONS"
    }
    return objectives.get(funnel_stage, "TRAFFIC")