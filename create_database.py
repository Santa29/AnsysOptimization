from models.database import create_db, Session
from models.langeron import LangeronModel
from models.shell import ShellModel


def create_database(load_fake_data: bool = True):
    create_db()
    if load_fake_data:
        _load_fake_data(Session())


def _load_fake_data(session: Session):
    pass
