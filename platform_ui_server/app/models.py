from app import db

class Person(db.Model):
    person_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    person_type = db.Column(db.Integer , nullable=False)

    def __repr__(self):
        return "Person('{self.person_id}')"


class Application(db.Model):
    app_id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(100), unique=True, nullable=False)
    # app_desc = db.Column(db.String(2000), nullable=False)
    AD_id = db.Column(db.Integer, db.ForeignKey(Person.person_id), nullable=False)
    app_logic_loc = db.Column(db.String(100), unique=False, nullable=True)
    config_file_loc = db.Column(db.String(100), unique=False, nullable=True)
    model_loc = db.Column(db.String(100), unique=False, nullable=True)
    app_ui_server = db.Column(db.String(100), unique=False, nullable=True)

    def __repr__(self):
        return "Application('{self.app_id}', '{self.app_logic_loc}', '{self.config_file_loc}' , '{self.config_file_loc}' , '{self.app_ui_server}')"


class User(db.Model):
    subscription_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Person.person_id), nullable=False)
    subscribed_model = db.Column(db.Integer , db.ForeignKey(Application.app_id) , nullable=False)


class Gateway(db.Model):
    gw_id = db.Column(db.Integer, primary_key=True)
    gw_name = db.Column(db.String(50), unique=True ,nullable=False)
    gw_location = db.Column(db.String(50), nullable=False)
    gw_IP = db.Column(db.String(50), nullable=False)
    gw_port = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "Gateway('{self.gw_id}')"


class Sensor(db.Model):
    sensor_id = db.Column(db.Integer, primary_key=True)
    sensor_type = db.Column(db.String(20), nullable=False)
    connected_gw_id = db.Column(db.Integer, db.ForeignKey(Gateway.gw_id), nullable=False)

    def __repr__(self):
        return "Sensor('{self.sensor_id}')"

db.create_all()
