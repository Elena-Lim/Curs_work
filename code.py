# Курсовая работа "Резервное копирование"
'''
Программа производит резервное копирование фотографий из профиля Вконтакте с наилучшим качеством на Яндекс диск

Входные данные:
user_id_token.txt   - токен Vk, token Yandex, Id Vk
amount_photo = 5    - количество фотографий для резервного копирования
folder_name_ya      - имя создаваемой папки на Яндекс диске

Выходные данные:
data.json - файл для вывода списка файлов в формате json
Папка на Яндекс диске с сохраненными фотографиями
'''

'''Модули'''
import requests
import json
from tqdm import tqdm

class VK:
    def __init__(self, access_token, user_id, amount_photo, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version
        }
        self.amount_photo = amount_photo

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

access_token = ''  # токен полученный из инструкции
user_id = ''  # идентификатор пользователя vk
vk = VK(access_token, user_id)
print(vk.users_info())


    def get_data_user_vk(self):
        data_url = self.url + 'photos.get'
        data_params = {
            'owner_id': self.params['user_ids'],
            'album_id': 'profile',
            'extended': '1',
            'v': '5.131'
        }

        res = requests.get(data_url, params={**self.params, **data_params}).json()
        return res ['response']['items']

    def selection_quality_photo(self, sizes_photo):
        # Метод класса VkUser предназначен для выбора наилучшего качества фотографий пользователя.
        # В методе selection_quality_photo() определяются параметры качества фотографий.
        quality_photo = 0
        for size in sizes_photo:
            if size['height'] * size['width'] >= quality_photo:
                quality_photo = size['height'] * size['width']
                type_photo = size['type']
                url_photo = size['url']
        return type_photo, url_photo

    def data_filtering(self):
        # Метод data_filtering() выбирает из профиля пользователя VK заданное количество фотографий
        # с наилучшим качеством и добавляет их параметры в список.
        data_user = self.get_data_user_vk()
        # Выбираем заданное amount_photo количество фотографий
        data_user = data_user[:amount_photo]

        list_photo = []
        for item in data_user:
            likes_photo = item['likes']['count']
            # Выбираем фотографию с максимальным качеством
            type_photo, url_photo = self.selection_quality_photo(item['sizes'])
            list_photo.append({'likes': likes_photo, 'type': type_photo, 'url': url_photo})
        return list_photo

    def get_list_files(list_photo):
        output_list_files = []
        list_files = []
        files = []

        for photo in list_photo:
            index = 0
            # Формируем имя файла
            file_name = str(photo['likes']) + '.jpg'
            # Если имя файла существует добавляем к имени _индекс
            while file_name in files:
                index += 1
                file_name = str(photo['likes']) + '_' + str(index) + '.txt'
            files.append(file_name)
            output_list_files.append({'file_name': file_name, 'size': photo['type']})
            list_files.append({'file_name': file_name, 'url': photo['url']})
        return output_list_files, list_files

    class YaUploader:
        # Он содержит только конструктор, который принимает один параметр - токен доступа к API Яндекса.
        # В конструкторе создается переменная token, которая будет содержать этот токен.'''

        def __init__(self, token):
            self.token = token

        def get_headers(self):
            return {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': 'OAuth {}'.format(self.token)
            }

        def _get_upload_link(self, disk_file_path):
            # Данный код представляет функцию _get_upload_link() класса YaUploader.
            # Она принимает путь к файлу на диске, который нужно загрузить на Яндекс Диск, и возвращает ссылку на загрузку файла.
            upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
            headers = self.get_headers()
            params = {'path': disk_file_path, 'overwrite': 'true'}
            response = requests.get(upload_url, headers=headers, params=params)
            return response.json()

        def create_folder_ya(self, folder_name):
            # Данный код представляет метод create_folder_ya() класса YaUploader, который создает папку на Яндекс Диске.
            # Прежде всего, создается URL для создания папки на Яндекс Диске, используя URL upload_url и параметр path, который передает имя папки. Затем формируются заголовки запроса с помощью метода get_headers().
            # Параметр overwrite имеет значение false, что означает, что при создании папки будет создана новая папка, если она уже существует.
            # Отправляется запрос на создание папки с помощью метода put(). Параметр f'{upload_url}?path={folder_name}' указывает на URL для создания папки и передает параметр path с именем папки.
            # Если ответ от сервера успешный (код состояния 201), то выводится сообщение о том, что папка успешно создана на Яндекс Диске с помощью метода print().
            # Если же ответ от сервера неудачный, то выводится соответствующее сообщение об ошибке.'''
            upload_url = 'https://cloud-api.yandex.net:443/v1/disk/resources'
            headers = self.get_headers()
            params = {'overwrite': 'false'}
            response = requests.put(f'{upload_url}?path={folder_name}', headers=headers, params=params)
            if response.status_code == 201:
                # Логирование процесса записи на яндекс диск
                print(f'Папка {folder_name} успешно создана на Яндекс диске')

        def upload(self, list_files, folder_ya):
            # Данный код является методом upload() класса YaUploader и предназначен для загрузки файлов с сервера на Яндекс Диск.
            # Сначала создается папка на Яндекс Диске и выводится сообщение о ее создании на экран.
            # Затем в цикле for по каждому файлу из списка list_files вызывается метод _get_upload_link(), который возвращает ссылку на загрузку файла на Яндекс Диск.
            # Ссылка сохраняется в переменной response_href, затем вызывается метод put() для загрузки файла на диск.
            # После того, как все файлы были загружены, выводится сообщение об успешном сохранении файлов на Яндекс Диск.
            # создаем папку на яндекс диске
            self.create_folder_ya(folder_name=folder_ya)
            print(f'Cохраняем файлы {len(list_files)} шт. в папку {folder_ya} на Яндекс диск')
            for file in tqdm(list_files, colour='green'):
                file_name = file['file_name']
                disk_file_path = folder_ya + '/' + file_name  # Если папка существует на яндекс диске
                response_href = self._get_upload_link(disk_file_path=disk_file_path)
                href = response_href.get('href', '')
                data = requests.get(file['url'])
                response = requests.put(href, data=data.content)
            print('Файлы успешно сохранены на Яндекс диск')

    if __name__ == '__main__':
        # Данный фрагмент написан на языке Python и представляет собой пример кода для загрузки фотографий из ВКонтакте на Яндекс.Диск с использованием API.
        # Происходит чтение токенов доступа к ВКонтакте и Яндекс.Диску, а также идентификаторов пользователей из файла "user_id_token.txt".
        # Затем запрашивается количество фотографий, которое необходимо загрузить на Яндекс.Диск, и задается имя папки на Яндекс.Диске.
        # Далее создается экземпляр класса VkUser с параметрами, полученными из файла "user_id_token.txt", и с помощью этого класса происходит получение списка фотографий наилучшего качества из ВКонтакте.
        # После этого происходит формирование списков output_list_files и list_files на основе полученных фотографий.
        # Наконец, происходит запись списка output_list_files в файл в формате JSON с помощью open() и json.dump(), а затем сохранение списка на Яндекс.Диск с помощью YaUploader().'''
        # Получаем токен Vk, токен на Яндекс диске, user id Vk
        with open('user_id_token.txt', 'r') as file_object:
            token_vk = file_object.readline().strip()
            token_ya = file_object.readline().strip()
            user_ids = file_object.readline().strip()

        # Запрашиваем количество сохраняемых фотографий
        amount_photo = int(input('Введите количество сохраняемых фотографий на Яндекс диск: '))
        # Задаем имя папки  на Яндекс диске
        folder_name_ya = 'my_photo_vk'
        # Задаем версию Vk
        version = '5.131'

        # Создаем экземпляр класса VkUser()
        vk_client = VkUser(token=token_vk, user_ids=user_ids, amount_photo=amount_photo, version=version)
        # Получаем список заданного amount_photo количества фотографий наилучшего качества
        list_photo = vk_client.data_filtering()
        # Формируем списки
        output_list_files, list_files = get_list_files(list_photo)
        # Выводим требуемый список output_list_files в json файл  data.json
        with open('data.json', 'w', encoding='utf-8') as file_obj:
            json.dump(output_list_files, file_obj, indent=4, ensure_ascii=False)
            print('Список файлов с указанием размера сохранен в формате json в файл data.json')

        # Создаем экземпляр класса YaUploader()
        uploader = YaUploader(token_ya)
        # Сохраняем фотографии на Яндекс диск
        uploader.upload(list_files, folder_name_ya)


