from flask_security import Security, SQLAlchemyUserDatastore
from src.user import models

user_data_store = SQLAlchemyUserDatastore(models.db, models.User, models.Role)

security = Security(datastore=user_data_store)
