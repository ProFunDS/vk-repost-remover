# pip3 install vk-api

from time import sleep

from vk_api import VkApi

from config import login, password, token # access_token


def two_factor():
    code = input('Код аутентификации: ')
    return code, True # True - сохранить сессию в локальном файле.

def enter():
    vk_session = VkApi(login, password, token=token, auth_handler=two_factor)
    vk_session.auth()
    vk = vk_session.get_api()
    return vk

def delete_reposts(vk, walls):
    length = len(walls)
    counter = 1
    for wall in walls:
        if 'copy_history' not in wall: # это не репост
            length -= 1
            continue
            
        result = vk.wall.delete(post_id=wall['id'])
        if result == 1:
            print(f'Пост {counter}/{length}')
        else:
            print(f'На посте №{wall["id"]} от {wall["created_by"]} произошла ошибка')
            
        sleep(0.15)
        counter += 1

if __name__ == '__main__':
    vk = enter()
    for i in range(1, 11): # первая тысяча постов
        print(f'[!]    Партия постов №{i}    [!]')
        walls = vk.wall.get(count=100, filter='owner')['items']
        delete_reposts(vk, walls)
        sleep(3)
