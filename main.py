import argparse
import csv
import datetime
import sys
import requests

# Nairobi Coordinates
LAT = -1.2921
LON = 36.8219
API_URL = "https://api.openaq.org/v2/measurements"

class NairobiAirQuality:
    def __init__(self, parameter="pm25"):
        self.parameter = parameter
        self.data = []

    def fetch_data(self, limit=24):
        """Fetches air quality data for Nairobi using OpenAQ API."""
        print(f"[*] Fetching last {limit} measurements for {self.parameter} in Nairobi...")
        params = {
            "coordinates": f"{LAT},{LON}",
            "radius": 50000,
            "parameter": self.parameter,
            "limit": limit,
            "order_by": "datetime",
            "sort": "desc"
        }
        try:
            response = requests.get(API_URL, params=params, timeout=15)
            response.raise_for_status()
            results = response.json().get("results", [])
            self.data = [
                {
                    "timestamp": r["date"]["local"],
                    "value": r["value"],
                    "unit": r["unit"],
                    "location": r["location"]
                } for r in results
            ]
            return True
        except Exception as e:
            print(f"[!] Error: {e}")
            return False

    def save_csv(self, filename):
        """Saves fetched data to a CSV file."""
        if not self.data:
            return
        keys = self.data[0].keys()
        try:
            with open(filename, "w", newline="") as f:
                dict_writer = csv.DictWriter(f, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(self.data)
            print(f"[+] Report saved to {filename}")
        except IOError as e:
            print(f"[!] CSV Write Error: {e}")

    def generate_ascii_chart(self):
        """Generates a simple ASCII bar chart of the pollution levels."""
        if not self.data:
            print("[!] No data available to visualize.")
            return

        print("\n--- Nairobi Air Quality Trend (PM2.5) ---")
        max_val = max(d["value"] for d in self.data)
        chart_width = 40

        for entry in reversed(self.data):
            timestamp = entry["timestamp"].split("T")[1][:5]
            val = entry["value"]
            bar_len = int((val / max_val) * chart_width) if max_val > 0 else 0
            bar = "█" * bar_len
            print(f"{timestamp} | {bar} {val:.2f} {entry['unit']}")
        print("-" * (chart_width + 20))

    def print_summary(self):
        """Prints basic statistics."""
        if not self.data:
            return
        values = [d["value"] for d in self.data]
        avg = sum(values) / len(values)
        print(f"Summary for Nairobi:")
        print(f"  - Max Level: {max(values):.2f}")
        print(f"  - Min Level: {min(values):.2f}")
        print(f"  - Average:   {avg:.2f}")
        status = "HEALTHY" if avg < 12 else "MODERATE" if avg < 35 else "UNHEALTHY"
        print(f"  - Status:    {status}")

def main():
    parser = argparse.ArgumentParser(description="Nairobi Air Quality Monitor 2026")
    parser.add_argument("--limit", type=int, default=15, help="Number of recent readings to fetch")
    parser.add_argument("--csv", type=str, default="nairobi_aqi_report.csv", help="Output CSV filename")
    parser.add_argument("--param", type=str, default="pm25", choices=["pm25", "pm10", "no2"], help="Metric to track")
    
    args = parser.parse_args()

    monitor = NairobiAirQuality(parameter=args.param)
    
    if monitor.fetch_data(limit=args.limit):
        monitor.generate_ascii_chart()
        monitor.print_summary()
        monitor.save_csv(args.csv)
    else:
        print("[!] Failed to retrieve data. Check your internet connection.")
        sys.exit(1)

if __name__ == "__main__":
    main()