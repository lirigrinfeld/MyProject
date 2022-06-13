import pickle
import Module
import pyautogui
# file, BloB, Scene
# file->Scene : read_from_file
# Scene->File : write_to_file
# Scene->Blob : serialize_to_object
# Blob->Scene : deserialize_from_object

# file->Blob : read_from_file ... serialize_to_object

width, height = pyautogui.size()
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
    rect1 = Module.Rectangle(10, 30, 100, 100, 0, "star1.jpg")
    rect2 = Module.Rectangle(180, 90, 75, 75, 0, "star1.jpg")
    rect3 = Module.Rectangle(350, 5, 125, 125, 0, "star1.jpg")
    rect4 = Module.Rectangle(520, 100, 75, 50, 0, "star1.jpg")
    rect5 = Module.Rectangle(700, 30, 100, 75, 0, "star1.jpg")
    rect6 = Module.Rectangle(900, 110, 75, 100, 0, "star1.jpg")
    rect7 = Module.Rectangle(1100, 20, 100, 100, 0, "star1.jpg")
    rect8 = Module.Rectangle(20, 200, 75, 75, 0, "star1.jpg")
    rect9 = Module.Rectangle(150, 225, 125, 125, 0, "star1.jpg")
    rect10 = Module.Rectangle(350, 205, 75, 50, 0, "star1.jpg")
    rect11 = Module.Rectangle(500, 240, 100, 75, 0, "star1.jpg")
    rect12 = Module.Rectangle(650, 230, 75, 100, 0, "star1.jpg")
    rect13 = Module.Rectangle(850, 270, 100, 100, 0, "star1.jpg")
    rect14 = Module.Rectangle(1000, 250, 100, 100, 0, "star1.jpg")
    rect15 = Module.Rectangle(1400, 200, 75, 75, 0, "star1.jpg")
    rect16 = Module.Rectangle(1350, 5, 125, 125, 0, "star1.jpg")
    rect17 = Module.Rectangle((width/2)-350, (height/2)-200, 200, 200, 0, "moon.jpg")
    rect18 = Module.Rectangle(15, 405, 125, 125, 0, "star1.jpg")
    rect19 = Module.Rectangle(200, 600, 75, 50, 0, "star1.jpg")
    rect20 = Module.Rectangle(320, 670, 100, 75, 0, "star1.jpg")
    rect21 = Module.Rectangle(600, 620, 75, 100, 0, "star1.jpg")
    rect22 = Module.Rectangle(1000, 480, 100, 100, 0, "star1.jpg")
    rect23 = Module.Rectangle(1300, 700, 75, 75, 0, "star1.jpg")
    rect24 = Module.Rectangle(1100, 650, 125, 125, 0, "star1.jpg")
    my_scene = Module.Scene([rect1, rect2, rect3, rect4, rect5, rect6, rect7, rect8, rect9, rect10, rect11, rect12, rect13, rect14, rect15, rect16, rect17, rect18, rect19, rect20, rect21, rect22, rect23, rect24])

    ex = LirisFileHandler("stars_scene.liri")
    ex.write_to_file(my_scene)

    print(ex.read_from_file())


if __name__ == '__main__':
    main()
