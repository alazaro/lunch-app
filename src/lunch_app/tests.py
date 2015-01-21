# -*- coding: utf-8 -*-
"""
Presence analyzer unit tests.
"""
from datetime import datetime, date, timedelta
import os.path
import unittest
from unittest.mock import Mock, patch

from sqlalchemy.orm import Session

from lunch_app import main, db, app
from lunch_app import utils

from lunch_app.models import Order, Food

# pylint: disable=maybe-no-member, too-many-public-methods, invalid-name

MOCK_ADMIN = Mock()
MOCK_ADMIN.is_admin.return_value = True
MOCK_ADMIN.username = 'test_user'

connection = db.engine.connect()
transaction = connection.begin()


def setUp():
    """
    Main setup.
    """
    test_config = os.path.join(
        os.path.dirname(__file__),
        '..', '..', 'parts', 'etc', 'test.cfg',
    )
    main.app.config.from_pyfile(test_config)
    main.app.config['WTF_CSRF_ENABLED'] = False
    main.init()
    db.init_app(app)
    db.create_all()


class LunchBackendViewsTestCase(unittest.TestCase):
    """
    Views tests.
    """

    def setUp(self):
        """
        Before each test, set up a environment.
        """
        self.client = main.app.test_client()
        self.__transaction = connection.begin_nested()
        self.session = Session(connection)

    def tearDown(self):
        """
        Get rid of unused objects after each test.
        """
        self.session.close()

    def test_mainpage_view(self):
        """
        Test main page view.
        """
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_info_view(self):
        """
        Test info page view.
        """
        resp = self.client.get('/info')
        self.assertEqual(resp.status_code, 200)

    def test_my_orders_view(self):
        """
        Test my orders page view.
        """
        with self.assertRaises(AttributeError):
            resp = self.client.get('/my_orders')
            self.assertEqual(resp.status_code, 200)

    def test_overview_view(self):
        """
        Test overview page.
        """
        resp = self.client.get('/overview')
        self.assertEqual(resp.status_code, 200)

    @patch('lunch_app.views.current_user', new=MOCK_ADMIN)
    def test_create_order_view(self):
        """
        Test create order page.
        """
        resp = self.client.get('/order')
        self.assertEqual(resp.status_code, 200)
        data = {'cost': 12,
                'company': 'Pod Koziołkiem',
                'description': 'dobre_jedzonko',
                'send_me_a_copy': False,
                'date': date(2015, 1, 21),
                'arrival_time': '12:00',
                'meal_from_list': ' ',
                }
        resp_2 = self.client.post('/order', data=data)
        order_db = Order.query.filter(
            Order.description == 'dobre_jedzonko'
        ).first()
        print(resp_2.status_code)
        self.assertTrue(resp_2.status_code == 302)
        self.assertEqual(order_db.description, 'dobre_jedzonko')

    @patch('lunch_app.permissions.current_user', new=MOCK_ADMIN)
    def test_add_food_view(self):
        """
        Test add food page.
        """
        resp = self.client.get('/add_food')
        self.assertEqual(resp.status_code, 200)
        data = {'cost': 333,
                'description': 'dobre_jedzonko',
                'date_available_to': date(2015, 1, 1),
                'company': 'Pod Koziołkiem',
                'date_available_from': date(2015, 1, 1),
                }
        resp_2 = self.client.post('/add_food', data=data)
        food_db = Food.query.filter(
            Food.description == 'dobre_jedzonko'
        ).first()
        self.assertTrue(resp_2.status_code == 302)
        self.assertEqual(food_db.description, 'dobre_jedzonko')

    @patch('lunch_app.permissions.current_user', new=MOCK_ADMIN)
    def test_day_summary_view(self):
        """
        Test day summary page.
        """
        resp = self.client.get('/day_summary')
        self.assertEqual(resp.status_code, 200)


class LunchBackendUtilsTestCase(unittest.TestCase):
    """
    Utils tests.
    """
    def setUp(self):
        """
        Before each test, set up a environment.
        """
        pass

    def tearDown(self):
        """
        Get rid of unused objects after each test.
        """
        pass

    def test_get_current_date(self):
        """
        Test current date.
        """
        self.assertEquals(utils.get_current_date(), date.today())

    def test_get_current_datetime(self):
        """
        Test current datetime.
        """
        self.assertAlmostEqual(
            utils.get_current_datetime(),
            datetime.now(),
            delta=(timedelta(microseconds=101)),
        )

    def test_make_date(self):
        """
        Test make date.
        """
        self.assertEquals(
            utils.make_date(datetime.now()),
            date.today()
        )


class LunchBackendPermissionsTestCase(unittest.TestCase):
    """
    Permissions tests.
    """
    def setUp(self):
        """
        Before each test, set up a environment.
        """
        self.client = main.app.test_client()

    def tearDown(self):
        """
        Get rid of unused objects after each test.
        """
        pass

    def test_permissions(self):
        """
        Tests if permissions decorator works properly
        """
        with self.assertRaises(AttributeError):
            resp = self.client.get('add_food')
            self.assertEqual(resp.status_code, 200)
            resp_2 = self.client.get('day_summary')
            self.assertEqual(resp_2.status_code, 200)


def suite():
    """
    Default test suite.
    """
    base_suite = unittest.TestSuite()
    base_suite.addTest(unittest.makeSuite(LunchBackendViewsTestCase))
    base_suite.addTest(unittest.makeSuite(LunchBackendUtilsTestCase))
    base_suite.addTest(unittest.makeSuite(LunchBackendPermissionsTestCase))
    return base_suite


if __name__ == '__main__':
    unittest.main()
