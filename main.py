import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Данные экскурсии с обложками
TOUR_DATA = {
    1: {
        "title": "🏛 Точка 1: Дворцовый мост",
        "text": "Дворцо́вый мост — автодорожный металлический разводной мост через Большую Неву в Санкт-Петербурге. Соединяет центральную часть города (Адмиралтейский остров) и Васильевский остров. Объект культурного наследия России регионального значения. Длина моста — 267,5 м, ширина — 31,6 м. Состоит из пяти пролётов. Разведённый центральный двукрылый пролёт Дворцового моста на фоне Кунсткамеры — один из главных символов города.",
        "cover": "photos/1.jpg",
        "photos": [
            {"file": "photos/1-1.jpg", "caption": "Первая переправа здесь появилась в 1727 году"},
            {"file": "photos/1-2.jpg", "caption": "В 1896 году наплавной Дворцовый мост был перенесён вниз по течению на 53,25 м с того места, где позже в 1911—1916 годах году был возведён постоянный Дворцовый мост[19]."},
            {"file": "photos/1-3.jpg", "caption": "Дополнительное фото 1 Дворцового моста"},
            {"file": "photos/1-4.jpg", "caption": "Дополнительное фото 2 Дворцового моста"}
        ],
        "audio": "audio/point1.mp3",
        "materials": "📚 Дополнительные материалы:\n\nЗдесь вы можете узнать больше об историческом периоде, к которому относится эта точка."
    },
    2: {
        "title": "🏰 Точка 2: Исаакиевский собор",
        "text": "Исаа́киевский собо́р (собор преподо́бного Исаа́кия Далма́тского) — крупнейший православный храм в Санкт-Петербурге. Расположен на Исаакиевской площади. Кафедральный собор Санкт-Петербургской епархии с 1858 по 1929 год.",
        "cover": "photos/2.jpg",
        "photos": [
            {"file": "photos/2-1.jpg", "caption": "Первый храм был построен для Адмиралтейских верфей, на которых к 1706 году работало более 10 тысяч человек. "},
            {"file": "photos/2-2.jpg", "caption": "В 1818 году Монферран, следуя указанию Александра I, составил проект, который предусматривал сохранение большей части ринальдиевского собора (алтарной части и подкупольных пилонов)[35][32]. "},
            {"file": "photos/2-3.jpg", "caption": "Дополнительное фото 1 Исаакиевского собора"},
            {"file": "photos/2-4.jpg", "caption": "Дополнительное фото 2 Исаакиевского собора"}
        ],
        "audio": "audio/point2.mp3",
        "materials": "📚 Дополнительные материалы:\n\nАрхитектор: Иван Иванов\nГод постройки: 1854\nСтиль: Неоклассицизм"
    },
    3: {
        "title": "🌳 Точка 3: Газпром Арена",
        "text": "«Газпром Аре́на»[5] (на всех международных матчах — стадион «Санкт-Петербург») — футбольный стадион в Санкт-Петербурге. Расположен на Крестовском острове, на месте снесённого стадиона имени С. М. Кирова[6][7]. Автор проекта «Газпром Арены» — японский архитектор Кисё Курокава[8].",
        "cover": "photos/3.jpg",
        "photos": [
            {"file": "photos/3-1.jpg", "caption": "Изначально строительство стоимостью 6,7 миллиарда рублей должно было осуществляться за счёт средств «Газпрома»[26], но впоследствии в СМИ появилась информация о том, что стадион будет построен за счёт средств городского бюджета[67] и что строительство обойдётся в 14 миллиардов[66].В августе 2008 года была озвучена сметная стоимость в 23,7 миллиарда рублей[116] и заявлено, что Санкт-Петербург откажется от финансирования «Охта-центра» в пользу стадиона[117]. 21 ноября 2011 года издание «Коммерсантъ» сообщило, что в результате доработок проекта в соответствии с требованиями ФИФА и УЕФА, включая увеличение вместимости стадиона с 62 тысяч до 69 тысяч болельщиков (около 7 тысяч за счёт установки временных трибун) и разработку новой конструкции купола для прогрева стадиона, смета может вырасти до 40 миллиардов рублей[103]."},
            {"file": "photos/3-2.jpg", "caption": "31 октября комиссия ФИФА, проверявшая готовность стадиона «Крестовский» к чемпионату мира, признала выкатное поле стадиона непригодным для проведения соревнований вследствие семикратного превышения нормативов по вибрации. Слишком сильные вибрации выкатного поля могут быть связаны с недостатком массы и жёсткости у конструкции: масса выполненного из стали основания поля составляет 5—6 тысяч тонн, а по первоначальному проекту оно должно весить 8,4 тысячи тонн"},
            {"file": "photos/3-3.jpg", "caption": "Дополнительное фото 1 Газпром Арены"},
            {"file": "photos/3-4.jpg", "caption": "Дополнительное фото 2 Газпром Арены"}
        ],
        "audio": "audio/point3.mp3",
        "materials": "📚 Дополнительные материалы:\n\nПарк был разбит в 1792 году садовым мастером Петром Сидоровым."
    }
}

# Текущая точка для каждого пользователя
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    keyboard = [
        [InlineKeyboardButton("🚶 Начать экскурсию", callback_data='start_tour')],
        [InlineKeyboardButton("📋 Список точек", callback_data='points_list')],
        [InlineKeyboardButton("ℹ️ О экскурсии", callback_data='about')],
        [InlineKeyboardButton("📞 Контакты", callback_data='contacts')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "🏛 Добро пожаловать в экскурсионного бота! Выберите действие:"
    
    await update.message.reply_text(text=text, reply_markup=reply_markup)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает главное меню с кнопкой списка точек"""
    keyboard = [
        [InlineKeyboardButton("🚶 Начать экскурсию", callback_data='start_tour')],
        [InlineKeyboardButton("📋 Список точек", callback_data='points_list')],
        [InlineKeyboardButton("ℹ️ О экскурсии", callback_data='about')],
        [InlineKeyboardButton("📞 Контакты", callback_data='contacts')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "🏛 Добро пожаловать в экскурсионного бота! Выберите действие:"
    
    if update.callback_query:
        await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup)

async def start_tour(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Начинает экскурсию с первой точки"""
    user_id = update.effective_user.id
    user_states[user_id] = 1
    await show_tour_point(update, context, user_id)

async def show_tour_point(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> None:
    """Показывает текущую точку экскурсии с обложкой"""
    point_number = user_states[user_id]
    point_data = TOUR_DATA[point_number]
    
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(point_data["cover"], 'rb'),
        caption=point_data["title"]
    )
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=point_data["text"]
    )
    
    keyboard = [
        [
            InlineKeyboardButton("📷 Фото", callback_data=f'photos_{point_number}'),
            InlineKeyboardButton("🔊 Аудио", callback_data=f'audio_{point_number}'),
            InlineKeyboardButton("📚 Текст", callback_data=f'materials_{point_number}'),
        ],
        [
            InlineKeyboardButton("🏠 Меню", callback_data='main_menu'),
            InlineKeyboardButton("📋 Список точек", callback_data='points_list'),   
        ],
        [
            InlineKeyboardButton("Следующая точка ➡️", callback_data=f'next_{point_number}'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Выберите действие:",
        reply_markup=reply_markup
    )

async def send_photos(update: Update, context: ContextTypes.DEFAULT_TYPE, point_number: int, show_additional=False):
    """Отправляет фото для указанной точки"""
    point_data = TOUR_DATA[point_number]
    
    if show_additional:
        # Отправляем только дополнительные фото (начиная с индекса 2)
        photos_to_send = point_data["photos"][2:]
    else:
        # Отправляем только первые 2 фото
        photos_to_send = point_data["photos"][:2]
    
    for photo in photos_to_send:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=open(photo["file"], 'rb'),
            caption=photo["caption"]
        )
    
    # Меню после просмотра фото
    keyboard = []
    
    if not show_additional and len(point_data["photos"]) > 2:
        # Если есть дополнительные фото и мы еще не показали их
        keyboard.append([
            InlineKeyboardButton("📷 Еще фото", callback_data=f'more_photos_{point_number}')
        ])
    
    keyboard.extend([
        [
            InlineKeyboardButton("📋 Список точек", callback_data='points_list'),
        ],
        [
            InlineKeyboardButton("Следующая точка ➡️", callback_data=f'next_{point_number}'),
        ]
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Выберите действие:",
        reply_markup=reply_markup
    )

async def show_points_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает список всех точек экскурсии для быстрого перехода"""
    keyboard = []
    
    for point_num in TOUR_DATA:
        point_title = TOUR_DATA[point_num]["title"]
        keyboard.append(
            [InlineKeyboardButton(f"{point_title}", callback_data=f'jump_{point_num}')]
        )
    
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data='main_menu')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text="📋 Выберите точку экскурсии:",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            text="📋 Выберите точку экскурсии:",
            reply_markup=reply_markup
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    # Обработка простых кнопок без подчеркивания
    if query.data in ['main_menu', 'start_tour', 'about', 'contacts', 'points_list']:
        if query.data == 'main_menu':
            await show_main_menu(update, context)
        elif query.data == 'start_tour':
            await start_tour(update, context)
        elif query.data == 'about':
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="ℹ️ Это экскурсионный бот по историческому комплексу.\n\nПродолжительность: 1,5 часа\nМаршрут: 10 точек\nЯзыки: русский"
            )
        elif query.data == 'contacts':
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="📞 Контакты:\n\nЭкскурсовод: Анна Петрова\nТелефон: +7 (123) 456-78-90\nEmail: guide@example.com"
            )
        elif query.data == 'points_list':
            await show_points_list(update, context)
        return
    
    # Обработка кнопок с подчеркиванием
    parts = query.data.split('_')
    action = parts[0]
    
    try:
        point_number = int(parts[-1])  # Берем последнюю часть как номер точки
    except (IndexError, ValueError):
        point_number = None
    
    if action == 'jump' and point_number:
        user_states[user_id] = point_number
        await show_tour_point(update, context, user_id)
    elif action == 'more' and point_number and parts[1] == 'photos':
        # Отправляем только дополнительные фото
        await send_photos(update, context, point_number, show_additional=True)
    elif action in ['prev', 'next'] and point_number:
        if action == 'prev' and point_number > 1:
            user_states[user_id] = point_number - 1
        elif action == 'next' and point_number < len(TOUR_DATA):
            user_states[user_id] = point_number + 1
        await show_tour_point(update, context, user_id)
    elif point_number:
        point_data = TOUR_DATA.get(point_number)
        if not point_data:
            return
            
        if action == 'photos':
            await send_photos(update, context, point_number)
        elif action == 'audio':
            await context.bot.send_audio(
                chat_id=query.message.chat_id,
                audio=open(point_data["audio"], 'rb'),
                title=f"Аудиогид: {point_data['title']}",
                performer="Экскурсионный гид"
            )
        elif action == 'materials':
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=point_data["materials"],
                parse_mode="Markdown"
            )

def main() -> None:
    """Запуск бота"""
    application = Application.builder().token("7431332809:AAEKuhntXgihb_KbHdfBrR3vGAzfxOx4eeI").build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('menu', show_main_menu))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    application.run_polling()

if __name__ == '__main__':
    main()