from GameData import *


class Output:
    def __init__(self, base, canvas_color, bg_color, tool_space):
        self.base = base
        self.bg_color = bg_color
        self.tool_space = tool_space
        self.canvas_color = canvas_color

        self.canvas = pygame.Surface((self.base.canvas_w, self.base.canvas_h))
        self.canvas.fill(self.canvas_color)

        self.menu_box = pygame.Surface((self.base.toolbar_w, self.base.toolbar_h))  # menuBox
        self.set_alpha(self.menu_box, 80)
        self.menu_box.fill(self.tool_space)

        # Used as background for the menu box
        self.menu_box_bg = pygame.Surface((self.base.toolbar_w, self.base.toolbar_h))
        self.menu_box_bg.fill(self.bg_color)

        self.ialpha = 150  # For the infobox
        self.info_box = pygame.Surface((self.base.infobox_w, self.base.infobox_h))
        self.set_alpha(self.info_box, self.ialpha)
        self.info_box.fill(self.bg_color)

    def blit_canvas(self):
        self.base.window.blit(self.canvas, (self.base.canvas_x, self.base.canvas_y))

    def clear_canvas(self):
        self.canvas.fill(self.canvas_color)

    def blit_background(self):
        self.base.window.fill(self.bg_color)
        self.clear_canvas()
        self.blit_canvas()

    def blit_menu(self):
        self.base.window.blit(self.menu_box_bg, (self.base.toolbar_x, self.base.toolbar_y))

        self.base.window.blit(self.menu_box, (self.base.toolbar_x, self.base.toolbar_y))
        self.base.window.blit(self.info_box, (self.base.infobox_x, self.base.infobox_y))

        self.info_box.fill(self.bg_color)

    def set_alpha(self, rectangle, alpha_val=100):
        rectangle.set_alpha(alpha_val)


class PaintData:
    def __init__(self):
        self.b_size = 10
        self.b_darkness = 0

        self.prime_color = Colors.red
        self.color = None
        self.set_color()

    def set_color(self):
        self.color = tupadd(self.prime_color, int(self.b_darkness))


class Painting:  # THE OUTPUT
    def __init__(self, output, paint_data):
        self.output = output
        self.paint_data = paint_data

        self.selected = None
        self.draw_list = []
        self.i = -1  # used for deletion
        self.cleaned_list = []

        self.undo_mode = False

        self.mouse = None
        self.clicked = None

    def get_position(self):
        self.mouse = pygame.mouse.get_pos()
        self.clicked = pygame.mouse.get_pressed()
        if self.clicked == (1, 0, 0):
            canvas_x_min = self.output.base.canvas_x
            canvas_x_max = self.output.base.canvas_x + self.output.base.canvas_w
            canvas_y_min = self.output.base.canvas_y
            canvas_y_max = self.output.base.canvas_y + self.output.base.canvas_h
            if canvas_x_min < [self.mouse][0][0] < canvas_x_max \
                    and canvas_y_min < [self.mouse][0][1] < canvas_y_max:  # Inside the canvas
                mouseCOD = [self.mouse]
                self.draw_list.append([self.mouse, self.paint_data.color, int(self.paint_data.b_size)])
                self.blit(mouseCOD)

        if self.undo_mode:
            self.undo()

    def perform_functions(self):
        self.blit_default()

        if self.selected is not None:
            if self.selected.being_clicked:
                if self.selected.name == 'Brush Size +' and self.selected.name != 'Pencil':
                    self.paint_data.b_size += 0.1

                elif self.selected.name == 'Brush Size -' and self.selected.name != 'Pencil':
                    if self.paint_data.b_size > 0:
                        self.paint_data.b_size -= 0.1

                if self.selected.name == 'Lighten Brush':
                    if self.paint_data.b_darkness < 200:
                        self.paint_data.b_darkness += 1
                        self.paint_data.set_color()

                elif self.selected.name == 'Darken Brush':
                    if self.paint_data.b_darkness > -200:
                        self.paint_data.b_darkness -= 1
                        self.paint_data.set_color()

                elif self.selected.name == 'Pencil':
                    self.paint_data.color = Colors.silver
                    self.paint_data.b_size = 2

                if self.selected.name == 'Brush':
                    self.paint_data.color = Colors.red
                    self.paint_data.b_size = 10

                elif self.selected.name == 'Eraser':
                    self.paint_data.color = self.output.canvas_color

                elif self.selected.name == 'Clear':
                    self.paint_data.b_size = 10
                    self.output.clear_canvas()
                    self.output.blit_canvas()
                    self.draw_list = []

    def blit_default(self):  # Blitting stuff like brushsize
        message_to_screen(self.output.base.window, "Shade : " + str(int(self.paint_data.b_darkness * -1)),
                          Colors.coolyellow, 80, 455, 20)  # BrushDarkness
        message_to_screen(self.output.base.window, "Size : " + str(int(self.paint_data.b_size)), Colors.coolgreen, 80,
                          515, 20)  # BrushSize

        pygame.draw.circle(self.output.base.window, Colors.black, (135, 630),
                           int(self.paint_data.b_size) + 2)  # Outline
        pygame.draw.circle(self.output.base.window, self.paint_data.color, (135, 630),
                           int(self.paint_data.b_size))  # How the brushlooks

    def blit(self, cood):
        canvas_cood = (cood[0][0] - self.output.base.canvas_x, cood[0][1] - self.output.base.canvas_y)
        pygame.draw.circle(self.output.canvas, self.paint_data.color, canvas_cood, int(self.paint_data.b_size))
        self.output.blit_canvas()

    def undo(self):
        if len(self.draw_list) > 0:
            self.draw_list.pop()

        self.output.clear_canvas()

        for i in self.draw_list:
            canvas_cood = (i[0][0] - self.output.base.canvas_x, i[0][1] - self.output.base.canvas_y)
            pygame.draw.circle(self.output.canvas, i[1], canvas_cood, i[2])

        self.output.blit_canvas()

    def clean_list(self):
        self.cleaned_list = []

        # Removing Duplicates
        for i in self.draw_list:
            if i not in self.cleaned_list:
                self.cleaned_list.append(i)

        print(len(self.draw_list))
        print(len(self.cleaned_list))


class MyButton:
    def __init__(self, output, painting, image, x, y, size, grow, name='NONE', detail='Description',
                 color=Colors.coolblue, function=None):
        self.output = output
        self.painting = painting

        self.file = pygame.image.load(image)
        self.size = size
        self.grow = grow
        self.color = color
        self.name = name
        self.detail = [detail]

        self.image = pygame.transform.scale(pygame.image.load(image), (self.size, self.size))
        self.image.set_alpha(25)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.function = function
        self.being_clicked = False

        self.mouse = None
        self.clicked = None

    def display_button(self):
        self.mouse = pygame.mouse.get_pos()
        self.clicked = pygame.mouse.get_pressed()

        if self.rect.x < self.mouse[0] < self.rect.x + self.size \
                and self.rect.y < self.mouse[1] < self.rect.y + self.size:
            self.image = pygame.transform.scale(self.file, (self.grow, self.grow))
            self.output.base.window.blit(self.image,
                                         (self.rect.x - (self.grow - self.size) * 0.5,
                                          self.rect.y - (self.grow - self.size) * 0.5))

            message_to_screen(self.output.info_box, self.name, self.color,
                              0, 0.25 * self.output.base.infobox_h, 30, True)

            self.output.set_alpha(self.output.info_box, 200)  # MAKES THE INFO BOX DARKER

            if self.clicked == (1, 0, 0):
                self.painting.selected = self
                self.being_clicked = True
            else:
                self.being_clicked = False

        else:
            self.image = pygame.transform.scale(self.file, (self.size, self.size))  # Change image to the original size
            self.output.base.window.blit(self.image, (self.rect.x, self.rect.y))  # Display the icon

            self.output.set_alpha(self.output.info_box, self.output.ialpha)  # makes the info box to the original color


class ColorButton:  # Buttons
    def __init__(self, output, painting, color, x, y, size, grow, name):
        self.output = output
        self.painting = painting

        self.size = size
        self.grow = grow
        self.color = color
        self.name = name

        self.box = pygame.Surface((self.size, self.size))
        self.box.fill(self.color)

        self.rect = self.box.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.being_clicked = False

        self.mouse = None
        self.clicked = None

    def display_color(self):
        self.mouse = pygame.mouse.get_pos()
        self.clicked = pygame.mouse.get_pressed()

        if self.rect.x < self.mouse[0] < self.rect.x + self.size \
                and self.rect.y < self.mouse[1] < self.rect.y + self.size:
            self.box = pygame.Surface((self.grow, self.grow))
            self.box.fill(self.color)

            self.output.base.window.blit(self.box,
                                         (self.rect.x - (self.grow - self.size) * 0.5,
                                          self.rect.y - (self.grow - self.size) * 0.5))

            message_to_screen(self.output.info_box, self.name, self.color,
                              0, 0.25 * self.output.base.infobox_h, 30, True)

            if self.clicked == (1, 0, 0):
                self.painting.paint_data.prime_color = self.color
                self.painting.paint_data.b_darkness = 0

                self.painting.paint_data.set_color()

                self.being_clicked = True

            else:
                self.being_clicked = False

        else:
            self.box = pygame.Surface((self.size, self.size))  # Change image to the original size
            self.box.fill(self.color)

            self.output.base.window.blit(self.box, (self.rect.x, self.rect.y))  # Display the icon
