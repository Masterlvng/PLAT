import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FORMS_DIR = os.path.join(BASE_DIR,'app','static','forms')
APPLICANT_DIR = os.path.join(BASE_DIR,'app','static','applicant')
POSTER_DIR = os.path.join(BASE_DIR,'app','static','img','posters')

SQLALCHEMY_DATABASE_URI = 'mysql://root:masterlvng@localhost/plat'

CSRF_ENABLED = True
SECRET_KEY = 'Ucando1tbettermore'
