
import json

class Order:
    def __init__(self, order_id):
        self.id = order_id
        self.items = {}

    def setItem(self, item_id, count):
        if item_id not in self.items:
            self.items[item_id] = count
        self.items[item_id] = count

    def reprJSON(self):
        return dict(id=self.id, items=[dict(id=i, count=self.items[i]) for i in self.items])

class OrderEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Order):
            return obj.reprJSON()
        return json.JSONEncoder.default(self, obj)

def main(filename):
    preor = json.load(open(filename, 'r'))
    preor.sort(key=lambda x: x['event_id'])
    orders = {}
    for el in preor:
        order_id = el['order_id']
        item_id = el['item_id']
        count = el['count'] - el['return_count']
        status = el['status']
        if order_id not in orders:
            orders[order_id] = Order(order_id)
        if status == 'CANCEL':
            if item_id in orders[order_id].items:
                orders[order_id].items.pop(item_id)
            continue
        else:
            orders[order_id].setItem(item_id, count)
    result = []
    for order_id in orders:
        buf = {}
        for item_id in orders[order_id].items:
            count = orders[order_id].items[item_id]
            if count < 1:
                continue
            buf[item_id] = count
        orders[order_id].items = buf
        if (len(buf) != 0):
            result.append(orders[order_id])
    print(json.dumps(result, cls=OrderEncoder))

if __name__ == '__main__':
    filename = 'test2.txt'
    main(filename)
