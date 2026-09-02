from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats

async def set_bot_commands(bot):
    # Shaxsiy chatda chiqadigan komandalar
    private_commands = [
        BotCommand(command="start", description="Botni ishga tushirish va asosiy menyu"),
        BotCommand(command="profile", description="Profil, balans va himoyalar"),
        BotCommand(command="credit", description="Qarz olish va shartlar"),
        BotCommand(command="shop", description="Olmos sotib olish va VIP tariflar"),
    ]
    await bot.set_my_commands(private_commands, scope=BotCommandScopeAllPrivateChats())

    # Guruhda chiqadigan komandalar
    group_commands = [
        BotCommand(command="game", description="O'yin yaratish"),
        BotCommand(command="vsgame", description="Jamoaviy o'yin yaratish"),
        BotCommand(command="roles", description="O'yin rollarini ko'rish"),
        BotCommand(command="leave", description="Oyindan chiqish"),
        BotCommand(command="stop", description="O'yinni to'xtatish"),
    ]
    await bot.set_my_commands(group_commands, scope=BotCommandScopeAllGroupChats())
