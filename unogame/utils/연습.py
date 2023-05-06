# import pygame
# import pickle
# import socket

# # Create a Pygame surface object
# surface = pygame.Surface((100, 100))
# surface.fill((255, 0, 0))

# # Create a list of integers
# int_list = ['1, 2, 3, 4, 5', '가나다라', 'hi']

# # Pack the surface and integer list into a tuple
# data = (int_list)

# # Serialize the data using pickle
# serialized_data = pickle.dumps(data)

# # Create a socket object and connect to the server
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, 10) 
# client_socket.connect(('203.246.85.194', 11002))

# # Send the serialized data over the socket
# client_socket.sendall(serialized_data)
# print('sended')

# # Close the socket
# client_socket.close()
import pygame
import datetime

pygame.init()

screen = pygame.display.set_mode((640, 480))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                current_date = datetime.date.today()
                print(current_date)

    screen.fill((255, 255, 255))
    pygame.display.flip()

