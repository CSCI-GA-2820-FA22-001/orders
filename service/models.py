"""
Models for YourResourceModel

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy
import json
logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass


class Order(db.Model):
    """
    Class that represents a Order Model
    id: int
    items: list[int]
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.String(63), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    items = db.Column(db.Text)

    def __repr__(self):
        return "<User {self.user_id} Order id=[{self.id}]>"

    def create(self):
        """
        Creates a YourResourceModel to the database
        """
        logger.info("Creating %s", self.id)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a YourResourceModel to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ Removes a YourResourceModel from the data store """
        logger.info("Deleting %s", self.id)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a YourResourceModel into a dictionary """
        return {"id": self.id, "name": self.items}

    def deserialize(self, data):
        """
        Deserializes a YourResourceModel from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.items = data["item"]
            self.user_id = data["user_id"]
            self.create_time = data["create_time"]
            self.status = data["status"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid YourResourceModel: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid YourResourceModel: body of request contained bad or no data - "
                "Error message: " + error
            ) from error
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the YourResourceModels in the database """
        logger.info("Processing all YourResourceModels")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a YourResourceModel by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all YourResourceModels with the given name

        Args:
            name (string): the name of the YourResourceModels you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

class Items(db.Model):
        """
        Class that represents a Item-Order matching Model
        id: int
        oder_id:int
        item_id:int
        """

        app = None

        # Table Schema
        id = db.Column(db.Integer, primary_key=True)
        order_id = db.Column(db.Integer, nullable=False)
        item_id = db.Column(db.Integer, nullable=False)

        def __repr__(self):
            return "<Order id=[{self.order_id}] Item id=[{self.item_id}]>"

        def create(self):
            """
            Creates a YourResourceModel to the database
            """
            logger.info("Creating %s", self.id)
            self.id = None  # id must be none to generate next primary key
            db.session.add(self)
            db.session.commit()

        def update(self):
            """
            Updates a YourResourceModel to the database
            """
            logger.info("Saving %s", self.name)
            db.session.commit()

        def delete(self):
            """ Removes a YourResourceModel from the data store """
            logger.info("Deleting %s", self.id)
            db.session.delete(self)
            db.session.commit()

        def serialize(self):
            """ Serializes a YourResourceModel into a dictionary """
            return {"id": self.id, "order_id": self.order_id, "item_id": self.item_id}

        def deserialize(self, data):
            """
            Deserializes a YourResourceModel from a dictionary

            Args:
                data (dict): A dictionary containing the resource data
            """
            try:
                self.items = data["item"]
                self.user_id = data["user_id"]
                self.create_time = data["create_time"]
                self.status = data["status"]
            except KeyError as error:
                raise DataValidationError(
                    "Invalid YourResourceModel: missing " + error.args[0]
                ) from error
            except TypeError as error:
                raise DataValidationError(
                    "Invalid YourResourceModel: body of request contained bad or no data - "
                    "Error message: " + error
                ) from error
            return self

        @classmethod
        def init_db(cls, app):
            """ Initializes the database session """
            logger.info("Initializing database")
            cls.app = app
            # This is where we initialize SQLAlchemy from the Flask app
            db.init_app(app)
            app.app_context().push()
            db.create_all()  # make our sqlalchemy tables

        @classmethod
        def all(cls):
            """ Returns all of the YourResourceModels in the database """
            logger.info("Processing all YourResourceModels")
            return cls.query.all()

        @classmethod
        def find(cls, by_id):
            """ Finds a YourResourceModel by it's ID """
            logger.info("Processing lookup for id %s ...", by_id)
            return cls.query.get(by_id)

        @classmethod
        def find_by_name(cls, name):
            """Returns all YourResourceModels with the given name

            Args:
                name (string): the name of the YourResourceModels you want to match
            """
            logger.info("Processing name query for %s ...", name)
            return cls.query.filter(cls.name == name)