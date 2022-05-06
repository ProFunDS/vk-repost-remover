# pip3 install vk-api

from time import sleep

from vk_api import VkApi
from vk_api.vk_api import VkApiMethod

from config import login, password, token  # access_token с правами доступа: wall.


def two_factor() -> tuple[str, bool]:
    code = input('Код аутентификации: ')
    return code, True  # True - сохранить сессию в локальном файле.

def enter() -> VkApiMethod:
    vk_session = VkApi(login, password, token=token, auth_handler=two_factor)
    vk_session.auth()
    return vk_session.get_api()

def delete_reposts(vk: VkApiMethod, walls: dict) -> None:
    length = len(walls)
    counter = 1
    for wall in walls:
        if 'copy_history' not in wall:  # это не репост
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
    COUNT = 100  # постов (макс. для одного запроса)
    walls = vk.wall.get(count=COUNT, filter='owner')['items']
    delete_reposts(vk, walls)
