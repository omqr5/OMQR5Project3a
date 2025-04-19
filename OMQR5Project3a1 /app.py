from flask import Flask, render_template, request, redirect, url_for, flash
from stock_api import fetch_stock_data
from chart_generator import generate_chart
from utils import validate_date_range

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing error messages

@app.route('/', methods=['GET', 'POST'])
def index():
    chart_data = None

    if request.method == 'POST':
        symbol = request.form.get('symbol', '').upper()
        chart_type = request.form.get('chart_type', 'line')
        time_series = request.form.get('time_series', 'DAILY')
        start_date = request.form.get('start_date', '')
        end_date = request.form.get('end_date', '')

        if not symbol:
            flash('Please enter a stock symbol.')
            return redirect(url_for('index'))

        if not validate_date_range(start_date, end_date):
            flash('Invalid date range. Please try again.')
            return redirect(url_for('index'))

        data = fetch_stock_data(symbol, time_series)

        if data:
            chart_data = generate_chart(data, chart_type, start_date, end_date, symbol)
        else:
            flash('Failed to retrieve stock data.')

    return render_template('index.html', chart_data=chart_data)

if __name__ == '__main__':
    app.run(debug=True)
