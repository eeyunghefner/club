import functools
from abc import ABC, abstractmethod


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
        self.timetable = ['Напарник', 'Тпв']
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
        if tempf.isalpha():
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

    def enroll_tr(self, ttt):
        tempe = input('Введите номер тренинга: ')
        if tempe.isdigit():
            self.timetable.append(ttt[int(tempe)])
        else:
            print('Ошибка в вводе.')
            self.enroll_tr(ttt)

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

    def enroll_tr(self, ttt):
        tempe = input('Введите номер тренинга: ')
        if tempe.isdigit():
            self.timetable.append(ttt[int(tempe)])
        else:
            print('Ошибка в вводе.')
            self.enroll_tr(ttt)

    def start_tr(self):
        if self.id_tr == None and self.active_trainings == []:
            print(self.timetable)
            i = input('Введите номер тренинга из вашего расписания: ')
            if i.isdigit() and int(i) <= len(self.timetable):
                a = Games()
                a.set_theme(self.timetable[int(i)])
                a.start(self)
                self.id_tr = i
                self.active_trainings.append(self.timetable[int(i)])
            else:
                print('Ошибка в вводе.')
                self.start_tr()
        else:
            print(f'Тренинг {self.active_trainings[0]} уже начат. ')

    def end_tr(self):
        if self.id_tr != None:
            a = Games()
            a.set_theme(self.timetable[int(self.id_tr)])
            a.end(self)
            self.id_tr = None
            self.active_trainings.pop(0)
        else:
            print('Тренинг уже закончен. ')
            self.end_tr()

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
            'Ошибка в вводе.'
            self.create_double()
        k = input('Введите номер второго тренинга: ')
        if k.isdigit() and int(i) <= len(self.timetable):
            tr2 = self.timetable[int(k)]
        else:
            print('Ошибка в вводе: ')
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
            x.start_tr()
        else:
            self.start(x)

    def end(self, x):
        num = input(f'Введите 1, если хотите закончить тренинг {self.theme}; Введите 0, если хотите выйти: ')
        if num == '1':
            print(f'Тренинг {self.theme} пройден')
            self.is_active = False
        elif num == '0':
            print('Вы вышли.')
            x.end_tr()
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


