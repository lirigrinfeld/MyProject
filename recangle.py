class BBox:
    def __init__(self, minx, miny, maxx, maxy):
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy

    def __str__(self):
        return f"[{self.minx}, {self.miny}, {self.maxx}, {self.maxy}]"


class Rectangle:
    def __init__(self, x, y, height, width, speed, content):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.speed = speed
        self.content = content

    def __str__(self):
        return f"[{self.x}, {self.y}, {self.height}, {self.width}, {self.speed}, {self.content}]"

    def in_bbox(self, bbox):
        if (self.x >= bbox.minx) and (self.x < bbox.maxx) and (self.y >= bbox.miny) and (self.y < bbox.maxy):
            return True
        if (self.x + self.width >= bbox.minx) and (self.x + self.width < bbox.maxx) and (self.y + self.height >= bbox.miny) and (self.y + self.height < bbox.max):
            return True
        return False

    def draw(self, canvas):
        self.rect = canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, outline="#fb0", fill="#fb0")

    def shift(self, dx):
        self.x += dx


class Scene:
    def __init__(self, rectangles):
        self.rectangles = rectangles

    def __str__(self):
        to_string = ''
        for i in range(len(self.rectangles)):
            to_string = to_string + self.rectangles[i].__str__()
        return to_string

    def draw(self, canvas):
        for rectangle in self.rectangles:
            rectangle.draw(canvas)

    def clear(self):
        pass

    def bbox_scene(self, bbox):
        rect_list = []
        for rect in self.rectangles:
            if rect.in_bbox(bbox):
                rect_list.append(rect)
        sub_scene = Scene(rect_list)
        return sub_scene

    def shift(self, dx):
        for x in self.rectangles:
            x.shift(dx)


class Screen:
    def __init__(self, id, bbox_360):
        self.id = id
        self.bbox = bbox_360

    def __str__(self):
        return f"[{str(self.id)}, {self.bbox.__str__()}]"

    def draw(self, scene, canvas):
        for obj in scene:
            if obj.in_bbox(self.bbox):
                obj.draw(self.bbox, canvas)


def main():
    rect1 = Rectangle(10, 10, 100, 100, 0, None)
    rect2 = Rectangle(120, 10, 100, 100, 0, None)

    my_scene = Scene([rect1, rect2])

    bbox1 = BBox(0, 0, 320, 200)
    screen1 = Screen(1, bbox1)

    bbox2 = BBox(320, 0, 640, 200)
    screen2 = Screen(2, bbox2)

    bbox3 = BBox(640, 0, 960, 200)
    screen3 = Screen(3, bbox3)

    screens = [screen1, screen2, screen3]

    for i in range(len(screens)):
        print(screens[i].__str__())
    print(my_scene.__str__())


if __name__ == '__main__':
    main()
