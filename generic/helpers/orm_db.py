from sqlalchemy import select, delete, update

from generic.helpers.orm_models import User
from orm_client.orm_client import OrmClient


class OrmDatabase:
    def __init__(self, user, password, host, database):
        self.db = OrmClient(user, password, host, database)

    def get_all_users(self):
        query = select([User])
        dataset = self.db.send_query(query)
        return dataset

    def get_user_by_login(self, login: str) -> list[User]:
        query = select([User]).where(User.Login == login)
        dataset = self.db.send_query(query)
        return dataset

    def delete_user_by_login(self, login):
        query = delete(User).where(User.Login == login)
        self.db.send_bulk_query(query=query)

    def activate_registered_user_by_login(self, login):
        query = update(User).where(User.Login == login).values(Activated=True)
        self.db.send_bulk_query(query=query)

    def change_registered_user_email(self, login, new_email):
        query = update(User).where(User.Login == login).values(Email=new_email)
        self.db.send_bulk_query(query=query)

    def get_password_hash_by_login(self, login) -> str:
        query = select(User.PasswordHash).where(User.Login == login)
        dataset = self.db.send_query(query)
        return dataset[0][0]
