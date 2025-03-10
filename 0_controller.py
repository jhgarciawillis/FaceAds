def run_workflow():
    print("=== Facebook Ad Generation System ===")
    
    print("\n1. Defining matrix structure...")
    matrix = define_matrix_structure()
    print(f"Created matrix with {len(matrix['matrix'])} combinations")
    
    print("\n2. Loading copy variations...")
    copy_csv = input("Enter path to Claude-generated copy CSV: ")
    
    print("\n3. Creating master CSV...")
    master_csv = create_master_csv(matrix, copy_csv)
    
    print("\n4. Generating Facebook campaign structure...")
    campaign_json = generate_facebook_campaign_structure(master_csv)
    
    print("\n=== Workflow Complete ===")
    print(f"Master CSV: {master_csv}")
    print(f"Campaign Structure: {campaign_json}")
    print("\nNext steps:")
    print("1. Use the master CSV to create images with your preferred tool")
    print("2. Upload ads to Facebook using the campaign structure as a guide")

if __name__ == "__main__":
    run_workflow()