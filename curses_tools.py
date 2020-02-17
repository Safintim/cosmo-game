SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258


def read_controls(canvas):
    """Read keys pressed and returns tuple witl controls state."""

    rows_direction = columns_direction = 0
    space_pressed = False

    while True:
        pressed_key_code = canvas.getch()

        if pressed_key_code == -1:
            # https://docs.python.org/3/library/curses.html#curses.window.getch
            break

        if pressed_key_code == UP_KEY_CODE:
            rows_direction = -2

        if pressed_key_code == DOWN_KEY_CODE:
            rows_direction = 2

        if pressed_key_code == RIGHT_KEY_CODE:
            columns_direction = 2

        if pressed_key_code == LEFT_KEY_CODE:
            columns_direction = -2

        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True

    return rows_direction, columns_direction, space_pressed


def draw_frame(canvas, start_row, start_column, text, negative=False):
    """Draw multiline text fragment on canvas. Erase text instead of drawing if negative=True is specified."""

    rows_number, columns_number = canvas.getmaxyx()

    for row, line in enumerate(text.splitlines(), round(start_row)):
        if row < 0:
            continue

        if row >= rows_number:
            break

        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue

            if column >= columns_number:
                break

            if symbol == ' ':
                continue

            # Check that current position it is not in a lower right corner of the window
            # Curses will raise exception in that case. Don`t ask why…
            # https://docs.python.org/3/library/curses.html#curses.window.addch
            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = symbol if not negative else ' '
            canvas.addch(row, column, symbol)


def get_frame_size(text):
    """Calculate size of multiline text fragment. Returns pair (rows number, colums number)"""

    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])
    return rows, columns


def read_file(path):
    with open(path) as f:
        return f.read()


def is_frame_go_out_of_height(frame_rows, height, row):
    return frame_rows < row < height


def is_frame_go_out_of_width(frame_cols, width, col):
    return frame_cols < col < width


def is_frame_go_out_of_bounds(canvas, frame):
    frame_rows, frame_cols = get_frame_size(frame)
    height_canvas, width_canvas = canvas.getmaxyx()

    def inner(start_row, start_column, rows_direction, columns_direction):
        new_row = start_row + rows_direction + frame_rows
        new_col = start_column + columns_direction + frame_cols
        return (is_frame_go_out_of_height(frame_rows, height_canvas, new_row)
                and is_frame_go_out_of_width(frame_cols, width_canvas, new_col))
    return inner
