from loader import db, db1


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    try:
        db.create_table_users()
    except Exception as e:
        print(e)
    print(db.select_all_users())

    try:
        db1.create_table_users()
    except Exception as e:
        print(e)
    print(db1.select_all_users())


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
