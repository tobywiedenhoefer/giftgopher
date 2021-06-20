# base packages
import unittest

# PyPi packages

# custom methods and classes
from models import *


class TestDB(unittest.TestCase):

    def setUp(self) -> None:
        # User info
        self.raw_pass = 'TestPassword123'  # valid
        self.hashed_pass = bcrypt.generate_password_hash(self.raw_pass).decode('utf-8')
        self.username = 'TstUsr'
        self.email = 'testusr@test.com'

        self.user = User(username=self.username, password=self.hashed_pass, email=self.email)
        if db.session.query(User).filter_by(email=self.user.email).count() == 0:
            db.session.add(self.user)
            db.session.commit()

        self.user_query = db.session.query(User).filter_by(email=self.user.email)

        # Gift One
        self.gift_name_one = "Gift One"
        self.link_one = "www.google.com"
        self.description_one = "Testing Gift One"
        self.public_one = True

        self.gift_one = Gifts(
            user_id=self.user_query.one().id,
            name=self.gift_name_one,
            link=self.link_one,
            description =self.description_one,
            public=self.public_one
        )
        if db.session.query(Gifts).filter_by(gift_id=self.gift_one.gift_id).count() < 1:
            db.session.add(self.gift_one)
            db.session.commit()

        self.gift_one_query = db.session.query(Gifts).filter_by(gift_id=self.gift_one.gift_id)

        # Gift Two
        self.gift_name_two = "Gift Two"
        self.link_two = "www.duckduckgo.com"
        self.description_two = "Testing Gift Two"
        self.public_two = False

        self.gift_two = Gifts(
            user_id=self.user_query.one().id,
            name=self.gift_name_two,
            link=self.link_two,
            description =self.description_two,
            public=self.public_two
        )
        if db.session.query(Gifts).filter_by(gift_id=self.gift_two.gift_id).count() == 0:
            db.session.add(self.gift_two)
            db.session.commit()

        self.gift_two_query = db.session.query(Gifts).filter_by(gift_id=self.gift_two.gift_id)

    def tearDown(self) -> None:
        if self.user_query.count() > 0:
            self.user_query.delete()
            db.session.commit()

        if self.gift_one_query.count() > 0:
            self.gift_one_query.delete()
            db.session.commit()

        if self.gift_two_query.count() > 0:
            self.gift_two_query.delete()
            db.session.commit()

    def test_userexistance(self):
        query = self.user_query.one()
        self.assertEqual(query.username, self.username)
        self.assertEqual(query.password, self.hashed_pass)
        self.assertEqual(query.email, self.email)

    def test_useraddition(self):
        count = self.user_query.count()
        self.assertEqual(count, 1)

    def test_userremoval(self):
        self.user_query.delete()
        db.session.commit()

        self.assertEqual(self.user_query.count(), 0)

    def test_userpass(self):
        """
        Assert pass is hashed for User table.
        """
        query = db.session.query(User).filter_by(email=self.user.email).one()
        self.assertEqual(query.password, self.hashed_pass)
        self.assertNotEqual(query.password, self.raw_pass)

    def test_giftexistance(self):
        gift_one = self.gift_one_query.one()
        self.assertEqual(gift_one.name, self.gift_name_one)
        self.assertIsNotNone(gift_one.date_posted)
        self.assertTrue(gift_one.public)

    def test_giftuserconnection(self):
        gift_one = self.gift_one_query.one()
        gift_two = self.gift_two_query.one()

        self.assertEqual(gift_one.user_id, gift_two.user_id)
        self.assertEqual(gift_one.user_id, self.user_query.one().id)


if __name__ == "__main__":
    unittest.main()
