import pytest, pygame, configparser, shutil
from .models import __init__,button,card,player
from .utils import sound, menu, settings, storyMode
from . import pause
from .single_play import Game


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
    yield sound.SoundFX()

    

def test_sound():
    sound.playMusic(1)
    sound.pauseMusic()
    sound.unpauseMusic()
    sound.musicDown()
    sound.musicUp()
    sound.getMusicVol()
    sound.resetMusicVol()

    config = configparser.ConfigParser()
    config.read("setting_data.ini")
    soundFX = sound.SoundFX()
    soundFX.soundIni(config)
    soundFX.soundPlay(1)
    soundFX.soundDown()
    soundFX.soundUp()
    soundFX.getSoundVol()
    soundFX.resetSoundVol()

    assert True

def test_models(screen):
    pygame.font.init()

    testBut = button.Button(0,0,0,0,(0,0,0),"","red",0,0)
    testBut.draw(screen)
    testBut.is_clicked(pygame.mouse.get_pos())

    testCard = card.Card('red',0,'reverse',True)
    testPlayer = player.Player(0,[testCard],True)
    testPlayer.update_hand(screen)
    testPlayer.hand[1:15] = [testCard] * 15
    testPlayer.update_hand(screen)
    testPlayer.hand[1:15] = [testCard] * 25
    testPlayer.update_hand(screen)

    testCom = button.Component(0,0,0,0,(0,0,0),"",'red',0,testPlayer)
    testCom.draw(screen)

    assert True

def test_Setting(config, keyList, screen):
    soundFX = sound.SoundFX()
    soundFX.soundIni(config)
    pygame.font.init()
    font = pygame.font.Font(None, 48)
    testSet = settings.Setting(keyList, font, screen, soundFX, config)

    testSet.draw()
    testSet.visible[0] = True
    testSet.visible[1] = 5
    testSet.option = 2
    testSet.draw()
    testSet.option = 4
    testSet.draw()

    pygame.event.clear()
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=testSet.keys["UP"]))
    testSet.configKeys(3)

    testSet.reset()

    testSet.option = 0
    testSet.selected = 0

    down = pygame.event.Event(pygame.KEYDOWN, key=testSet.keys["DOWN"])
    up = pygame.event.Event(pygame.KEYDOWN, key=testSet.keys["UP"])
    left = pygame.event.Event(pygame.KEYDOWN, key=testSet.keys["LEFT"])
    right = pygame.event.Event(pygame.KEYDOWN, key=testSet.keys["RIGHT"])
    enter = pygame.event.Event(pygame.KEYDOWN, key=testSet.keys["RETURN"])

    savePos = pygame.event.Event(pygame.MOUSEMOTION, pos=(screen.get_width() // 5+5, screen.get_height() * 10 // 12+5), rel=(0, 1), buttons=(0, 0, 0))
    blockPos = pygame.event.Event(pygame.MOUSEMOTION, pos=(screen.get_width() // 5+5,screen.get_height() // 4 + 80+5), rel=(0, 1), buttons=(0, 0, 0))
    clickU = pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=(screen.get_width() // 5+5, screen.get_height() * 10 // 12+5), touch = False)

    pygame.event.clear()
    #test 'Window Size'
    pygame.event.post(up)
    pygame.event.post(down)
    pygame.event.post(enter)
    #choose 1 > 2 > 3 > 1 option and Save
    pygame.event.post(blockPos)
    pygame.event.post(savePos)
    pygame.event.post(down)
    pygame.event.post(enter)
    pygame.event.post(down)
    pygame.event.post(enter)
    pygame.event.post(down)
    pygame.event.post(enter)
    pygame.event.post(down)
    pygame.event.post(down)
    pygame.event.post(enter)
    pygame.event.post(up)
    pygame.event.post(enter)

    #test 'key config'
    pygame.event.post(down)
    pygame.event.post(down)
    pygame.event.post(enter)
    pygame.event.post(blockPos)
    pygame.event.post(savePos)
    pygame.event.post(enter)

    #test 'sound setting'
    pygame.event.post(up)
    pygame.event.post(up)
    pygame.event.post(enter)
    #pygame.event.post(pygame.event.Event(1024, pos=(screen.get_width() // 4+8, 247), rel=(0,1), buttons=(0,0,0)))
    #pygame.event.post(pygame.event.Event(1025, pos=(screen.get_width() // 4+8, 247), button=1, touch=False, window=None))
    #pygame.event.post(pygame.event.Event(1026, pos=(screen.get_width() // 4+8, 247), button=1, touch=False, window=None))
    pygame.event.post(blockPos)
    pygame.event.post(savePos)
    pygame.event.post(up)
    pygame.event.post(enter)
    pygame.event.post(right)
    pygame.event.post(enter)
    pygame.event.post(up)
    pygame.event.post(enter)
    pygame.event.post(left)
    pygame.event.post(enter)
    pygame.event.post(up)
    pygame.event.post(enter)
    pygame.event.post(up)
    pygame.event.post(enter)

    #test reset
    pygame.event.post(up)
    pygame.event.post(enter)
    pygame.event.post(down)
    pygame.event.post(enter)

    testSet.run()
    

    with pytest.raises(SystemExit):
        pygame.event.post(pygame.event.Event(pygame.QUIT)) 
        testSet.run()

    assert True
'''
def test_storyMode(screen, font, config, keyList):
    pygame.init()
    testStory = storyMode.StoryMode(screen, font, config, keyList)

    pygame.event.clear()
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))

    mouse = pygame.event.Event(pygame.MOUSEBUTTONUP, pos=(screen.get_width() // 2 - 50 // screen.get_height() * 3 // 4), rel=(0, 0), buttons=(0, 0, 0))
    pygame.event.post(mouse)
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))

    testStory.run()

    assert True
'''
def test_menu(keyList, screen):
    from .utils import __init__

    pygame.font.init()
    font = pygame.font.Font(None, 48)

    testMenu = menu.Menu(keyList, font, screen)

    testMenu.visible[0] = True
    testMenu.draw()
    testMenu.visible[1] = 7
    testMenu.draw()

    down = pygame.event.Event(pygame.KEYDOWN, key=testMenu.keys["DOWN"])
    up = pygame.event.Event(pygame.KEYDOWN, key=testMenu.keys["UP"])
    left = pygame.event.Event(pygame.KEYDOWN, key=testMenu.keys["LEFT"])
    right = pygame.event.Event(pygame.KEYDOWN, key=testMenu.keys["RIGHT"])
    enter = pygame.event.Event(pygame.KEYDOWN, key=testMenu.keys["RETURN"])

    startGamePos = pygame.event.Event(pygame.MOUSEMOTION, pos = (screen.get_width() // 2, screen.get_height() // 2 + 50))

    pygame.event.clear()
    pygame.event.post(startGamePos)
    pygame.event.post(down)
    pygame.event.post(right)
    pygame.event.post(left)
    pygame.event.post(up)
    pygame.event.post(enter)

    testMenu.run()

    pygame.quit()
    assert True

def test_pause(screen, font, config, keyList, soundFX):
    pygame.init()
    testPause = pause.Pause(screen, font, config, keyList, soundFX)

    down = pygame.event.Event(pygame.KEYDOWN, key=testPause.keys["DOWN"])
    up = pygame.event.Event(pygame.KEYDOWN, key=testPause.keys["UP"])
    enter = pygame.event.Event(pygame.KEYDOWN, key=testPause.keys["RETURN"])

    mouse = pygame.event.Event(pygame.MOUSEMOTION, pos = (screen.get_width() // 2, screen.get_height() // 2 + 50))
    click = pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=(screen.get_width() // 2, screen.get_height() // 2 + 50), touch = False)

    testPause.draw()

    pygame.event.clear()
    pygame.event.post(mouse)
    pygame.event.post(down)
    pygame.event.post(up)
    pygame.event.post(enter)

    testPause.run()
    pygame.quit()

def test_main(keyList, screen):
    pygame.event.clear()
    mouse = pygame.event.Event(pygame.MOUSEBUTTONUP, pos=(screen.get_width() // 2 - 50 // screen.get_height() * 3 // 4), rel=(0, 0), buttons=(0, 0, 0))
    pygame.event.post(mouse)
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key = keyList["UP"]))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key = keyList["DOWN"]))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key = keyList["LEFT"]))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key = keyList["RETURN"]))

    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key = pygame.K_ESCAPE))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key = keyList["ESCAPE"]))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key = keyList["UP"]))
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key = keyList["RETURN"]))

    with pytest.raises(SystemExit):
        from . import main
        assert True

    assert True

'''
def test_singlePlay(keyList):
    pygame.init()
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key = keyList["RETURN"]))

    pygame.event.clear()
    with pytest.raises(SystemExit):
        from . import main
        assert True

    #with pytest.raises(SystemExit):
    #    game.start_single_play()   
    assert True'''