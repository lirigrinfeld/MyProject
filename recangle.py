import tkinter
from tkinter import Tk, Canvas, Frame, BOTH, Toplevel

class BBox:
    def __init__(self, minx, miny, maxx, maxy):
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy


class Rectangle:
    def __init__(self, x, y, height, width, speed, content):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.speed = speed
        self.content = content

    def in_bbox(self, bbox):
        if self.x >= bbox.minx and self.x < bbox.maxx and self.y >=bbox.miny and self.y <bbox.maxy:
            return True
        if self.x + self.width >= bbox.minx and self.x + self.width < bbox.maxx and self.y + self.height >= bbox.miny and self.y + self.height < bbox.max:
            return True
        return False


class Scene:
    def __init__(self, rectangles):
        self.rectangles = rectangles


    def draw(self):

    def clear(self):


class screen:

    def __init__(self, id, bbox_360):
        self.id = id
        self.bbox = bbox_360

    def draw(self, scene, draw_panel):
        for obj in scene:
            if obj.in_bbox(self.bbox)
                obj.draw(self.bbox, draw_panel)
                # liri sus rezah liri boai habita ani raev;
class SceneObject:
    def __init__(self, generator_func):
        self.id = id
        self.obj = None
        self.generator_func = generator_func

    def draw_obj(self, params):
        self.generator_func(params)

    def clear_obj(self, cleaner):
        cleaner.delete(self.obj)
        self.obj = None


# class Rectangle(SceneObject):
#     def __init__(self, id, generator_func):
#         super(Rectangle, self).__init__(id, generator_func)
#
#     def draw_obj(self, params):
#         self.generator_func(params)


class SceneManager:
    def __init__(self, tk, num_of_screens):
        self.tk = tk
        self.num_of_screens = num_of_screens
        self.screens = []

        for i in range(self.num_of_screens):
            # 1-width, 2-height, 3-posx, 4-posy (changes by i-screens' num)
            self.screens.append(Screen(800, 200, 50, 200*i+50, f"screen {i}"))

        self.delta_x = 0
        self.current = 0
        self.next = (self.current + 1) % self.num_of_screens
        self.status = 0

        # 25- time sharing- 25 ms
        self.tk.after(25, self.draw)

    def clear(self):
        self.screens[self.current].clear()
        if self.status != 0:
            self.screens[self.next].clear()

    def draw(self):
        if self.delta_x <= 700:
            if self.status == 1:
                self.status = 0
                self.current = (self.current + 1) % self.num_of_screens
                self.next = (self.current + 1) % self.num_of_screens

        else:
            if self.status == 0:
                self.status = 1

        self.screens[self.current].draw(self.delta_x)
        if self.status != 0:
            self.screens[self.next].draw(self.delta_x-800)

    def handle(self):
        self.clear()
        self.draw()
        self.delta_x = (self.delta_x + 10) % 800
        self.tk.after(40, self.handle)


class Screen(Toplevel):
    def __init__(self, width, height, pos_x, pos_y, title):
        super().__init__()
        self.initUI(width, height, pos_x, pos_y, title)
        self.rect = None

    def initUI(self, width, height, pos_x, pos_y, title):
        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
        # self.top_level.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=1)

    def clear(self):
        self.canvas.delete(self.rect)
        self.rect = None

    def draw(self, delta_x):
        self.rect = self.canvas.create_rectangle(max(0, delta_x), 10, min(100+delta_x, 800), 110,
        outline="#fb0", fill="#fb0")


class Example(Frame):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.delta_x = 0
        self.rect = None
        self.extra_rect = None


    def initUI(self):
        self.master.title("Colours")
        self.pack(fill=BOTH, expand=1)

        self.canvas = []
        self.canvas.append(Canvas(self))
        self.canvas[0].pack(fill=BOTH, expand=1)

        self.canvas[0].pack(fill=BOTH, expand=1)

        self.top_level = tkinter.Toplevel()
        self.top_level.geometry("800x200+100+400")
        #self.top_level.pack(fill=BOTH, expand=1)
        self.canvas.append(Canvas(self.top_level))
        self.canvas[1].pack(fill=BOTH, expand=1)

        self.canvas[1].pack(fill=BOTH, expand=1)

        self.after(25, self.draw)
        self.status = 0
        self.screen = 0

    def draw(self):
        if self.rect != None:
            self.canvas[self.screen].delete(self.rect)
            self.rect = None
            if self.extra_rect != None:
                self.canvas[(self.screen + 1)%2].delete(self.extra_rect)
                self.extra_rect = None

        if self.delta_x <= 700:
            if self.status == 1:
                self.status = 0
                self.screen = (self.screen + 1) % 2

            self.rect = self.canvas[self.screen].create_rectangle(self.delta_x, 10, 100+self.delta_x, 110, outline="#fb0", fill="#fb0")
        else:
            if self.status == 0:
                self.status = 1

            self.rect= self.canvas[self.screen].create_rectangle(self.delta_x, 10, 800, 110, outline="#fb0", fill="#fb0")
            self.extra_rect = self.canvas[(self.screen + 1) % 2].create_rectangle(0, 10, self.delta_x - 700, 110, outline="#fb0", fill="#fb0")

        self.delta_x = (self.delta_x + 10)%800
        self.after(25, self.draw)


def main():
    root = Tk()
    handler = SceneManager(root, 3)
    #root.geometry("800x200+100+100")
    root.after(40, handler.handle)

    root.mainloop()


if __name__ == '__main__':
    main()
