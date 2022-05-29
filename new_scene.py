import pickle

import rectangle_draft

# file, BloB, Scene
# file->Scene : read_from_file
# Scene->File : write_to_file
# Scene->Blob : serialize_to_object
# Blob->Scene : deserialize_from_object

# file->Blob : read_from_file ... serialize_to_object


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
        return pickle.load(file)

    def serialize_to_object(self, object_model):
        return pickle.dumps(object_model)

    def deserialize_from_object(self, data):
        return pickle.loads(data)


def main():
    # ex = LirisFileHandler()
    # ex.serialize_to_file()
    # print(ex.deserialize_from_file())
    #
    # data = ex.serialize_to_object()
    # print(data)
    # print(ex.deserialize_from_object())

    rect1 = rectangle_draft.Rectangle(10, 10, 100, 100, 0, "tree_image.jpg")
    rect2 = rectangle_draft.Rectangle(120, 10, 75, 75, 0, "tree_image.jpg")
    rect3 = rectangle_draft.Rectangle(120, 10, 50, 50, 0, "None")
    my_scene = rectangle_draft.Scene([rect1, rect2, rect3])

    ex = LirisFileHandler("NewScene.liri")
    ex.write_to_file(my_scene)

    print(ex.read_from_file())


if __name__ == '__main__':
    main()
