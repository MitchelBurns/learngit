import csv
import json

# Input and output file names
INPUT_CSV = "lots_output.csv"
OUTPUT_JSON = "lots.json"

def convert_csv_to_json():
    """Convert geocoded CSV to JSON format for the web app"""
    
    try:
        with open(INPUT_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except FileNotFoundError:
        print(f"ERROR: Could not find '{INPUT_CSV}'")
        print("Please run geocode_csv.py first to create this file")
        return
    
    lots = []
    
    for row in rows:
        # Only include successfully geocoded lots
        if row.get('GeocodeStatus') == 'Success' and row.get('Latitude') and row.get('Longitude'):
            lot = {
                "lotNumber": row.get('LotId', ''),
                "lotIdCRM": row.get('LotIdCRM', ''),
                "address": row.get('Address', ''),
                "coordinates": {
                    "lat": float(row.get('Latitude', 0)),
                    "lng": float(row.get('Longitude', 0))
                },
                "acreage": row.get('Acreage', 'TBD'),
                "hasWaterAssessment": row.get('HasWaterAssessment', 'Unknown'),
                "isAvailable": row.get('IsAvailable', 'Unknown'),
                "lotType": row.get('LotTypeDescription', 'TBD'),
                "phaseName": row.get('PhaseName', 'TBD'),
                "membershipType": row.get('MembershipType', 'TBD'),
                "membershipStatus": row.get('MembershipStatus', 'TBD'),
                "jonasMemberNumber": row.get('JonasMemberNumber', 'TBD'),
                "membershipPeriod": row.get('MembershipPeriod', 'TBD'),
                "ownerName": row.get('OwnerName', 'Available')
            }
            lots.append(lot)
    
    output = {"lots": lots}
    
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    
    print(f"Successfully converted {len(lots)} lots to {OUTPUT_JSON}")

if __name__ == "__main__":
    convert_csv_to_json()
