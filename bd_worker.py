import edit_distance
import json
filename = 'subjects.json'


def add_new_teacher(subject, name, description='', rating=-1, number=None):
    with open(filename, 'r') as f:
        subjects_fo = json.load(f)
        subjects_fo[subject][name] = {"feedback": [], "ratings": []}
        if description != '':
            subjects_fo[subject][name]["feedback"].append(description)
        if float(rating) >= 0:
            subjects_fo[subject][name]["ratings"].append(float(rating))
        subjects_fo[subject][name]["number"] = number
    with open(filename, 'w') as f:
        json.dump(subjects_fo, f)


def add_new_description(subject, name, description ='', rating = -1, number = None):
    with open(filename, 'r') as f:
        subjects_fo = json.load(f)
        if description != '':
            subjects_fo[subject][name]["feedback"].append(description)
        if float(rating) >= 0:
            subjects_fo[subject][name]["ratings"].append(float(rating))
        subjects_fo[subject][name]["number"] = number
    with open(filename, 'w') as f:
        json.dump(subjects_fo, f)


def find_teachers(subject, target):
    with open(filename, 'r') as f:
        subjects_fo = json.load(f)
    teachers = list(subjects_fo[subject].keys())
    target = target.lower()
    teachers.sort(
        key=lambda t: edit_distance.SequenceMatcher(a=target, b=t.lower()).distance()
    )
    return teachers


def read_teacher(subject, name):
    with open(filename, 'r') as f:
        subjects_fo = json.load(f)
        if name not in subjects_fo[subject].keys():
            return None
        return subjects_fo[subject][name]


"""---------------------------------------"""


def add_new_subject(name):
    with open(filename, 'r') as f:
        subjects_fo = json.load(f)
        subjects_fo[name] = {}
    with open(filename, 'w') as f:
        json.dump(subjects_fo, f)


def find_subject(st) -> list:
    with open(filename, 'r') as f:
        ret = []
        subjects_fo = json.load(f)
        for i in subjects_fo.keys():
            if st in i:
                ret.append(i)
        return ret


def read_subject(name):
    with open(filename, 'r') as f:
        subjects_fo = json.load(f)
        if name not in subjects_fo.keys():
            return None
        return subjects_fo[name]


def get_all_subjects() -> list:
    with open(filename, 'r') as f:
        subjects_fo = json.load(f)
        return list(subjects_fo.keys())


def is_subject_exist(subject: str) -> bool:
    with open(filename, 'r') as f:
        subjects_fo = json.load(f)
        if subject in subjects_fo.keys():
            return True
        return False

def drop(are_you_sure : bool) -> None:
    if are_you_sure:
        with open(filename, 'w') as f:
            f.write('{}')


#recommit
# drop(True)
# add_new_subject('Физика')
# add_new_subject('Математика')
# add_new_subject('Креативные технологии')
# add_new_subject('Физическая культура')
# add_new_subject('Иностранный язык')
# add_new_subject('Безопасность жизнедеятельности')
# add_new_subject('Коммуникации и командообразование')
# add_new_subject('Современные инструменты анализа данных	')
# add_new_subject('Программирование')
# add_new_teacher('Физика', 'Боярский Кирилл Кириллович', '', 10)
# add_new_teacher('Физика', 'Николаев Владимир Георгиевич', '', 10)
# add_new_teacher('Физика', 'Иванов Иван Иванович', '', 10)
# add_new_teacher('Математика', 'Иванов Иван Иванович', '', 10)
# add_new_teacher('Креативные технологии', 'Иванов Иван Иванович', '', 10)
# add_new_teacher('Иностранный язык', 'Иванов Иван Иванович', '', 10)
# add_new_teacher('Физическая культура', 'Иванов Иван Иванович', '', 10)
# add_new_teacher('Физическая культура', 'Сергеев Иван Олегович', '', 10)
# add_new_teacher('Безопасность жизнедеятельности', 'Новиков Борис Юрьевич', '', 10)
# add_new_teacher('Коммуникации и командообразование', 'Смольянинова Светлана Владимировна', '', 10)
# add_new_teacher('Программирование', 'Казаков Михаил Вячиславович', 'Хороший преподователь, рекомендую!', 10)