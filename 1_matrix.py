# Simple matrix structure definition
def define_matrix_structure():
    # Core matrix structure - simple Python dictionaries
    personas = [
        {"id": "retiree", "name": "Manuel", "age": "50-65", "situation": "retirement planning"},
        {"id": "family", "name": "Sofía", "age": "30-45", "situation": "family upgrading"},
        {"id": "investor", "name": "Carlos", "age": "35-55", "situation": "investment properties"}
    ]

    funnel_stages = [
        {"id": "awareness", "intent": "discovery", "cta_type": "learn more"},
        {"id": "interest", "intent": "consideration", "cta_type": "get value"},
        {"id": "decision", "intent": "evaluation", "cta_type": "free valuation"},
        {"id": "action", "intent": "conversion", "cta_type": "value now"}
    ]

    property_types = ["casa", "departamento", "terreno", "local comercial"]
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