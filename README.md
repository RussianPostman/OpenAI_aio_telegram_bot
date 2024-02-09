# OpenAI_aio_telegram_bot

Проект по общению с языковыми моделями OpenAI через апи. Реализованные фичи:
- Для каждого пользователя бота автоматически при запуске создавался личный кабинет в базе данных (PostgresQL) После каждого запроса к GPT или Wisper считается количество потраченных токенов и записывается за пользователем
- Возможность общаться с GPT 3 и GPT 4 моделями.
- Сохранение контекста каждого диалога в БД с возможностью в любой момент его продолжить.
- Транскрипция аудиосообщения или любого аудиофайла с речью в текст. Возможность сразу отправить как сообщение языковой модели.
- Настройка параметров диалога с ГПТ (температура, top_p и т.д.)
- Старт диалога с одним из выбранных пресетов (SQL помощник, бизнес помощник и т.д.)
Технологии:
- python openai, aiogram, SQLAlchemy, Ffmpeg

Канонично описывать процесс развёртки и запуска не стал т.к. это не ограничивается простым сбором контейнеров, а так же требует наличие двух апи ключей OpenAI (отдельно для ГПТ 3.5 и виспера, отдельно для ГПТ4). Это была вынужденная мера т.к. на момент разработка ГПТ4 только выходила в релиз и оформить подписку на основной аккаунт не получалось. Так же на момент редактирования этого ридми эндпоинтами OpenAI нельзя пользоваться с территории РФ.
Однако, если всё-таки хотите попробовать этот проект, можете связаться со мной в ТГ:
https://t.me/Russian_Postman
