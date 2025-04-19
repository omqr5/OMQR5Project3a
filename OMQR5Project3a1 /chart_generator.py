import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt # type: ignore
from datetime import datetime
import os
import webbrowser

def generate_chart(data, chart_type, start_date, end_date, symbol):
    # Identify the correct time series key from the API response
    time_series_key = next((key for key in data if 'Time Series' in key), None)
    if not time_series_key:
        print("Could not find time series data in API response.")
        return

    raw_data = data[time_series_key]

    # Filter and sort the data based on date range
    filtered_dates = []
    closing_prices = []

    for date_str in sorted(raw_data.keys()):
        if start_date <= date_str <= end_date:
            filtered_dates.append(datetime.strptime(date_str, "%Y-%m-%d"))
            closing_prices.append(float(raw_data[date_str]["4. close"]))

    if not filtered_dates:
        print("No stock data found in the selected date range.")
        return

    # Plots the chart
    plt.figure(figsize=(12, 6))
    if chart_type == "line":
        plt.plot(filtered_dates, closing_prices, marker='o', linestyle='-', color='blue')
    elif chart_type == "bar":
        plt.bar(filtered_dates, closing_prices, color='skyblue')
    else:
        print("Unsupported chart type.")
        return

    # Add labels and title
    plt.xlabel("Date")
    plt.ylabel("Closing Price (USD)")
    plt.title(f"{symbol} Stock Prices ({start_date} to {end_date})")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)

    # Save chart as file and open in browser
    filename = f"{symbol}_{start_date}_to_{end_date}.png"
    plt.savefig(filename)
    plt.close()

    print(f"\nChart saved as: {filename}")
    abs_path = os.path.abspath(filename)
    webbrowser.open(f"file://{abs_path}")
