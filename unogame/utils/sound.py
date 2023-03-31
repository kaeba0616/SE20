import pygame
import os

def playMusic(num): #배경음악 재생
    pygame.mixer.init() #mixer 초기화
    path = os.getcwd() #원래 작업 디렉토리 임시 저장
    module_path = os.path.abspath(os.path.dirname(__file__))
    os.chdir(module_path+"/../resources/music") #파일 경로 탐색 용이하게 한번 바꾸기

    pygame.mixer.music.stop()
    pygame.mixer.music.load("music"+str(num)+".mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1) #반복재생

def pauseMusic(): #배경음악 일시정지
    pygame.mixer.music.pause()
def unpauseMusic(): #배경음악 다시 재생
    pygame.mixer.music.unpause()

def musicDown():
    currentVol = pygame.mixer.music.get_volume()
    pygame.mixer.music.set_volume(currentVol-0.1)
    if currentVol <= 0.1: pygame.mixer.music.set_volume(0)
def musicUp():
    currentVol = pygame.mixer.music.get_volume()
    pygame.mixer.music.set_volume(currentVol+0.1)



class Sounds:
    def __init__(self) :
        pygame.mixer.init() #mixer 초기화
        path = os.getcwd() #원래 작업 디렉토리 임시 저장
        module_path = os.path.abspath(os.path.dirname(__file__)) 
        os.chdir(module_path+"/../resources/sounds") #파일 경로 탐색 용이하게 한번 바꾸기

        self.soundEffects = [
            pygame.mixer.Sound("bleep.mp3"),
            pygame.mixer.Sound("coin.mp3"),
            pygame.mixer.Sound("short_blip.mp3")
        ]

        os.chdir(path) # 경로 원위치

        for sound in self.soundEffects:
            sound.set_volume(0.1) #초기값은 0.5
    
    def soundPlay(self, num):
        self.soundEffects[num-1].play()
    
    def soundDown(self):
        currentVol = self.soundEffects[0].get_volume()
        set = currentVol - 0.1
        if currentVol <= 0.1: set = 0
        for sound in self.soundEffects:
            sound.set_volume(set)
        print(self.soundEffects[0].get_volume())
    def soundUp(self):
        currentVol = self.soundEffects[0].get_volume()
        for sound in self.soundEffects:
            sound.set_volume(currentVol + 0.1)
        print(self.soundEffects[0].get_volume())
