import unittest

from pihole6api.metrics import PiHole6Metrics


class FakeConnection:
    def __init__(self):
        self.calls = []

    def get(self, path, params=None):
        self.calls.append((path, params))
        return {"queries": []}


class GetQueriesTests(unittest.TestCase):
    def test_client_is_sent_as_client_ip(self):
        connection = FakeConnection()
        metrics = PiHole6Metrics(connection)

        metrics.get_queries(
            length=42,
            from_ts=1000,
            until_ts=2000,
            upstream="1.1.1.1",
            domain="example.com",
            client="192.168.1.3",
            cursor="123",
        )

        self.assertEqual(len(connection.calls), 1)

        path, params = connection.calls[0]

        self.assertEqual(path, "queries")
        self.assertEqual(
            params,
            {
                "length": 42,
                "from": 1000,
                "until": 2000,
                "upstream": "1.1.1.1",
                "domain": "example.com",
                "client_ip": "192.168.1.3",
                "cursor": "123",
            },
        )
        self.assertNotIn("client", params)

    def test_client_ip_is_omitted_when_client_is_none(self):
        connection = FakeConnection()
        metrics = PiHole6Metrics(connection)

        metrics.get_queries(length=25, domain="example.org")

        self.assertEqual(len(connection.calls), 1)

        path, params = connection.calls[0]

        self.assertEqual(path, "queries")
        self.assertEqual(params["length"], 25)
        self.assertEqual(params["domain"], "example.org")
        self.assertNotIn("client", params)
        self.assertNotIn("client_ip", params)


if __name__ == "__main__":
    unittest.main()
