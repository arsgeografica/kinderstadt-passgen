from kinderstadt_passgen.models import Order
from kinderstadt_passgen.tasks import PassGen, execute_order


def test_create_pass(app):
    order = Order()
    order.range_from = 1
    order.range_size = 9

    with app.app_context():
        generator = PassGen(order)
        generator.init()
        from path import Path
        generator.work_dir = Path('/tmp')
        generator._create_passes()


def test_execute_order(app):
    with app.app_context():
        order = Order.create(size=11)
