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
        db.session.add(self.user)
        db.session.commit()

        self.user_query = db.session.query(User).filter_by(id=self.user.id)

        # TODO: test with gifts

    def tearDown(self) -> None:
        if self.user_query.count() > 0:
            self.user_query.delete()
            db.session.commit()

        # TODO: add teardown for gifts

    def test_existance(self):
        query = self.user_query.one()
        self.assertEqual(query.username, self.username)
        self.assertEqual(query.password, self.hashed_pass)
        self.assertEqual(query.email, self.email)

    def test_addition(self):
        count = self.user_query.count()
        self.assertEqual(count, 1)

    def test_removal(self):
        self.user_query.delete()
        db.session.commit()

        self.assertEqual(self.user_query.count(), 0)

    def test_pass(self):
        """
        Assert pass is hashed for User table.
        """
        query = db.session.query(User).filter_by(id=self.user.id).one()
        self.assertEqual(query.password, self.hashed_pass)
        self.assertNotEqual(query.password, self.raw_pass)


if __name__ == "__main__":
    unittest.main()
