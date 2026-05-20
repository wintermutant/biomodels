from sqlmodel import Session, select
from biomodels.app import create_db_and_tables, get_engine
from biomodels.models import DBTestRun
import biomodels


def test_test_run():
    create_db_and_tables()
    engine = get_engine()
    content = f"test according to v{biomodels.__version__}"
    with Session(engine) as session:
        run = DBTestRun(test_content=content)
        session.add(run)
        session.commit()
        session.refresh(run)

        assert run.id is not None
        assert run.test_time is not None
        assert run.test_content == content
