class Player:
    # number : 플레이어 넘버 / type : 어떤 플레이어 종류인지 / hand : 플레이어의 패 / turn : 플레이어 객체의 턴
    def __init__(self, number, hand, turn):
        self.number = number
        self.hand = hand
        self.turn = turn
