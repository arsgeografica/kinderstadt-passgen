from passgen.models import Order


def test_order_creation(app):
    """Test order creation yields correct ranges"""
    with app.test_request_context():
        a = Order.create(size=100)
        assert a.range_from == 1
        assert a.range_size == 100

        b = Order.create(size=200)
        assert b.range_from == 101
        assert b.range_size == 200

        c = Order.create(size=300)
        assert c.range_from == 301
        assert c.range_size == 300


def test_order_api_create():
    pass
