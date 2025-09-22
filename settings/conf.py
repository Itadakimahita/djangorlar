# Project modules
from decouple import config

# -----------------------------------
# Env id
# -----------------------------------
ENV_POSSIBLE_OPTIONS = (
    'local',
    'prod',
)
ENV_ID = config("DJANGORLAR_ENV_ID", cast=str)
SECRET_KEY = 'django-insecure--*edk!1d6+x&#re&df%js^x07a8@vns@d45nsoe%m&i1d)w03-'
