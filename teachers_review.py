from telegram import (
    Update, CallbackQuery, ReplyKeyboardMarkup
)
from telegram.ext import CallbackQueryHandler, MessageHandler, Filters, \
    CallbackContext
import translations
import bd_worker
import translations as tr
from translations import gettext as _
from utils import make_inline_keyboard, main_reply, answer_query

from states import State

TEACHERS_KEYBOARD = 'TEACHERS_LIST'
TEACHERS_INDEX = 'TEACHERS_LIST_INDEX'
MAX_INLINE_CHARACTERS = 80
MAX_INLINE_COLUMNS = 1
MAX_INLINE_ROWS = 5


class Answers:
    NOT_IN_LIST = 'NOT_IN_LIST'
    TYPE_AGAIN = 'TYPE_AGAIN'
    FORWARD = 'FORWARD'
    BACK = 'BACK'


def start(update: Update, context: CallbackContext):
    if update.message.text == _(tr.REVIEW_ADD, context):
        update.message.reply_text("Введите ФИО преподователя")
        return State.ADD_T
    elif update.message.text == _(tr.REVIEW_READ, context):
        update.message.reply_text("Начните вводить имя преподователя")
        return State.READ_T
    elif update.message.text == 'Назад':
        main_reply(update.message.reply_text, context)
        return State.FIRST_NODE
    return None


def add_t(update: Update, context: CallbackContext):
    teachers = bd_worker.find_teachers(update.message.text)
    if teachers:
        context.user_data['teacher_name'] = update.message.text
        print(get_teachers_keyboards(teachers))
        context.user_data[TEACHERS_KEYBOARD] = [get_teachers_keyboards(teachers)[0][:-1]]
        print(context.user_data[TEACHERS_KEYBOARD])
        context.user_data[TEACHERS_KEYBOARD][0].append([['Нет в списке?', 'NOT_IN_LIST']])
        print(context.user_data[TEACHERS_KEYBOARD])
        show_teachers(update.message.reply_text, context)
        return State.ADD_T_INLINE
    else:
        context.user_data['teacher_name'] = update.message.text
        update.message.reply_text("Оставьте отзыв о преподователе")
        return State.ADD_DESC


def addictional_add(update, context):
    context.user_data['teacher_name'] = update.message.text
    update.message.reply_text("Оставьте отзыв о преподователе")
    return State.ADD_DESC


def add_t_inline(update, context):
    data, reply = answer_query(update, context)
    if data == Answers.NOT_IN_LIST:
        reply("Введите полное ФИО")
        return State.ADDICTIONAL_ADD
    else:
        print(data)
        context.user_data['teacher_name'] = data
        reply("Оставьте отзыв о преподователе")
        return State.ADD_DESC


def get_teachers_keyboards(teachers):
    rows = [[]]
    last_len = 0
    for t in teachers:
        if (last_len + len(t) > MAX_INLINE_CHARACTERS
            or len(rows[-1]) + 1 > MAX_INLINE_COLUMNS) \
                and len(rows[-1]) != 0:
            rows.append([])
        rows[-1].append([t, t])
    keyboards = []
    for i in range(0, len(rows), MAX_INLINE_ROWS - 1):
        keyboards.append(rows[i:i + MAX_INLINE_ROWS - 1])
        row = [
            ['Написать заново', Answers.TYPE_AGAIN]
        ]
        if i > 0:
            row.append(['<<< Назад', Answers.BACK])
        if i + MAX_INLINE_ROWS - 1 < len(rows):
            row.append(['>>> Дальше', Answers.FORWARD])
        keyboards[-1].append(row)
    return keyboards


def show_teachers(set_message, context):
    teachers_keyboard = context.user_data[TEACHERS_KEYBOARD]
    i = context.user_data.setdefault(TEACHERS_INDEX, 0)
    keyboard = teachers_keyboard[i]
    set_message(text="Учителя:", reply_markup=make_inline_keyboard(keyboard))


def show_teacher_feedback(reply, teacher_name):
    teacher = bd_worker.read_teacher(teacher_name)
    msg = str(teacher_name) + '\nОтзывы: ' + '\n***\n'.join(
        teacher["feedback"]) + '\nРейтинг: ' + str(
        sum(teacher["ratings"]) / len(teacher["ratings"]))
    reply(msg)


def read_t(update: Update, context: CallbackContext):
    teachers = bd_worker.find_teachers(update.message.text)
    if len(teachers) == 0:
        update.message.reply_text('Такого преподователя не найдено')
    elif len(teachers) > 1:
        context.user_data[TEACHERS_KEYBOARD] = get_teachers_keyboards(teachers)
        show_teachers(update.message.reply_text, context)
        return State.READ_T_INLINE
    else:
        show_teacher_feedback(update.message.reply_text, teachers[0])
        main_reply(update.message.reply_text, context)
        return State.FIRST_NODE


def read_t_inline(update, context):
    data, reply = answer_query(update, context)

    if data == Answers.FORWARD:
        context.user_data[TEACHERS_INDEX] += 1
        show_teachers(reply, context)
        return None
    elif data == Answers.BACK:
        context.user_data[TEACHERS_INDEX] -= 1
        show_teachers(reply, context)
        return None
    elif data == Answers.TYPE_AGAIN:
        del context.user_data[TEACHERS_INDEX]
        reply("Начните вводить имя преподователя")
        return State.READ_T
    else:
        del context.user_data[TEACHERS_INDEX]
        show_teacher_feedback(reply, data)
        main_reply(update.effective_user.send_message, context)
        return State.FIRST_NODE


def add_desc(update: Update, context: CallbackContext):
    context.user_data['teacher_desc'] = update.message.text
    update.message.reply_text("Как вы оцените преподователя? (из 10)")
    return State.ADD_RATING


def add_rating(update: Update, context: CallbackContext):
    if update.message.text.isnumeric() and 0 <= int(update.message.text) <= 10:
        context.user_data['teacher_rating'] = update.message.text
        teacher = bd_worker.read_teacher(context.user_data['teacher_name'])
        if not teacher:
            bd_worker.add_new_teacher(context.user_data['teacher_name'],
                                      context.user_data['teacher_desc'],
                                      context.user_data['teacher_rating'])
        else:
            bd_worker.add_new_description(context.user_data['teacher_name'],
                                      context.user_data['teacher_desc'],
                                      context.user_data['teacher_rating'])
        main_reply(update.message.reply_text, context)
        return State.FIRST_NODE
    else:
        update.message.reply_text(
            'Неправильный рейтинг, выберите число от 0 до 10')
        return None


def get_states():
    return {
        State.ADDICTIONAL_ADD: [MessageHandler(Filters.text, addictional_add)],
        State.REVIEW: [MessageHandler(Filters.text, start)],
        State.ADD_T: [MessageHandler(Filters.text, add_t)],
        State.READ_T: [MessageHandler(Filters.text, read_t)],
        State.READ_T_INLINE: [CallbackQueryHandler(read_t_inline)],
        State.ADD_T_INLINE: [CallbackQueryHandler(add_t_inline)],
        State.ADD_DESC: [MessageHandler(Filters.text, add_desc)],
        State.ADD_RATING: [MessageHandler(Filters.text, add_rating)],
    }
