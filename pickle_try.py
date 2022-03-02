import pickle

import recangle
from recangle import *



class LirisFileHandler:
    magic_number = "lirif"

    def __init__(self, filename):
        self.file = filename

    def write_to_file(self, object_model):
        file = open(self.file, 'wb')
        file.write(LirisFileHandler.magic_number.encode())
        self.serialize_to_file(file, object_model)
        file.close()

    def read_from_file(self):
        file = open(self.file, 'rb')
        if file.read(5).decode() == LirisFileHandler.magic_number:
            data = self.deserialize_from_file(file)
        else:
            data = None
        file.close()
        return data

    def serialize_to_file(self, file, data):
        # dump information to that file
        pickle.dump(data, file)

    def deserialize_from_file(self, file):
        # dump information to that file
        data = pickle.load(file)
        return data

    def serialize_to_object(self, object_model):
        return pickle.dumps(object_model)

    def deserialize_from_object(self):
        return pickle.loads(self.serialize_to_object())


def main():
    # ex = LirisFileHandler()
    # ex.serialize_to_file()
    # print(ex.deserialize_from_file())
    #
    # data = ex.serialize_to_object()
    # print(data)
    # print(ex.deserialize_from_object())

    rect1 = recangle.Rectangle(10, 10, 100, 100, 0, None)
    rect2 = recangle.Rectangle(120, 10, 100, 100, 0, None)
    my_scene = recangle.Scene([rect1, rect2])

    ex = LirisFileHandler("important.liri")
    ex.write_to_file(my_scene)

    print(ex.read_from_file())


if __name__ == '__main__':
    main()
