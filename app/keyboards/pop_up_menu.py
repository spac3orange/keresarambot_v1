from aiogram.types import BotCommand


async def set_commands_menu(bot):
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Главное меню'),
        BotCommand(command='/cancel',
                   description='Отменить/Главное меню'),
        BotCommand(command='/about_us',
                   description='О нас')
    ]

    await bot.set_my_commands(main_menu_commands)
