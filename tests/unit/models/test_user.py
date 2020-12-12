from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest


class UserModelTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('username', 'password')

        self.assertEqual(user.username, 'username')
        self.assertEqual(user.password, 'password')