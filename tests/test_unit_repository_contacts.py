import unittest
from unittest.mock import MagicMock
from datetime import datetime

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel
from src.repository.contacts import *


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactModel(
            first_name="test firstname",
            last_name="test lastname",
            email="test@test.com",
            phone_number="+380123456789",
            birthday=datetime(year=2000, month=12, day=12).date(),
            additional_info="test info",
        )
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.additional_info, body.additional_info)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_contact_found(self):
        body = ContactModel(
            first_name="test firstname",
            last_name="test lastname",
            email="test222@test.com",
            phone_number="+380123456789",
            birthday=datetime(year=2001, month=12, day=12).date(),
            additional_info="test test info",
        )
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(
            contact_id=1, body=body, user=self.user, db=self.session
        )
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        body = ContactModel(
            first_name="test firstname",
            last_name="test lastname",
            email="test222@test.com",
            phone_number="+380123456789",
            birthday=datetime(year=2001, month=12, day=12).date(),
            additional_info="test test info",
        )
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(
            contact_id=1, body=body, user=self.user, db=self.session
        )
        self.assertIsNone(result)

    async def test_search_contacts_all_match(self):
        contacts = [Contact()]
        self.session.query().filter().filter().filter().filter().all.return_value = (
            contacts
        )
        result = await search_contacts(
            first_name="test firstname",
            last_name="test lastname",
            email="test222@test.com",
            user=self.user,
            db=self.session,
        )
        self.assertEqual(result, contacts)

    async def test_search_contacts_first_name_match(self):
        contacts = [Contact()]
        self.session.query().filter().filter().all.return_value = contacts
        result = await search_contacts(
            first_name="test firstname",
            last_name="",
            email="",
            user=self.user,
            db=self.session,
        )
        self.assertEqual(result, contacts)

    async def test_search_contacts_last_name_match(self):
        contacts = [Contact()]
        self.session.query().filter().filter().all.return_value = contacts
        result = await search_contacts(
            first_name="",
            last_name="test lastname",
            email="",
            user=self.user,
            db=self.session,
        )
        self.assertEqual(result, contacts)

    async def test_search_contacts_email_match(self):
        contacts = [Contact()]
        self.session.query().filter().filter().all.return_value = contacts
        result = await search_contacts(
            first_name="",
            last_name="",
            email="test222@test.com",
            user=self.user,
            db=self.session,
        )
        self.assertEqual(result, contacts)

    async def test_search_contacts_no_match(self):
        contacts = [Contact()]
        self.session.query().filter().filter().filter().filter().all.return_value = (
            contacts
        )
        result = await search_contacts(
            first_name="Test",
            last_name="Test",
            email="test@test.com",
            user=self.user,
            db=self.session,
        )
        self.assertEqual(result, contacts)

    async def test_search_contacts_no_filters(self):
        contacts = [Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await search_contacts(
            first_name="", last_name="", email="", user=self.user, db=self.session
        )
        self.assertEqual(result, contacts)

    async def test_get_upcoming_birthdays(self):
        contacts = [
            Contact(
                first_name="test firstname",
                last_name="test lastname",
                email="test@test.com",
                phone_number="+380123456789",
                birthday=datetime(year=2000, month=5, day=20).date(),
                additional_info="test info",
            )
        ]
        self.session.query().filter().all.return_value = contacts
        result = await get_upcoming_birthdays(user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
