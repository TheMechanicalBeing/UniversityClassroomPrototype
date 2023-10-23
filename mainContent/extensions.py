from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

tagnames = {
  0: {
    "Home": "/",
    "Login": "/auth/login"
  },
  1: {
    "Home": "/",
    "Add": "/add",
    "Log Out": "/auth/logout"
  },
  2: {
    "Home": "/",
    "Log Out": "/auth/logout"
  },
  3: {
    "Home": "/",
    "Log Out": "/auth/logout"
  }
}
