from utils.db_api.sqllite import Database

dp = Database()

def test():
    dp.create_table_users()
    users = dp.select_all_users()
    print(f"До начала дбавления пользоватетлей: {users=}")
    dp.add_user(1, "One")
    dp.add_user(2, "Vasta")
    dp.add_user(3, "Goga")
    dp.add_user(4, "Mike")
    dp.add_user(5, "John")
    users = dp.select_all_users()
    print(f"После дбавления пользоватетлей: {users=}")
    user = dp.select_user(Name="John", id=5)
    print(f"Получил пользователя {user}")


test()