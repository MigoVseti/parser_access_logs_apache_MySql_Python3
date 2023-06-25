import re
from database import LogEntry, add_entry_to_database, database, app
from datetime import datetime
import json
import os

config_file_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_file_path) as json_data_file:
    config = json.load(json_data_file)

log_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', config['logs']['directory']))

def parse_access_log(log_directory):
    pattern = r'(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+) (\S+)" (\d+) (\d+)'

    for file_name in os.listdir(log_directory):
        if file_name.endswith('.log'):
            file_path = os.path.join(log_directory, file_name)
            try:
                with open(file_path, 'r') as file:
                    for line in file:
                        match = re.match(pattern, line)
                        if match:
                            ip = match.group(1)
                            date = match.group(4)
                            method = match.group(5)
                            url = match.group(6)
                            http_version = match.group(7)
                            status_code = int(match.group(8))
                            bytes_sent = int(match.group(9))

                            date = datetime.strptime(date, "%d/%b/%Y:%H:%M:%S %z")

                            entry = LogEntry(
                                ip=ip,
                                date=date,
                                method=method,
                                resource=url,
                                protocol=http_version,
                                status=status_code,
                                size=bytes_sent,
                            )

                            add_entry_to_database(entry)
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

if __name__ == '__main__':
    with app.app_context():
        database.create_all()
        parse_access_log(log_directory)