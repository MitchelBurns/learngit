import requests
import json
import time

# PUT YOUR GOOGLE API KEY HERE
API_KEY = "AIzaSyA-FgnLuD6u_trXwMhh_mOZaUWtHfUUbcs"

# Your lot addresses
lots_addresses = [
    {"lotNumber": "2", "address": "113 N Haystack Mountain Drive, Heber City, UT 84032"},
    {"lotNumber": "11", "address": "142 N Haystack Mountain Drive, Heber City, UT 84032"},
    {"lotNumber": "12", "address": "150 N Haystack Mountain Drive, Heber City, UT 84032"},
    {"lotNumber": "13", "address": "158 N Haystack Mountain Drive, Heber City, UT 84032"},
    {"lotNumber": "14", "address": "157 N Haystack Mountain Drive, Heber City, UT 84032"},
    {"lotNumber": "15", "address": "165 N Haystack Mountain Drive, Heber City, UT 84032"},
    {"lotNumber": "16", "address": "191 N Haystack Mountain Drive, Heber City, UT 84032"},
    {"lotNumber": "17", "address": "215 N Haystack Mountain Drive, Heber City, UT 84032"},
    {"lotNumber": "18", "address": "255 N Haystack Mountain Drive, Heber City, UT 84032"},
    {"lotNumber": "19", "address": "285 N Haystack Mountain Drive, Heber City, UT 84032"},
    {"lotNumber": "20", "address": "230 N Haystack Mountain Drive, Heber City, UT 84032"},
    {"lotNumber": "102", "address": "2881 E Brown Duck Mountain Circle, Heber City, UT 84032"},
    {"lotNumber": "103", "address": "2880 E Brown Duck Mountain Circle, Heber City, UT 84032"},
    {"lotNumber": "104", "address": "2884 E Brown Duck Mountain Circle, Heber City, UT 84032"},
    {"lotNumber": "105", "address": "2888 E Brown Duck Mountain Circle, Heber City, UT 84032"},
    {"lotNumber": "106", "address": "2900 E Brown Duck Mountain Circle, Heber City, UT 84032"},
    {"lotNumber": "107", "address": "2910 E Brown Duck Mountain Circle, Heber City, UT 84032"},
    {"lotNumber": "108", "address": "2918 E Brown Duck Mountain Circle, Heber City, UT 84032"},
    {"lotNumber": "109", "address": "2930 E Brown Duck Mountain Circle, Heber City, UT 84032"},
    {"lotNumber": "110", "address": "601 N Red Ledges Boulevard, Heber City, UT 84032"},
    {"lotNumber": "111", "address": "565 N Red Ledges Boulevard, Heber City, UT 84032"},
    {"lotNumber": "112", "address": "551 N Red Ledges Boulevard, Heber City, UT 84032"},
    {"lotNumber": "113", "address": "537 N Red Ledges Boulevard, Heber City, UT 84032"},
    {"lotNumber": "114", "address": "511 N Red Ledges Boulevard, Heber City, UT 84032"},
    {"lotNumber": "115", "address": "481 N Red Ledges Boulevard, Heber City, UT 84032"},
    {"lotNumber": "116", "address": "445 N Red Ledges Boulevard, Heber City, UT 84032"},
    {"lotNumber": "117", "address": "427 N Red Ledges Boulevard, Heber City, UT 84032"},
    {"lotNumber": "118", "address": "393 N Red Ledges Boulevard, Heber City, UT 84032"},
    {"lotNumber": "119", "address": "355 N Red Ledges Boulevard, Heber City, UT 84032"},
    {"lotNumber": "120", "address": "311 N Red Ledges Boulevard, Heber City, UT 84032"},
    {"lotNumber": "121", "address": "295 N Red Ledges Boulevard, Heber City, UT 84032"},
    {"lotNumber": "122", "address": "271 N Red Ledges Boulevard, Heber City, UT 84032"},
    {"lotNumber": "123", "address": "330 N Red Ledges Boulevard, Heber City, UT 84032"},
    {"lotNumber": "124", "address": "310 N Red Ledges Boulevard, Heber City, UT 84032"},
    {"lotNumber": "125", "address": "304 N Red Ledges Boulevard, Heber City, UT 84032"},
    {"lotNumber": "126", "address": "280 N Red Ledges Boulevard, Heber City, UT 84032"},
    {"lotNumber": "127", "address": "205 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "128", "address": "209 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "129", "address": "223 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "130", "address": "229 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "131", "address": "235 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "132", "address": "241 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "133", "address": "253 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "134", "address": "206 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "135", "address": "212 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "136", "address": "216 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "137", "address": "220 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "138", "address": "224 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "139", "address": "228 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "140", "address": "234 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "141", "address": "240 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "142", "address": "3050 E Corral Peak Circle, Heber City, UT 84032"},
    {"lotNumber": "143", "address": "3088 E Corral Peak Circle, Heber City, UT 84032"},
    {"lotNumber": "144", "address": "3090 E Corral Peak Circle, Heber City, UT 84032"},
    {"lotNumber": "145", "address": "3097 E Corral Peak Circle, Heber City, UT 84032"},
    {"lotNumber": "146", "address": "3081 E Corral Peak Circle, Heber City, UT 84032"},
    {"lotNumber": "147", "address": "3057 E Corral Peak Circle, Heber City, UT 84032"},
    {"lotNumber": "148", "address": "3035 E Corral Peak Circle, Heber City, UT 84032"},
    {"lotNumber": "149", "address": "280 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "150", "address": "292 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "151", "address": "304 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "152", "address": "312 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "153", "address": "3226 E Horseshoe Canyon Circle, Heber City, UT 84032"},
    {"lotNumber": "154", "address": "3290 E Horseshoe Canyon Circle, Heber City, UT 84032"},
    {"lotNumber": "155", "address": "3330 E Horseshoe Canyon Circle, Heber City, UT 84032"},
    {"lotNumber": "156", "address": "3336 E Horseshoe Canyon Circle, Heber City, UT 84032"},
    {"lotNumber": "157", "address": "3340 E Horseshoe Canyon Circle, Heber City, UT 84032"},
    {"lotNumber": "158", "address": "3335 E Horseshoe Canyon Circle, Heber City, UT 84032"},
    {"lotNumber": "159", "address": "3311 E Horseshoe Canyon Circle, Heber City, UT 84032"},
    {"lotNumber": "160", "address": "3225 E Horseshoe Canyon Circle, Heber City, UT 84032"},
    {"lotNumber": "161", "address": "362 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "162", "address": "390 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "163", "address": "420 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "164", "address": "444 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "165", "address": "466 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "166", "address": "3220 E Horsehead Peak Court, Heber City, UT 84032"},
    {"lotNumber": "167", "address": "3246 E Horsehead Peak Court, Heber City, UT 84032"},
    {"lotNumber": "168", "address": "3250 E Horsehead Peak Court, Heber City, UT 84032"},
    {"lotNumber": "169", "address": "3245 E Horsehead Peak Court, Heber City, UT 84032"},
    {"lotNumber": "170", "address": "3231 E Horsehead Peak Court, Heber City, UT 84032"},
    {"lotNumber": "171", "address": "3205 E Horsehead Peak Court, Heber City, UT 84032"},
    {"lotNumber": "172", "address": "556 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "173", "address": "590 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "174", "address": "618 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "175", "address": "634 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "176", "address": "650 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "177", "address": "657 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "178", "address": "637 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "179", "address": "623 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "180", "address": "605 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "181", "address": "595 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "182", "address": "583 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "183", "address": "567 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "184", "address": "551 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "185", "address": "515 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "186", "address": "3155 E Horse Mountain Circle, Heber City, UT 84032"},
    {"lotNumber": "187", "address": "3125 E Horse Mountain Circle, Heber City, UT 84032"},
    {"lotNumber": "188", "address": "3101 E Horse Mountain Circle, Heber City, UT 84032"},
    {"lotNumber": "189", "address": "3077 E Horse Mountain Circle, Heber City, UT 84032"},
    {"lotNumber": "190", "address": "3055 E Horse Mountain Circle, Heber City, UT 84032"},
    {"lotNumber": "191", "address": "3050 E Horse Mountain Circle, Heber City, UT 84032"},
    {"lotNumber": "192", "address": "3052 E Horse Mountain Circle, Heber City, UT 84032"},
    {"lotNumber": "193", "address": "3060 E Horse Mountain Circle, Heber City, UT 84032"},
    {"lotNumber": "194", "address": "3090 E Horse Mountain Circle, Heber City, UT 84032"},
    {"lotNumber": "195", "address": "3120 E Horse Mountain Circle, Heber City, UT 84032"},
    {"lotNumber": "196", "address": "3140 E Horse Mountain Circle, Heber City, UT 84032"},
    {"lotNumber": "197", "address": "3166 E Horse Mountain Circle, Heber City, UT 84032"},
    {"lotNumber": "198", "address": "347 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "199", "address": "307 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "200", "address": "295 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "201", "address": "289 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "202", "address": "283 N Ibapah Peak Drive, Heber City, UT 84032"},
    {"lotNumber": "203", "address": "141 N Haystack Mountain Drive, Heber City, UT 84032"},
    {"lotNumber": "204", "address": "149 N Haystack Mountain Drive, Heber City, UT 84032"},
    {"lotNumber": "205", "address": "725 N Red Mountain Court, Heber City, UT 84032"},
    {"lotNumber": "206", "address": "693 N Red Mountain Court, Heber City, UT 84032"},
    {"lotNumber": "207", "address": "669 N Red Mountain Court, Heber City, UT 84032"},
    {"lotNumber": "208", "address": "645 N Red Mountain Court, Heber City, UT 84032"},
]

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
                "lng": round(location["lng"], 7)
            }
        else:
            print(f"Error geocoding {address}: {data['status']}")
            return None
    except Exception as e:
        print(f"Exception geocoding {address}: {str(e)}")
        return None

def main():
    print(f"Starting geocoding of {len(lots_addresses)} addresses...")
    print("This will take about 2 minutes (to avoid API rate limits)...\n")
    
    lots_data = []
    failed_addresses = []
    
    for i, lot in enumerate(lots_addresses, 1):
        print(f"[{i}/{len(lots_addresses)}] Geocoding Lot {lot['lotNumber']}: {lot['address']}")
        
        coordinates = geocode_address(lot["address"])
        
        if coordinates:
            lots_data.append({
                "lotNumber": lot["lotNumber"],
                "address": lot["address"],
                "coordinates": coordinates,
                "size": "TBD",
                "status": "Available",
                "price": "Contact for pricing",
                "features": ["Red Ledges Community", "Mountain views"]
            })
            print(f"  ✓ Success: {coordinates}")
        else:
            failed_addresses.append(lot)
            print(f"  ✗ Failed")
        
        # Sleep to avoid hitting rate limits (Google allows 50 requests/second)
        time.sleep(0.1)
    
    # Save to JSON file
    output = {"lots": lots_data}
    
    with open("lots_geocoded.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"COMPLETE!")
    print(f"Successfully geocoded: {len(lots_data)} lots")
    print(f"Failed: {len(failed_addresses)} lots")
    print(f"Output saved to: lots_geocoded.json")
    print(f"{'='*60}")
    
    if failed_addresses:
        print("\nFailed addresses:")
        for lot in failed_addresses:
            print(f"  - Lot {lot['lotNumber']}: {lot['address']}")

if __name__ == "__main__":
    if API_KEY == "YOUR_API_KEY_HERE":
        print("ERROR: Please replace 'YOUR_API_KEY_HERE' with your actual Google API key")
        print("Edit the script and put your API key on line 6")
    else:
        main()
