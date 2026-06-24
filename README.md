# Nairobi Air Quality 20260624d

A CLI tool to monitor and visualize air quality trends in Nairobi, Kenya.

## Features
- Fetches real-time/recent data from the OpenAQ API.
- Generates ASCII bar charts for terminal visualization.
- Exports detailed data to CSV for further analysis.
- Calculates basic statistics (Min, Max, Avg) and air quality status.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
Run the main script to see the current trend:
```bash
python main.py
```

Customizing the output:
```bash
python main.py --limit 20 --param pm25 --csv my_report.csv
```

## Parameters
- `--limit`: Number of historical data points to fetch (default: 15).
- `--csv`: Custom filename for the CSV report.
- `--param`: The pollutant to track (pm25, pm10, or no2).