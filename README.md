# Facebook Ad Generator

A Streamlit application for automating the creation of targeted Facebook ad campaigns for property valuation services.

## Overview

This tool helps you create a complete Facebook ad campaign structure with:

- Persona-based targeting
- Funnel stage organization
- Property type and location customization
- AI-generated ad copy (via Claude)

## Features

- **Matrix Structure Generation**: Define personas, funnel stages, property types, and locations
- **Ad Copy Generation**: Use Claude AI to create targeted copy variations
- **Master CSV Creation**: Combine matrix structure with copy to create all ad variations
- **Campaign Structure Generation**: Organize ads into Facebook-ready campaign structure

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/facebook-ad-generator.git
   cd facebook-ad-generator
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

## Workflow Guide

This guide provides a comprehensive workflow for using the Streamlit application to generate your Facebook ads for property valuation.

```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│ Define Matrix │     │  Claude Copy  │     │  Master CSV   │     │   Campaign    │
│   Structure   │────▶│  Generation   │────▶│   Generator   │────▶│   Structure   │
│               │     │               │     │               │     │   Generator   │
└───────────────┘     └───────────────┘     └───────────────┘     └───────────────┘
       │                     │                     │                     │
       ▼                     ▼                     ▼                     ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│ Persona and   │     │ Ad copy with  │     │ Complete ad   │     │ Ready-to-use  │
│ funnel data   │     │ placeholders  │     │ variations    │     │ FB campaign   │
└───────────────┘     └───────────────┘     └───────────────┘     └───────────────┘
```

### Step 1: Define Your Matrix Structure
**Input:** Custom personas, property types, and locations (optional)  
**Output:** Matrix structure with all combinations

1. Navigate to "Step 1: Matrix Structure" in the sidebar
2. You can either:
   - Use the default personas (Manuel, Sofía, Carlos), property types, and locations
   - Customize these elements by expanding the "Customize Matrix Structure" section
3. Click "Generate Matrix Structure" to create all possible combinations
4. Review the preview data and download the JSON if needed
5. The system will store this matrix for subsequent steps

### Step 2: Generate Ad Copy with Claude
**Input:** Claude prompt (provided by the app)  
**Output:** CSV file with copy variations

1. Navigate to "Step 2: Copy Generation" in the sidebar
2. Copy the provided prompt and paste it into Claude AI
3. When Claude responds with the table, you have two options:
   - Copy Claude's response and save it as a CSV file
   - Ask Claude to output the data in CSV format for easier handling
4. Upload the CSV file using the file uploader in the app
5. The system validates that the CSV has the required columns and stores it for the next step

### Step 3: Create Master CSV
**Input:** Matrix data + Claude's copy CSV  
**Output:** Complete master CSV with all ad variations

1. Navigate to "Step 3: Master CSV" in the sidebar
2. If you've completed the previous steps, the required data will be available
3. Click "Generate Master CSV" to create all ad variations
4. Review the preview of the master CSV
5. Download the master CSV file for your records
6. The system stores this data for the final step

### Step 4: Generate Campaign Structure
**Input:** Master CSV  
**Output:** JSON file with Facebook campaign structure

1. Navigate to "Step 4: Campaign Structure" in the sidebar
2. If you've completed Step 3, the master CSV will be available
3. Click "Generate Campaign Structure" to create the campaign JSON
4. Review the campaign structure in the expandable preview
5. Download the JSON file for use with Facebook Ads Manager
6. Follow the "Next Steps" instructions to implement your ads

### All-in-One Workflow

For convenience, you can also use the "All-in-One Workflow" option:

1. Navigate to "All-in-One Workflow" in the sidebar
2. Follow the sequential steps on a single page:
   - Generate Matrix Structure with one click
   - Upload the Claude-generated CSV
   - Generate the Master CSV
   - Create the Campaign Structure
3. Download the required files at each step

## Key Files Generated

1. **Matrix Structure JSON:**
   - Contains personas, funnel stages, property types, and locations
   - Includes all possible combinations

2. **Claude Copy CSV:**
   - 12 rows (3 personas × 4 funnel stages)
   - Contains headlines, descriptions, CTAs with placeholders

3. **Facebook Ads Master CSV:**
   - Many rows (personas × stages × property types × locations)
   - Contains complete ad copy with placeholders filled in

4. **Facebook Campaign Structure JSON:**
   - Hierarchical organization of campaigns, ad sets, and ads
   - Contains targeting parameters for each audience segment

## Next Steps After Using the Application

1. **Image Creation:**
   - Use the master CSV to identify which images you need
   - The `image_code` column follows the format: `{persona_id}_{funnel_stage}_1`
   - Create or source images matching these codes
   - Add text to images manually or with a graphic design tool

2. **Facebook Campaign Setup:**
   - Use the campaign JSON structure as a guide when setting up in Facebook Ads Manager
   - Create campaigns matching the structure
   - Upload your images and assign them to the correct ads

3. **Testing and Optimization:**
   - Start with a small daily budget to test performance
   - Monitor which combinations perform best
   - Scale budget for winning combinations

## Directory Structure
```
facebook-ad-generator/
├── app.py                  # Main Streamlit application
├── modules/                # Application modules
│   ├── __init__.py         # Makes the directory a Python package
│   ├── matrix.py           # Matrix structure generation
│   ├── copy_generator.py   # Instructions for generating copy with Claude
│   ├── csv_generator.py    # Master CSV generation
│   ├── campaign_generator.py  # Campaign structure generation
│   └── utils.py            # Utility functions
├── assets/                 # Asset files
│   └── claude_prompt.txt   # Claude prompt template
├── temp/                   # Temporary files (created at runtime)
├── requirements.txt        # Dependencies
└── README.md               # Project documentation
```

## Requirements

- Python 3.7+
- pandas
- streamlit
- python-dotenv
- Pillow

## License

[MIT](LICENSE)