from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Pa$$w0rd@localhost/python_kt'
database = SQLAlchemy(app)

with app.app_context():
    engine = database.engine
    Base = database.Model.metadata

    class LogEntry(database.Model):
        __tablename__ = 'log_entries'
        id = database.Column(database.Integer, primary_key=True)
        ip = database.Column(database.String(15), nullable=False)
        date = database.Column(database.DateTime, nullable=False)
        method = database.Column(database.String(50), nullable=False)
        resource = database.Column(database.String(2048), nullable=False)
        protocol = database.Column(database.String(10), nullable=False)
        status = database.Column(database.Integer, nullable=False)
        size = database.Column(database.Integer, nullable=False)

        def to_dict(self):
            return {
                'id': self.id,
                'ip': self.ip,
                'date': self.date,
                'method': self.method,
                'resource': self.resource,
                'protocol': self.protocol,
                'status': self.status,
                'size': self.size
            }

    database.create_all()
def add_entry_to_database(entry):
    database.session.add(entry)
    database.session.commit()
def get_all_entries():
    return LogEntry.query.all()

def get_entries_by_ip(ip):
    return LogEntry.query.filter_by(ip=ip).all()

def get_entries_by_date_range(start_date, end_date):
    return LogEntry.query.filter(LogEntry.date.between(start_date, end_date)).all()

def get_grouped_by_ip():
    result = database.session.query(LogEntry.ip, database.func.count(LogEntry.ip)).group_by(LogEntry.ip).all()
    grouped_entries = [{'ip': entry[0], 'count': entry[1]} for entry in result]
    return grouped_entries

def get_grouped_by_date():
    return database.session.query(database.func.date(LogEntry.date), database.func.count(database.func.date(LogEntry.date))).group_by(database.func.date(LogEntry.date)).all()

if __name__ == '__main__':
    with app.app_context():
        database.create_all()



