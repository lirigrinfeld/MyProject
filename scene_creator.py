import pickle
import Module

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
        self.file = open(self.file, 'rb')
        if self.file.read(5).decode() == LirisFileHandler.magic_number:
            data = self.deserialize_from_file()
        else:
            data = None
        self.file.close()
        return data

    def serialize_to_file(self, file, data):
        # dump information to that file
        pickle.dump(data, file)

    def deserialize_from_file(self):
        return pickle.load(self.file)

    def serialize_to_object(self, object_model):
        return pickle.dumps(object_model)

    def deserialize_from_object(self, data):
        return pickle.loads(data)


def main():
    rect1 = Module.Rectangle(10, 10, 100, 100, 0, "boy.jpg")
    rect2 = Module.Rectangle(10, 110, 25, 100, 0, "skate.jpg")
    my_scene = Module.Scene([rect1, rect2])

    ex = LirisFileHandler("skater_boy_scene.liri")
    ex.write_to_file(my_scene)

    print(ex.read_from_file())


if __name__ == '__main__':
    main()
