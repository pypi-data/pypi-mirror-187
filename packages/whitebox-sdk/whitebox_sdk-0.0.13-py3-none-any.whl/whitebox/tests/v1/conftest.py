import databases
import sqlalchemy
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy.orm import sessionmaker

from whitebox.core.settings import get_settings
from whitebox.entities.Base import Base
from whitebox.main import app
from whitebox.sdk.whitebox import Whitebox
from whitebox.tests.utils.maps import v1_test_order_map
from secrets import token_hex

settings = get_settings()


def get_order_number(task):
    return v1_test_order_map.index(task)


@fixture(scope="session")
def client():
    with TestClient(app) as client:
        yield client


@fixture(scope="session", autouse=True)
async def db():
    # runs once before all tests
    engine = sqlalchemy.create_engine(settings.DATABASE_URL)
    database = databases.Database(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)
    await database.connect()
    db = SessionLocal()
    yield db
    # runs once after all tests
    await database.disconnect()
    # await database.execute(query="DROP DATABASE test WITH (FORCE);")
    Base.metadata.drop_all(engine)


class TestsState:
    user: dict = {}
    api_key: str = token_hex(32)
    model_binary: dict = {}
    model_multi: dict = {}
    model_multi_2: dict = {}
    model_multi_3: dict = {}
    inference_row_multi: dict = {}
    inference_row_binary: dict = {}


state = TestsState()


class TestsSDKState:
    wb: Whitebox


state_sdk = TestsSDKState()
