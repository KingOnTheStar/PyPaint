from Widgets import *


def display_list(output, painting):
    print("Executed")
    # clear Screen
    output.blit_background()

    # Draw
    for i in painting.cleaned_list:
        pygame.draw.circle(output.base.window, i[1], i[0], i[2])


def paint_loop(output, painting, buttons, color_buttons):
    output.blit_background()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                full_quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    full_quit()

                if event.key == pygame.K_RETURN:
                    painting.cleanlist()
                    print(painting.cleaned_list)

                if event.key == pygame.K_BACKSPACE:
                    painting.undo_mode = True

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_BACKSPACE:
                    painting.undo_mode = False

        # Draw Everything

        # output.blitBackground()
        output.blit_menu()

        for button in buttons:
            button.display_button()

        for button in color_buttons:
            button.display_color()

        # Update Function
        painting.perform_functions()
        painting.get_position()

        # Logic Testing

        # Delay framerate
        output.base.clock.tick(output.base.FPS)

        # Update Screen
        pygame.display.update()
