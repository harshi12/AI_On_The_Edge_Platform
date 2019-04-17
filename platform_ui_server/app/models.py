from app import db

class Person(db.Model):
    person_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    person_type = db.Column(db.Integer , nullable=False)

    def __repr__(self):
        return "Person('{self.person_id}')"


class Application(db.Model):
    app_id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(100), unique=True, nullable=False)
    AD_id = db.Column(db.Integer, db.ForeignKey(Person.person_id), nullable=False)
    #app_logic_loc = db.Column(db.String(100), unique=False, nullable=True)
    #app_config_loc = db.Column(db.String(150), unique=False, nullable=True)
    #model_loc = db.Column(db.String(100), unique=False, nullable=True)
    app_ui_server = db.Column(db.String(100), unique=False, nullable=True)

    def __repr__(self):
        return "Application('{self.app_id}', '{self.app_name}', '{self.app_ui_server}')"

class Service(db.Model):
    service_id = db.Column(db.Integer , primary_key=True)
    service_name = db.Column(db.String(150),nullable=False)
    service_type = db.Column(db.String(10))
    app_id = db.Column(db.Integer, db.ForeignKey(Application.app_id), nullable=False)
    deploy_config_loc = db.Column(db.String(150), unique=False, nullable=True)
    prod_config_loc = db.Column(db.String(150), unique=False, nullable=True)

    def __repr__(self):
        return "Services('{self.service_id}','{self.service_name}')"

class User(db.Model):
    subscription_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Person.person_id), nullable=False)
    subscribed_app = db.Column(db.Integer , db.ForeignKey(Application.app_id) , nullable=False)


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
