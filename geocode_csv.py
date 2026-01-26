import csv
import requests
import time

# PUT YOUR GOOGLE API KEY HERE
API_KEY = "AIzaSyA-FgnLuD6u_trXwMhh_mOZaUWtHfUUbcs"

# Input and output file names
INPUT_FILE = "lots_input.csv"
OUTPUT_FILE = "lots_output.csv"

def geocode_address(address):
    """Geocode a single address using Google's Geocoding API"""
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": API_KEY
    }
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if data["status"] == "OK":
            location = data["results"][0]["geometry"]["location"]
            return {
                "lat": round(location["lat"], 7),
                "lng": round(location["lng"], 7),
                "status": "Success"
            }
        else:
            return {
                "lat": "",
                "lng": "",
                "status": f"Error: {data['status']}"
            }
    except Exception as e:
        return {
            "lat": "",
            "lng": "",
            "status": f"Exception: {str(e)}"
        }

def main():
    print(f"Reading CSV file: {INPUT_FILE}")
    print("="*60)
    
    # Read input CSV
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except FileNotFoundError:
        print(f"ERROR: Could not find '{INPUT_FILE}'")
        print(f"Please create a CSV file with columns: LotID,Address")
        return
    except Exception as e:
        print(f"ERROR reading CSV: {str(e)}")
        return
    
    if not rows:
        print("ERROR: CSV file is empty")
        return
    
    # Check for required columns
    if 'LotID' not in rows[0] or 'Address' not in rows[0]:
        print("ERROR: CSV must have 'LotID' and 'Address' columns")
        print(f"Found columns: {list(rows[0].keys())}")
        return
    
    print(f"Found {len(rows)} addresses to geocode\n")
    
    # Process each row
    output_rows = []
    success_count = 0
    fail_count = 0
    
    for i, row in enumerate(rows, 1):
        lot_id = row['LotID']
        address = row['Address']
        
        print(f"[{i}/{len(rows)}] Lot {lot_id}: {address}")
        
        # Geocode the address
        result = geocode_address(address)
        
        # Add lat/lng to the row
        row['Latitude'] = result['lat']
        row['Longitude'] = result['lng']
        row['GeocodeStatus'] = result['status']
        
        output_rows.append(row)
        
        if result['status'] == "Success":
            success_count += 1
            print(f"  ✓ {result['lat']}, {result['lng']}")
        else:
            fail_count += 1
            print(f"  ✗ {result['status']}")
        
        # Sleep to avoid hitting rate limits
        time.sleep(0.1)
    
    # Write output CSV
    if output_rows:
        fieldnames = list(output_rows[0].keys())
        
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(output_rows)
        
        print(f"\n{'='*60}")
        print(f"COMPLETE!")
        print(f"Successfully geocoded: {success_count}")
        print(f"Failed: {fail_count}")
        print(f"Output saved to: {OUTPUT_FILE}")
        print(f"{'='*60}")
    else:
        print("No data to write")

if __name__ == "__main__":
    if API_KEY == "YOUR_API_KEY_HERE":
        print("ERROR: Please replace 'YOUR_API_KEY_HERE' with your actual Google API key")
        print("Edit the script and put your API key on line 6")
    else:
        main()
