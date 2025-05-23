import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import UserModel, UserDb
from src.repository.users import *


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_user_by_email_found(self):
        user = User()
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email='test@test.com', db=self.session)
        self.assertEqual(result, user)

    async def test_get_user_by_email_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email='test@test.com', db=self.session)
        self.assertIsNone(result)

    async def test_create_user(self):
        body = UserModel(
            username = 'test',
            email = 'test@test.com',
            password = 'asdfasdf'
        )
        result = await create_user(body, db=self.session)

        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_token(self):
        user = User()
        user.refresh_token = 'token'
        new_token = 'new_token'
        await update_token(user, new_token, self.session)

        self.assertEqual(user.refresh_token, new_token)

    async def test_confirmed_email_found(self):
        user = User()
        user.confirmed = False
        self.session.query().filter().first.return_value = user
        await confirmed_email('test@email.com', self.session)
        self.assertEqual(user.confirmed, True)

    async def test_update_password(self):
        user = User()
        user.password = "1234"
        new_password = "5678"
        await update_password(user, new_password, self.session)
        self.assertEqual(user.password, new_password)

    async def test_update_avatar_found(self):
        user = User()
        user.avatar = 'testurl1'
        new_url = 'testurl2'
        self.session.query().filter().first.return_value = user

        result = await update_avatar('test@test.com', new_url, self.session)
        self.assertEqual(user.avatar, new_url)


if __name__ == "__main__":
    unittest.main()