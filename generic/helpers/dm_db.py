import allure

from db_client.db_client import DbClient


class DmDatabase:
    def __init__(self, user, password, host, database):
        self.db = DbClient(user, password, host, database)

    def get_all_users(self):
        with allure.step("Получение информации о всех существующих пользователях"):
            query = 'select * from "public"."Users"'
            dataset = self.db.send_query(query=query)
            return dataset

    def get_user_by_login(self, login):
        with allure.step(f"Получение информации о пользователе {login}"):
            query = f'''
            select * from "public"."Users"
            where "Login" = '{login}'
            '''
            dataset = self.db.send_query(query=query)
            return dataset

    def delete_user_by_login(self, login):
        with allure.step(f"Удаление пользователя {login} из базы данных"):
            query = f'''
            delete from "public"."Users"
            where "Login" = '{login}'
            '''
            dataset = self.db.send_bulk_query(query=query)
            return dataset

    def activate_registered_user_by_login(self, login):
        with allure.step(f"Активация зарегистрированного пользователя {login} через БД"):
            query = f'''
            update "public"."Users"
            set "Activated" = true
            where "Login" = '{login}'
            '''
            dataset = self.db.send_bulk_query(query=query)
            return dataset
