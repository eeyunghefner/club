import functools
from threading import Thread
import asyncio
from abc import ABC, abstractmethod
from time import sleep, perf_counter
from peewee import *
from datetime import date

tt = SqliteDatabase('timetablenew.db')


class Tt(Model):
    id = PrimaryKeyField(unique=True)
    time = DateTimeField()
    place = CharField()
    theme = CharField()
    is_active = BooleanField()

    class Meta:
        database = tt
        order_by = 'id'
        tt_table = 'timetable'


with tt:
    tt.create_tables([Tt])


def benchmark(func):
    import time
    def duration(self, *args, **kwargs):
        start = time.time()
        func(self, *args, **kwargs)
        end = time.time()
        print('Время тренинга: {} секунд.'.format(end - start))

    return duration


def validate_text(func):
    def wrapper(self, nottempg, tempg):
        if not nottempg.isalpha():
            raise ValueError("Текст должен состоять только из букв")
        func(self, nottempg, tempg)
        if len(tempg) >= 100:
            raise ValueError("Текст не должен превышать 100 символов")

    return wrapper


class Adapter:

    def __init__(self):
        self.name = None
        self.faculty = None
        self.course = None
        self.timetable = {}
        self.old_timetable = []
        self.active_trainings = []

    def set_name(self):
        a = []
        tempn = input('Введите ФИ студента: ')
        a = tempn.split()
        if a[0].isalpha() and a[1].istitle():
            self.name = tempn
        else:
            print('Ошибка в вводе.')
            self.set_name()

    def get_name(self):
        print(self.name)

    def set_faculty(self):
        tempf = input('Введите возраст студента: ')
        if tempf.isdigit():
            if int(tempf) <= 0:
                raise My_age_Error(tempf)
            self.faculty = tempf
        else:
            print('Ошибка в вводе.')
            self.set_faculty()

    def get_faculty(self):
        print(self.faculty)

    def set_course(self):
        tempc = input('Введите курс студента: ')
        if tempc.isdigit():
            self.course = tempc
        else:
            print('Ошибка в вводе.')
            self.set_course()

    def get_course(self):
        print(self.course)

    def check_timetable(self):
        print(self.timetable)


class Participante(Adapter):
    def __init__(self):
        Adapter.__init__(self)
        self.is_old = False

    def enroll_tr(self, Tt, Games_new):
        try:
            tran = Games_new.get(theme=f'{input()}')
            choose = Tt.create(time=tran.time, place=tran.place, theme=tran.theme,
                               is_active=tran.is_active)
            self.timetable[f'{choose.id}'] = [choose.place, choose.theme]
            print(self.timetable)
        except IndexError:
            print('Ошибка в вводе.')
            self.enroll_tr(Tt, Games_new)

    @benchmark
    def visit_tr(self):
        print(self.timetable)
        i = input('Введите номер тренинга из вашего расписания: ')

        if i.isdigit() and int(i) <= len(self.timetable):
            print(f'Вы посетили тренинг {self.timetable[int(i)]}')
        else:
            print('Ошибка в вводе.')
            self.visit_tr()


class Organisator(Adapter):
    class __SMM:
        def post(self):
            print('Пост выложен')

    def __init__(self):
        Adapter.__init__(self)
        self.id_tr = None

    def enroll_tr(self, Tt, Games1):
        try:
            tran = Games_new.get(theme=f'{input()}')
            choose = Tt.create(time=tran.time, place=tran.place, theme=tran.theme,
                               is_active=tran.is_active)
            self.timetable[f'{choose.id}'] = [choose.place, choose.theme]
            print(self.timetable)
        except IndexError:
            print('Ошибка в вводе.')
            self.enroll_tr(Tt, Games_new)

    def start_tr(self, Tt, Games1):
        if self.id_tr == None and self.active_trainings == []:
            print(self.timetable)
            i = input('Введите номер тренинга из вашего расписания: ')
            tr = Tt.get(id=i)
            if i.isdigit():
                if tr.is_active == 0:
                    a = Games()
                    a.set_theme(self.timetable[i])
                    a.start(self)
                    self.id_tr = i
                    self.active_trainings.append(self.timetable[i])
                    tr.is_active = 1
                    tr.save()
            else:
                print('Ошибка в вводе.')
                self.start_tr(Tt, Games_new)
        else:
            print(f'Тренинг {self.active_trainings[0]} уже начат. ')

    def end_tr(self, Tt):
        if self.id_tr != None:
            a = Games()
            a.set_theme(self.timetable[self.id_tr])
            a.end(self)
            Tt.delete().where(Tt.id == self.id_tr).execute()
            self.id_tr = None
        else:
            print('Тренинг уже закончен. ')
            self.end_tr(Tt)
        self.active_trainings = None

    @benchmark
    def training(self):
        self.start_tr()
        self.end_tr()

    def create_double(self):
        i = input('Введите номер первого тренинга: ')
        tr1 = ''
        tr2 = ''
        if i.isdigit() and int(i) <= len(self.timetable):
            tr1 = self.timetable[int(i)]
        else:
            self.create_double()
        k = input('Введите номер второго тренинга: ')
        if k.isdigit() and int(i) <= len(self.timetable):
            tr2 = self.timetable[int(k)]
        else:
            self.create_double()
        self.old_timetable.append(tr1 + tr2)
        print(self.old_timetable)


class Training(ABC):
    def __init__(self):
        self.time = None
        self.place = None
        self.theme = None
        self.is_active = True

    @abstractmethod
    def return_call(self):
        pass


class QualityMixin:
    def set_time(self, t):
        self.time = t

    def set_place(self, p):
        self.place = p

    def set_theme(self, th):
        self.theme = th

    def start(self, x):
        num = input(f'Введите 1, если хотите начать тренинг {self.theme}; Введите 0, если хотите выйти: ')
        if num == '1':
            print(f'Тренинг {self.theme} начался')
        elif num == '0':
            print('Вы вышли.')
            x.start_tr(Tt, Games_new)
        else:
            self.start(x)

    def end(self, x):
        num = input(f'Введите 1, если хотите закончить тренинг {self.theme}; Введите 0, если хотите выйти: ')
        if num == '1':
            print(f'Тренинг {self.theme} пройден')
            self.is_active = False
        elif num == '0':
            print('Вы вышли.')
        else:
            self.end(x)


class Games(Training, QualityMixin):
    def __init__(self):
        super().__init__()
        self.type = 'Игры'

    def __str__(self):
        return "{0}".format(self.theme)

    def __add__(self, other):
        hard_tr = self.theme + other.theme
        g = Games()
        g.set_theme(hard_tr)
        return (hard_tr)

    def return_call(self):
        tempg = ''
        tempg = (input('Ответьте в 100 буквенных символах: как прошел ваш тренинг? '))
        nottempg = tempg.split()
        nottempg = ''.join(nottempg)
        self.print_call(nottempg, tempg)

    @validate_text
    def print_call(self, nottempg, tempg):
        print(f'Ваша обратка: {tempg}')


class Theory(Training):
    def __init__(self):
        super().__init__()
        self.type = 'Теория'

    def __str__(self):
        return "{0}".format(self.theme)

    def __add__(self, other):
        hard_tr = self.theme + other.theme
        g = Games()
        g.set_theme(hard_tr)
        return (hard_tr)

    def return_call(self):
        tempt = []
        tempt.append(input('Ответьте: Что из теории вам запомнилось больше всего?'))
        print(f'Ваша обратка: {tempt}')


class Create_new_training(type):
    base = (Training, QualityMixin)

    def __init__(self, name, base, attrs):
        self.time = None
        self.place = None
        self.theme = None
        super().__init__(name, base, attrs)

    attrs = {}

    def __new__(cls, name, base, attrs):
        return super().__new__(cls, name, base, attrs)

    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


class New_Training(metaclass=Create_new_training):
    def __new__(cls):
        return super(New_Training, cls).__new__(cls)


class My_age_Error(Exception):
    def __init__(self, age, message='Введите свой настоящий возраст'):
        self.age = age
        self.mess = message
        super().__init__(self.mess)


def time_writing():
    print('У вас есть 10 секунд, чтобы написать обратку!')
    sleep(5)
    print('Время написания вышло.')


async def f1(tt, x):
    print('Организатор выбрал тренинг')
    await asyncio.sleep(3)
    a = Organisator()
    a.enroll_tr(tt, x)
    print(f'Организатор записался на тренинг {tt[x]}')


async def f2(tt, x):
    print('Участник выбрал тренинг')
    await asyncio.sleep(3)
    b = Participante()
    b.enroll_tr(tt, x)
    print(f'Участник записался на тренинг{tt[x]}')


async def main(tt):
    task1 = asyncio.create_task(f1(tt, 1))
    task2 = asyncio.create_task(f2(tt, 1))
    await task1
    await task2


db = SqliteDatabase('trainingsnew.db')


class Trainings(Model):
    id = PrimaryKeyField(unique=True)
    time = DateTimeField()
    place = CharField()
    theme = CharField()
    is_active = BooleanField()

    class Meta:
        database = db
        order_by = 'id'


class Games_new(Trainings):
    class Meta:
        db_table = 'games'


class Theory_new(Trainings):
    class Meta:
        db_table = 'theory'


with db:
    db.create_tables([Games_new, Theory_new])
print('Done')

