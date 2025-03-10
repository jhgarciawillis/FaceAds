# modules/copy_generator.py
import streamlit as st

def get_claude_prompt():
    """
    Returns the prompt template for Claude to generate ad copy
    """
    return """
Please create a structured table with 12 variations of Facebook ad copy for a property valuation tool, covering each combination of persona and funnel stage.

Personas:
1. Manuel (Retiree): 50-65 years old, considering downsizing for retirement
2. Sofía (Family): 30-45 years old, family outgrown current home
3. Carlos (Investor): 35-55 years old, owns multiple properties

Funnel Stages:
1. Awareness: Just learning about property valuation
2. Interest: Considering valuing their property
3. Decision: Ready to get a valuation
4. Action: Ready to complete valuation form

For each combination, provide:
1. Headline (max 40 chars)
2. Description (max 125 chars)
3. CTA text

Format as a CSV table with these columns:
persona_id,funnel_stage,headline,description,cta_text

Use these personas and funnel stages as identifiers:
- Personas: retiree, family, investor
- Funnel stages: awareness, interest, decision, action

Include relevant Spanish text with property placeholders like {property_type} and {location} where appropriate.
"""

def display_copy_generation_instructions():
    """
    Displays instructions for generating copy with Claude
    """
    st.info("""
    ### How to Generate Ad Copy with Claude:
    
    1. **Copy the prompt** below and paste it into Claude AI
    2. Claude will generate a table with ad copy variations
    3. **Copy Claude's response** and save it as a CSV file
    4. Make sure the CSV has these columns: `persona_id`, `funnel_stage`, `headline`, `description`, `cta_text`
    5. Upload the CSV in the next step
    
    Tip: If Claude formats the result as markdown, ask it to provide the output as CSV format only.
    """)