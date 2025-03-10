# modules/copy_generator.py
import streamlit as st

def get_claude_prompt():
    """
    Returns a simple default prompt for Claude.
    This is only used if claude_prompt.txt doesn't exist yet.
    """
    return """Please create 12 variations of Facebook ad copy for a property valuation tool in CSV format, covering each combination of persona and funnel stage.

Detailed Persona Insights 
Retiree Persona (Manuel, 50-65 years):
**Pain Points:**
- Awareness: Uncertainty about property value for retirement planning
- Interest: Fear of making financial mistakes as retirement approaches
- Decision: Stress about whether to sell now or wait longer
- Action: Anxiety about getting an accurate valuation without hassle

**Benefits:**
- Awareness: Clear understanding of your property's value for retirement planning
- Interest: Data-backed insights to inform critical retirement decisions
- Decision: Expert valuation to maximize retirement nest egg
- Action: Quick hassle-free process designed for your peace of mind

**CTA Style:** Professional reassuring emphasizing security and peace of mind

Family Persona (Sofía, 30-45 years):
**Pain Points:**
- Awareness: Growing family needs more space but uncertain about current equity
- Interest: Stress about affording a larger home for your family
- Decision: Uncertainty about timing the market for maximum value
- Action: Lack of time to research property values while managing family life

**Benefits:**
- Awareness: Discover if you have enough equity to upgrade to a larger home
- Interest: Tailored insights for families looking to upgrade their living space
- Decision: Expert guidance to maximize your home's value for your next family move
- Action: Quick mobile-friendly valuation that fits your busy family schedule

**CTA Style:** Warm practical emphasizing family needs and future planning

Investor Persona (Carlos, 35-55 years):
**Pain Points:**
- Awareness: Difficulty assessing portfolio performance without current valuations
- Interest: Challenge of identifying underperforming properties in your portfolio
- Decision: Market timing concerns for maximizing investment returns
- Action: Time wasted on inaccurate valuations or dealing with agents

**Benefits:**
- Awareness: Gain a clear picture of your property portfolio's current value
- Interest: Data-driven insights to optimize your investment strategy
- Decision: Market intelligence to maximize returns on your property investments
- Action: Efficient valuation process designed for serious property investors

**CTA Style:** Direct data-focused emphasizing ROI and strategic decision-making

Ad Copy Requirements and CSV Format Instructions

1. Your response must begin with "persona_id,funnel_stage,headline,description,cta_text" as the header row
2. Each subsequent row must contain exactly 5 fields in the specified order
3. ALL text fields must be enclosed in double quotes (")
4. Do NOT use commas in headlines at all
5. If commas are needed in descriptions or CTAs, ensure the entire text is properly enclosed in quotes
6. Keep headlines under 40 characters
7. Keep descriptions under 125 characters
8. Use Spanish text with property placeholders like {property_type} and {location} where appropriate

CSV Formatting Rules:
- Begin with the header row
- Provide exactly 12 rows of data (one for each persona/funnel stage combination)
- Ensure ALL fields are properly quoted with double quotes
- Check that no unescaped quotes appear in the text
- Format as plain text CSV with no markdown or other formatting
- Each line should follow this exact format: "persona_id","funnel_stage","headline","description","cta_text"

Personas and Stages:
- Personas: retiree, family, investor
- Funnel stages: awareness, interest, decision, action

Make the copy emotionally resonant, targeted, and compelling. Each ad should clearly speak to the specific persona's situation, fears, and desires at their particular funnel stage.
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