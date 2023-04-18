import pytest

def test_main():
        with pytest.raises(SystemExit):
            from . import main
        assert True