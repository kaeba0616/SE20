import pytest, configparser, shutil, pygame
from . import single_play
from .utils import sound
'''
@pytest.fixture
def config(tmp_path):
    source = "setting_data.ini"
    shutil.copy(source, tmp_path/'temp.ini')

    config = configparser.ConfigParser()
    config.read(tmp_path/'temp.ini')
    yield config
@pytest.fixture(scope="function")
def screen():
    yield pygame.display.set_mode((800, 600))
@pytest.fixture(scope="session")
def font():
    pygame.font.init()
    font = pygame.font.Font(None, 48)
    yield font
@pytest.fixture
def keyList(config):
    key_list = {
    "LEFT": int(config["key"]["left"]),
    "RIGHT": int(config["key"]["right"]),
    "UP": int(config["key"]["up"]),
    "DOWN": int(config["key"]["down"]),
    "RETURN": int(config["key"]["return"]),
    "ESCAPE": int(config["key"]["escape"]),
    }
    yield key_list
@pytest.fixture
def soundFX():
    yield sound.SoundFX()'''

def test_single():
    pygame.init()
    config = configparser.ConfigParser()
    config.read("setting_data.ini")
    screen = pygame.display.set_mode((800, 600))
    key_list = {
    "LEFT": int(config["key"]["left"]),
    "RIGHT": int(config["key"]["right"]),
    "UP": int(config["key"]["up"]),
    "DOWN": int(config["key"]["down"]),
    "RETURN": int(config["key"]["return"]),
    "ESCAPE": int(config["key"]["escape"]),
    }
    soundFX = sound.SoundFX()

    try:
        pass
        # game = single_play.Game(screen, 2, key_list, config, soundFX)
        # game.start_single_play()
    finally:
        pygame.quit()
    assert True


