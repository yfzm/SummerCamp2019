from key_value import KeyValue
from test import test_corr


ABORT = -1
SUCCEED = 0


class ChangeRecord:
    def __init__(self, bn, i, k, v):
        self.bucket_num = bn
        self.index = i
        self.key = k
        self.value = v


class CockooHash:
    def __init__(self, s):
        self.s = s
        self.containers = ([KeyValue(None, None) for i in range(self.s)], [KeyValue(None, None) for i in range(self.s)])
        self.hashes = (self.hash0, self.hash1)
        self.visited_keys = set()
        self.change_list = []

    def set(self, key, value):
        for bn, container in enumerate(self.containers):
            index = self.hashes[bn](key)
            if container[index].key == key:
                container[index].value = value
                return

        self.visited_keys = set()
        self.change_list = []
        if self.set_to_cx(0, key, value) != ABORT:
            for item in self.change_list:
                self.containers[item.bucket_num][item.index] = KeyValue(item.key, item.value)
        else:
            self.set(key, value)

    def set_to_cx(self, bn, key, value):
        index = self.hashes[bn](key)
        next_bn = (bn + 1) % 2
        container = self.containers[bn]
        if container[index].key is None:
            self.change_list.append(ChangeRecord(bn, index, key, value))
            return SUCCEED

        if key in self.visited_keys:
            self.add_capacity()
            return ABORT
        self.visited_keys.add(key)

        cur_item = container[index]
        if self.set_to_cx(next_bn, cur_item.key, cur_item.value) == ABORT:
            return ABORT
        self.change_list.append(ChangeRecord(bn, index, key, value))
        return SUCCEED

    def get(self, key):
        for bn, container in enumerate(self.containers):
            index = self.hashes[bn](key)
            if container[index].key == key:
                return container[index].value
        return None

    def remove(self, key):
        for bn, container in enumerate(self.containers):
            index = self.hashes[bn](key)
            if container[index].key == key:
                container[index] = KeyValue(None, None)
                return

    def hash0(self, key):
        return key % self.s

    def hash1(self, key):
        return (key // self.s) % self.s

    def add_capacity(self):
        # print("Increase size")
        all_kvs = []
        for item in self.containers[0] + self.containers[1]:
            all_kvs.append(item)

        self.s *= 2
        self.containers = ([KeyValue(None, None) for i in range(self.s)], [KeyValue(None, None) for i in range(self.s)])
        for item in all_kvs:
            if item.key is not None:
                self.set(item.key, item.value)


if __name__ == '__main__':
    flag_debug = False
    ch = CockooHash(8)
    dataset = "large"
    with open(dataset + ".in", "r") as f:
        lines = f.readlines()
    results = []
    for line in lines:
        if flag_debug:
            print(line.strip())
        ops = line.split()
        if ops[0] == 'Get':
            result = ch.get(int(ops[1]))
            # print("get {} = {}".format(int(ops[1]), result))
            results.append(result)
        elif ops[0] == 'Set':
            ch.set(int(ops[1]), int(ops[2]))
        elif ops[0] == 'Del':
            ch.remove(int(ops[1]))
        else:
            print("Invalid operation: " + ops[0])
        if flag_debug:
            for bn, container in enumerate(ch.containers):
                print("[{}] ".format(bn), end="")
                for item in container:
                    # if item.key is not None:
                    print("({}:{})".format(item.key, item.value), end="")
                print()

    with open("my_{}.ans".format(dataset), "w") as f:
        for result in results:
            if result is None:
                f.write("null\n")
            else:
                f.write(str(result) + "\n")
    test_corr(mine="my_{}.ans".format(dataset), correct="{}.ans".format(dataset))
