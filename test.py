import unittest
import json
import io
from main import app


class ResalApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client

    def test_getting_top_product(self):
        res = self.client().get('/api/v1/bestProduct', data={
            'csvFile': (io.BytesIO(b'id,product_name,customer_average_rating\n\
                    132,"Massoub gift card", 5.0\n\
                    154,"Kebdah gift card", 3.2\n\
                    12,"Fatayer gift card", 1.8\n\
            '), 'csvFile.csv')
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['top_product'], 'Massoub gift card')
        self.assertEqual(data['product_rating'], 5.0)

    def test_getting_top_product_2(self):
        res = self.client().get('/api/v1/bestProduct', data={
            'csvFile': (io.BytesIO(b'id,product_name,customer_average_rating\n\
                    132,"Massoub gift card", 5.0\n\
                    154,"Kebdah gift card", 3.2\n\
                    12,"Kabab gift card", 10.8\n\
            '), 'csvFile.csv')
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['top_product'], 'Kabab gift card')
        self.assertEqual(data['product_rating'], 10.8)

    def test_getting_top_product_missing_column(self):
        res = self.client().get('/api/v1/bestProduct', data={
            'csvFile': (io.BytesIO(b'id,product_name\n\
                    132,"Massoub gift card"\n\
                    154,"Kebdah gift card"2\n\
                    12,"Kabab gift card"\n\
            '), 'csvFile.csv')
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Incorrect columns')

    def test_getting_top_product_no_file(self):
        res = self.client().get('/api/v1/bestProduct')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Missing file')


if __name__ == "__main__":
    unittest.main()
