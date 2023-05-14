import pytest
from dotenv import load_dotenv
from utils.helper import BaseSession
import os


load_dotenv()


class Globals:
    REQRES_URL = os.getenv('REQRES_URL')
    REQRES_API = os.getenv('REQRES_API')
    TRICENTIS_URL = os.getenv('TRICENTIS_URL')
    WEB_SHOP_API_URL = os.getenv('WEB_SHOP_API_URL')


@pytest.fixture(scope="session")
def reqres_base():
    with BaseSession(base_url=Globals.REQRES_API) as session:
        yield session
