import telebot
import config
from telebot import types
from operations.auth import auth, get_projects, get_tasks, get_users_from_task
from string import Template

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def sticker(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn2 = types.KeyboardButton("❓ Задать вопрос")
    markup.add(btn2)
    ''''sti = open('D:\Telegram Desktop\sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)'''
    msg = bot.send_message(message.chat.id,
                           "Добро пожаловать, {0.first_name}!\nя - <b>{1.first_name}</b>, бот созданный чтобы быть лучшей системой для работы.".format(
                               message.from_user, bot.get_me()),
                           parse_mode='html', reply_markup=markup)
    # bot.send_message(message.chat.id,'Отправьте, пожалуйста, ваш логин')


username = ''
password = ''
token = ''
project_info = []
task_info = []


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Введите логин")
        bot.register_next_step_handler(message, log)  # следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')


def log(message):  # получаем фамилию
    global username
    username = message.text
    bot.send_message(message.from_user.id, 'Введите пароль')
    bot.register_next_step_handler(message, get_password)


def get_password(message):
    global password
    global token
    password = message.text
    token = auth(username, password)
    if token == '1':
        bot.send_message(message.from_user.id, 'Неверен логин или пароль')
        bot.send_message(message.from_user.id, 'Введите логин')
        bot.register_next_step_handler(message, log)
    else:
        bot.send_message(message.from_user.id, 'Вы автори...')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Список проектов")
        button2 = types.KeyboardButton("Список твоих задач")
        button3 = types.KeyboardButton("Дедлайн задач")
        markup.add(button1, button2, button3)
        bot.send_message(message.from_user.id, text='Выберите операцию', reply_markup=markup)
        bot.register_next_step_handler(message, get_operations)


def get_operations(message):
    if message.text == "Список проектов":
        global project_info
        project_info = get_projects('http://26.190.19.174:8000/project/get/', token)
        keyboard = types.InlineKeyboardMarkup()
        for project_name in project_info:
            project_name = project_name['projectName']
            key_name = types.InlineKeyboardButton(text=project_name, callback_data=f'project.{project_name}')
            keyboard.add(key_name)
        bot.send_message(message.from_user.id, text='Список проектов', reply_markup=keyboard)
        bot.register_next_step_handler(message, get_operations)

    if message.text == "Список твоих задач":
        global task_info
        task_info = get_tasks('http://26.190.19.174:8000/project/tasks/get', token)
        keyboard = types.InlineKeyboardMarkup()
        for task_name in task_info:
            task_name = task_name['task_name']  # сюда
            key_name = types.InlineKeyboardButton(text=task_name, callback_data=f'task.{task_name}')
            keyboard.add(key_name)
        bot.send_message(message.from_user.id, text='Список задач', reply_markup=keyboard)
        bot.register_next_step_handler(message, get_operations)
    if message.text == "Дедлайн задач":
        pass


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data.split('.')[0] == 'task':
        for info in task_info:
            name = info['task_name']
            if name == call.data.split('.')[1]:
                desc = info['description']
                deadline = info['deadline']
                text = f'Название задачи: {name} \n Описание: {desc} \n Дедлайн: {deadline}'
                break
        bot.send_message(call.message.chat.id, text=text)
    if call.data.split('.')[0] == 'project':
        for info in project_info:
            name = info['projectName']
            desc = info['projDesc']
            if name == call.data.split('.')[1]:
                text = f'Название проекта: {name} \n Описание: {desc}'
                bot.send_message(call.message.chat.id, text=text)
                project_id = info['id']
                break
        tasks_info = get_tasks(f'http://26.190.19.174:8000/project/task-project/get?project_id={project_id}',
                               token)
        for info in tasks_info:
            name = info['task_name']
            desc = info['description']
            deadline = info['deadline']
            text = f'Название задачи: {name} \n Описание: {desc} \n Дедлайн: {deadline} \n Работающие над задачей: '
            task_id = info['id']
            user_info = get_users_from_task(f'http://26.190.19.174:8000/project/task-users/get?task_id={task_id}',
                                            token)
            for user in user_info:
                user_name = user['username']
                user_email = user['email']
                text_user = f'Пользователь: {user_name}, {user_email} \n'
                text += text_user
            bot.send_message(call.message.chat.id, text=text)


'''
@bot.message_handler(content_types=['text'])
def trych(message):
    global answers
    answers = []
    first_answer = message.text
    answers.append(first_answer)

    send = bot.send_message(message.chat.id, 'Отправьте, пожалуйста, ваш пароль')
    bot.register_next_step_handler(send, three_q)

def three_q(message):
    two_answer = message.text
    answers.append(two_answer)
    text1 = auth(answers[0], answers[1])
    send = bot.send_message(message.chat.id, 'Проверяем авторизацию')
    if text1 == '1':
        send = bot.send_message(message.chat.id, r'Неправильно введен логин или пароль')
        send = bot.send_message(message.chat.id, r'Введите заного')
        bot.register_next_step_handler(send, trych)
    else:
        send = bot.send_message(message.chat.id, 'Вы авторизованы')
    bot.register_next_step_handler(send, function)

def function(message):
    if (message.text == "❓ Задать вопрос"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Список проектов")
        button2 = types.KeyboardButton("Список твоих задач")
        button3 = types.KeyboardButton("Дедлайн задач")
        markup.add(button1, button2, button3)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)
    elif (message.text == "Список проектов"):
        url = "http://26.190.19.174:8000/project/get/"
        token = auth('1', '1')
        text = get_projects(url, token)
        bot.send_message(message.chat.id, text=text)
'''

bot.polling(none_stop=True)
