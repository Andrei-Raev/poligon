import os
import shutil
from json import load
import re
from random import choice
from string import ascii_letters

os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def find_path_to_quest(name: str) -> str:
    with open('quests/data.json', 'r') as json_file:
        name_list = load(json_file)
    try:
        return name_list[name]
    except KeyError:
        return


def parse(path, temp_prefix):
    with open(path, 'r', encoding='utf-8') as file_to_read:
        text = file_to_read.read()
    head = re.search(r'{[\s\S][^}]*}', re.search(r'ЗАГОЛОВОК.*{[\s\S][^}]*}', text)[0])[0][1:-1].strip()
    body = re.search(r'{[\s\S][^}]*}', re.search(r'ТЕЛО.*{[\s\S][^}]*}', text)[0])[0][1:-1].strip()
    action = re.search(r'{[\s\S][^}]*}', re.search(r'ДЕЙСТВИЯ.*{[\s\S][^}]*}', text)[0])[0][1:-1].strip()

    res_head, res_body, res_action = None, '', []

    for string in head.split('\n'):
        if string:
            res_head = string
        else:
            res_head = ''

    for string in body.split('\n'):
        if string.strip().startswith('ИЗОБРАЖЕНИЕ'):
            tmp = string.split()
            res_body += f'<div class="blurred_edges_img" style="margin: 15px 0; background-image: url(\'../static/temp/{temp_prefix}/{tmp[1]}\')" width="100%" alt="{tmp[1]}"><img width="100%" style="opacity: inherit" src="../static/temp/{temp_prefix}/{tmp[1]}"></div><br>'
        else:
            res_body += string + '<br>'

    for string in action.split('\n'):
        if string.strip() != 'ПУСТО':
            tmp = f'<button onclick="window.open(\'?p={string.split()[2]}\', \'_self\');">{string.split()[1].replace("%", " ")}</button>'
            res_action.append(tmp)

    return res_head, res_body, res_action


class Parser:
    def __init__(self, name, temp_path):
        self.temp_path = temp_path
        self.quest = {None: None}
        self.data = {'path': find_path_to_quest(name)}

        # загрузка квеста
        with open('quests/' + self.data['path'] + '/manifest.json', 'r', encoding='utf-8') as json_file:
            manifest = load(json_file)

        self.data.update({'title': manifest['title'],
                          'description': manifest['description'],
                          'author': manifest['author'],
                          'version': manifest['version'],
                          'age_limit': manifest['age_limit'],
                          'genre': manifest['genre']})
        self.engine_version = manifest['engine_version']

        self.processing()

    def processing(self):
        try:
            os.mkdir('static/temp/' + self.temp_path)
        except FileExistsError:
            pass

        for img in os.listdir('quests/' + self.data['path'] + '/img'):
            shutil.copyfile('quests/' + self.data['path'] + '/img/' + img, 'static/temp/' + self.temp_path + '/' + img)

        files = os.listdir('quests/' + self.data['path'] + '/text')
        for file in files:
            if file.endswith('.txt'):
                self.quest.update({file[:-4]: parse('quests/' + self.data['path'] + '/text/' + file, self.temp_path)})

    def get_page(self, name: str) -> str:
        page = ''
        buttons = []
        headers = ''

        if name == "main":
            page = f'<h1 style="margin-bottom: 5px"><b>Квест</b> "{self.data["title"]}"</h1>'
            page += f'<h4><b>Автор:</b> {self.data["author"]}</h4>'
            page += f'<h4><b>Жанр:</b> {self.data["genre"]}</h4>'
            page += f'<cite>{self.data["description"]}</cite><br>'
            buttons.append(f'<button class="action_button" style="margin-top:15px" onclick="window.location.replace(\'?p=index\')">Начать прохождение</button>')
        else:
            try:
                tmp_page = self.quest[name]
                a, b, c = tmp_page
                return [a.upper()[0] + a.swapcase()[1:], b], c
            except KeyError:
                page = f'<h2 style="color: #D20007">Внутренняя ошибка квеста!</h2><br>' \
                       f'<h3 style="color: #D20007">Страница "{name}" успешно не обнаружена</h3>'
        return ['', page], buttons
