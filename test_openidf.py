"""py.test for openidf"""

import openidf

class TestIdfQ(object):
    """py.test for openidf.IdfQ class functions"""
    def test_sample(self):
        assert 1 == 1
    def test_init(self):
        """py.test set maxvalue of queue"""
        q = openidf.IdfQ(5)
        assert q.maxsize == 5
    def test_put(self):
        """py.test for put"""
        def afunc(i, a=0, b=0):
            return i + a + b
        item = 11
        q = openidf.IdfQ(3, afunc, **dict(a=1, b=2))
        # - 
        result = q.put(item)
        assert item in q.queue
        assert result == item + 3
        # - same item is not put again
        result = q.put(item)
        assert result == None
        # - new item is put
        item2 = 2
        result = q.put(item2)
        assert [item, item2] == list(q.queue)
        assert result == item2 + 3
        # - remove an item
        item3, item4 = 3, 4
        result = q.put(item3)
        assert [item, item2, item3] == list(q.queue)
        assert result == item3 + 3
        result = q.put(item4)
        assert result == item4 + 3
        assert [item2, item3, item4] == list(q.queue)


