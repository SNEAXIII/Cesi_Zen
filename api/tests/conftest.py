import pytest
from datetime import datetime


@pytest.fixture(scope="function")
def use_time_machine(time_machine):
    time_machine.move_to(datetime.now(), tick=False)
    yield time_machine
