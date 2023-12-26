import telebot
import random

TOKEN = '6858509264:AAHbKVlWR-nrtwCGtkpTxCZ8yJC0abP-62c'
bot = telebot.TeleBot(TOKEN)

user_profiles = {}

keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row('🎯 Рулетка', '🎰 Слоты')
keyboard.row('⛄ Профиль', '🎁 Получить бесплатное бабло')


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id not in user_profiles:
        user_profiles[user_id] = {'coins': 1000}
    bot.send_message(message.chat.id, "Привет! Добро пожаловать в игровое казино.", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == '🎯 Рулетка')
def roulette(message):
    user_id = message.from_user.id
    if user_id not in user_profiles:
        bot.send_message(message.chat.id, "Сначала создайте профиль.", reply_markup=keyboard)
        return

    bot.send_message(message.chat.id, "Введите свою ставку:")
    bot.register_next_step_handler(message, process_roulette_bet)


def process_roulette_bet(message):
    try:
        bet = int(message.text)
        if bet <= 0 or bet > user_profiles[message.from_user.id]['coins']:
            raise ValueError()

        result = play_roulette()
        update_balance(message.from_user.id, result, bet)

        if result == 'win':
            bot.send_message(message.chat.id,
                             f"Вы выиграли! Ваш баланс: {user_profiles[message.from_user.id]['coins']} монет.",
                             reply_markup=keyboard)
        elif result == 'jackpot':
            bot.send_message(message.chat.id,
                             f"Джекпот! Вы выиграли {bet * 50} монет! Ваш баланс: {user_profiles[message.from_user.id]['coins']} монет.",
                             reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id,
                             f"Вы проиграли. Ваш баланс: {user_profiles[message.from_user.id]['coins']} монет.",
                             reply_markup=keyboard)
    except ValueError:
        bot.send_message(message.chat.id, "Неверная ставка. Попробуйте снова.", reply_markup=keyboard)


def play_roulette():
    outcome = random.choices(['win', 'lose', 'jackpot'], weights=[0.35, 0.6, 0.05])[0]
    return outcome


@bot.message_handler(func=lambda message: message.text == '🎰 Слоты')
def slots(message):
    user_id = message.from_user.id
    if user_id not in user_profiles:
        bot.send_message(message.chat.id, "Сначала создайте профиль.", reply_markup=keyboard)
        return

    bot.send_message(message.chat.id, "Введите свою ставку:")
    bot.register_next_step_handler(message, process_slots_bet)


def process_slots_bet(message):
    try:
        bet = int(message.text)
        if bet <= 0 or bet > user_profiles[message.from_user.id]['coins']:
            raise ValueError()

        result = play_slots(message)
        update_balance(message.from_user.id, result, bet)

        if result == 'win':
            bot.send_message(message.chat.id,
                             f"Вы выиграли! Ваш баланс: {user_profiles[message.from_user.id]['coins']} монет.",
                             reply_markup=keyboard)
        elif result == 'jackpot':
            bot.send_message(message.chat.id,
                             f"Джекпот! Вы выиграли {bet * 10} монет! Ваш баланс: {user_profiles[message.from_user.id]['coins']} монет.",
                             reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id,
                             f"Вы проиграли. Ваш баланс: {user_profiles[message.from_user.id]['coins']} монет.",
                             reply_markup=keyboard)
    except ValueError:
        bot.send_message(message.chat.id, "Неверная ставка. Попробуйте снова.", reply_markup=keyboard)


def play_slots(message):  # Теперь принимает параметр message
    symbols = ['🍒', '🍋', '🍇', '7']
    result = [random.choice(symbols) for _ in range(3)]
    bot.send_message(message.chat.id,f"{' '.join(result)}")

    if result.count('🍋') == 3:
        return 'win_x5'
    elif result.count('🍇') == 3:
        return 'win_x2'
    elif result.count('7') == 3:
        return 'jackpot'
    else:
        return 'lose'


def update_balance(user_id, result, bet):
    if result == 'win':
        user_profiles[user_id]['coins'] += bet * 2
    elif result == 'jackpot':
        user_profiles[user_id]['coins'] += bet * 100
    elif result == 'win_x5':
        user_profiles[user_id]['coins'] += bet * 5
    elif result == 'win_x2':
        user_profiles[user_id]['coins'] += bet * 2
    else:
        user_profiles[user_id]['coins'] -= bet

@bot.message_handler(func=lambda message: message.text == '🎁 Получить бесплатное бабло')
def get_free_money(message):
    user_id = message.from_user.id
    if user_id not in user_profiles:
        user_profiles[user_id] = {'coins': 100}
    user_profiles[user_id]['coins'] += 500
    coins = user_profiles[user_id]['coins']
    bot.send_message(message.chat.id, f"Вы получили 500 монет! Теперь у вас {coins} монет.", reply_markup=keyboard)

if __name__ == '__main__':
    bot.polling(none_stop=True)