# modules/matrix.py
def define_matrix_structure(personas=None, funnel_stages=None, property_types=None, locations=None):
    """
    Define the matrix structure for ad generation
    
    Parameters:
    - personas: List of persona dictionaries (optional)
    - funnel_stages: List of funnel stage dictionaries (optional)
    - property_types: List of property types (optional)
    - locations: List of locations (optional)
    
    Returns:
    - Dictionary with matrix structure
    """
    # Default values if not provided
    if personas is None:
        personas = [
            {"id": "retiree", "name": "Manuel", "age": "50-65", "situation": "retirement planning"},
            {"id": "family", "name": "Sofía", "age": "30-45", "situation": "family upgrading"},
            {"id": "investor", "name": "Carlos", "age": "35-55", "situation": "investment properties"}
        ]
    
    if funnel_stages is None:
        funnel_stages = [
            {"id": "awareness", "intent": "discovery", "cta_type": "learn more"},
            {"id": "interest", "intent": "consideration", "cta_type": "get value"},
            {"id": "decision", "intent": "evaluation", "cta_type": "free valuation"},
            {"id": "action", "intent": "conversion", "cta_type": "value now"}
        ]
    
    if property_types is None:
        property_types = ["casa", "departamento", "terreno", "local comercial"]
    
    if locations is None:
        locations = ["Tampico", "Ciudad Madero", "Altamira", "Tamaulipas"]

    # Create combinations matrix
    matrix = []
    for persona in personas:
        for stage in funnel_stages:
            for prop_type in property_types:
                for location in locations:
                    matrix.append({
                        "persona_id": persona["id"],
                        "persona_name": persona["name"],
                        "funnel_stage": stage["id"],
                        "property_type": prop_type,
                        "location": location,
                    })

    return {
        "personas": personas,
        "funnel_stages": funnel_stages,
        "property_types": property_types,
        "locations": locations,
        "matrix": matrix
    }