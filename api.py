# Import necessary modules
from flask import Flask, request, render_template
from database import database, LogEntry, get_entries_by_ip, get_entries_by_date_range, get_grouped_by_ip, get_grouped_by_date, get_all_entries
import json
import os

# Read configuration from JSON file
config_file_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_file_path) as json_data_file:
    config = json.load(json_data_file)

# Set up Flask app and database connection
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['database']['DB_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database.init_app(app)

# Define endpoint to retrieve logs
@app.route('/logs', methods=['GET'])
def get_logs():
    # Get query parameters
    ip = request.args.get('ip')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Retrieve logs based on query parameters
    if ip:
        entries = get_entries_by_ip(ip)
    elif start_date and end_date:
        entries = get_entries_by_date_range(start_date, end_date)
    else:
        entries = get_all_entries()

    # Render logs using HTML template
    return render_template("test.html", entries=[entry.to_dict() for entry in entries])

# Define endpoint to retrieve grouped logs
@app.route('/logs/grouped', methods=['GET'])
def get_grouped_logs():
    # Get query parameters
    group_by = request.args.get('group_by')
    sort_by = request.args.get('sort_by', 'ip')
    sort_order = request.args.get('sort_order', 'asc')

    # Group logs by IP or date
    if group_by == 'ip':
        entries = get_grouped_by_ip()
    elif group_by == 'date':
        entries = get_grouped_by_date()
    else:
        entries = [entry.to_dict() for entry in get_all_entries()]

    # Sort logs based on sorting parameters
    entries = sort_entries(entries, sort_by, sort_order)

    # Render logs using HTML template
    return render_template('test_group.html', entries=entries)

# Define function to sort logs
def sort_entries(entries, sort_by, sort_order):
    reverse = False
    if sort_order == 'desc':
        reverse = True
    return sorted(entries, key=lambda entry: entry.get(sort_by, ''), reverse=reverse)

# Initialize database and run Flask app
if __name__ == '__main__':
    with app.app_context():
        database.create_all()
    app.run(host=config['API']['API_HOST'], port=config['API']['API_PORT'])