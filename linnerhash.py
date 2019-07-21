from key_value import KeyValue
from test import test_corr


class LinearHash:
    def __init__(self, s):
        self.s = s
        self.container = [KeyValue(None, None) for i in range(self.s)]
        self.counter = 0

    def set(self, key, value):
        index = self.hash(key)
        while True:
            if self.container[index].key is None:
                self.container[index] = KeyValue(key, value)
                self.counter += 1
                if self.counter * 2 > self.s:
                    self.add_capacity()
                return
            if self.container[index].key == key:
                self.container[index].value = value
                return
            index = self.increase(index)

    def get(self, key):
        index = self.hash(key)
        while True:
            if self.container[index].key is None:
                return None
            if self.container[index].key == key:
                return self.container[index].value
            index = self.increase(index)

    def remove(self, key):
        index = self.hash(key)
        while True:
            if self.container[index].key is None:
                return
            if self.container[index].key == key:
                self.remove_index(index)
                return
            index = self.increase(index)

    def remove_index(self, index):
        next_index = self.search_fit_and_return_index(index)
        if next_index is None:
            self.container[index] = KeyValue(None, None)
        else:
            self.container[index] = self.container[next_index]
            self.remove_index(next_index)

    def search_fit_and_return_index(self, bucket_index):
        cur = self.increase(bucket_index)
        while self.container[cur].key is not None:
            should_in = self.hash(self.container[cur].key)
            if should_in <= bucket_index:
                if cur < should_in or bucket_index < cur:
                    return cur
            cur = self.increase(cur)
        return None

    def hash(self, key):
        return key % self.s

    def increase(self, i):
        return (i + 1) % self.s

    def add_capacity(self):
        container_copy = self.container.copy()
        self.counter = 0
        self.s *= 2
        self.container = [KeyValue(None, None) for i in range(self.s)]
        for item in container_copy:
            if item.key is not None:
                self.set(item.key, item.value)


if __name__ == '__main__':
    flag_debug = False
    lh = LinearHash(8)
    dataset = "large"
    with open(dataset + ".in", "r") as f:
        lines = f.readlines()
    results = []
    for line in lines:
        if flag_debug:
            print(line.strip())
        ops = line.split()
        if ops[0] == 'Get':
            result = lh.get(int(ops[1]))
            # print("get {} = {}".format(int(ops[1]), result))
            results.append(result)
        elif ops[0] == 'Set':
            lh.set(int(ops[1]), int(ops[2]))
        elif ops[0] == 'Del':
            lh.remove(int(ops[1]))
        else:
            print("Invalid operation: " + ops[0])
        if flag_debug:
            for item in lh.container:
                if item.key is not None:
                    print("{}:{} ".format(item.key, item.value), end="")
            print()
            # print(lh.container)
    with open("my_{}.ans".format(dataset), "w") as f:
        for result in results:
            if result is None:
                f.write("null\n")
            else:
                f.write(str(result) + "\n")
    test_corr(mine="my_{}.ans".format(dataset), correct="{}.ans".format(dataset))
