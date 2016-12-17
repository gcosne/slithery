#!/usr/bin/python

class Game:
    # curses coordinates are in the format {y, x}
    length = config['size'][0]
    height = config['size'][0]
    x_center = dim[1]/2
    y_center = dim[0]/2

    # Top left, top right, bottom left, bottom right
    corners = {'TOP_LEFT': (y_center-y/2+2, x_center-x/2+1),
               'TOP_RIGHT': (y_center-y/2+2, x_center+x/2),
               'BOTTOM_LEFT': (y_center+y/2+2, x_center-x/2+1),
               'BOTTOM_RIGHT': (y_center+y/2+2, x_center+x/2)}

    STATE_MENU = 0
    STATE_GAME = 1
    current_state = STATE_MENU

    MENU_SINGLEPLAYER = 0
    MENU_MULTIPLAYER = 1
    current_menu = MENU_SINGLEPLAYER

    board = []
    ITEM_EMPTY = 0
    ITEM_FOOD = 1
    ITEM_SNAKE_HEAD = 2
    ITEM_SNAKE_BODY = 3
    ITEM_SNAKE_TAIL = 4

    DIRECTION_UP = 0
    DIRECTION_DOWN = 1
    DIRECTION_LEFT = 2
    DIRECTION_RIGHT = 3
    current_direction = None


    def draw_menu_items():
        screen.addstr(y_center-2, x_center-4, 'slithery', curses.A_BOLD)
        screen.addstr(y_center, x_center-4, '1-player',
                curses.A_BOLD if current_menu == MENU_SINGLEPLAYER else curses.A_NORMAL)
        screen.addstr(y_center+2, x_center-6, 'Multi-player',
                curses.A_BOLD if current_menu == MENU_MULTIPLAYER else curses.A_NORMAL)


    def draw_borders():
        screen.addstr(corners['TOP_LEFT'][0]-1, corners['TOP_LEFT'][1], config['borders'][2]*x)
        screen.addstr(corners['BOTTOM_LEFT'][0], corners['BOTTOM_LEFT'][1], config['borders'][3]*x)
        for i in range(corners['TOP_LEFT'][0], corners['BOTTOM_LEFT'][0]):
            screen.addstr(i, corners['TOP_LEFT'][1]-1, config['borders'][0])
            screen.addstr(i, corners['TOP_RIGHT'][1]+1, config['borders'][1])


    def board_replace(coords, value):
        '''
        Replace the item at coords with the specified value
        '''
        board[coords[0]][coords[1]] = value


    def where_is_snake():
        '''
        Output a dictionary of all coordinates covered by snake, categorized
        into either head, body or tail
        '''
        snake_head = []
        snake_body = []
        snake_tail = []

        for i in range(height):
            for j in range(width):
                if board[i][j] == ITEM_SNAKE_HEAD:
                    snake_head.append((i, j))
                elif board[i][j] == ITEM_SNAKE_BODY:
                    snake_body.append((i, j))
                elif board[i][j] == ITEM_SNAKE_TAIL:
                    snake_body.append((i, j))
            
        return {'HEAD': snake_head, 'BODY': snake_body, 'TAIL': snake_tail}


    def spawn_food():
        snake = where_is_snake()
        

        while True:
            food_spawn = (random.randint(height),
                          random.randint(length))

            if food_spawn not in snake.values():
                return food_spawn


    def init_spawn():
        '''
        Spawn the snake and food at a random location, as well as specify a starting direction
        '''
        snake_spawn = (random.randint(height/4, height-height/4), 
                       random.randint(length/4, length-length/4))

        board_replace(snake_spawn, ITEM_SNAKE_HEAD)
        board_replace(spawn_food(), ITEM_FOOD)

        # TODO: Make this more Pythonic?
        current_direction = random.randint(DIRECTION_UP, DIRECTION_RIGHT)


    def init_singleplayer_board():
        for i in range(height):
            row = []
            for j in range(width):
                row.append(ITEM_EMPTY)
            board.append(row)

        init_spawn()


    def merge_row_to_string(row):
        items_text = {ITEM_EMPTY: '^',
                      ITEM_SNAKE_HEAD: 'O',
                      ITEM_SNAKE_BODY: 'O',
                      ITEM_SNAKE_TAIL: 'O',
                      ITEM_FOOD: '*'}
        string = ""

        for i in row:
            string += items_text[i]
        return string


    def draw_board():
        for index, row in enumerate(board):
            screen.addstr(corners['TOP_LEFT'][0]+index, corners['TOP_LEFT'][1], 
                          merge_row_to_string(row))


    def coord_add(initial, arg):
        return (initial[i] + arg[i] for i in range(2))


    def iteration(char):
        direction_keymap = {'w': DIRECTION_UP,
                            's': DIRECTION_DOWN,
                            'a': DIRECTION_LEFT,
                            'd': DIRECTION_RIGHT}

        # The x and y values to move the snake's head
        coord_diff = {DIRECTION_UP: (-1, 0),
                             DIRECTION_DOWN: (1, 0),
                             DIRECTION_LEFT: (0, -1),
                             DIRECTION_RIGHT: (0, 1)}

        char_lower = str.lower(char)
        current_direction = direction_keymap[char]
        new_head = coord_add(snake_head, coord_diff[current_direction])

        # Out of borders
        if new_head[0] < corners['TOP_LEFT'][0] or new_head[0] > corners['BOTTOM_LEFT'][0] \
                or new_head[1] < corners['TOP_LEFT'][1] or new_head[0] > corners['TOP_RIGHT'][1]:
            return 1
        else:
            snake_head = new_head

            if snake_head == 0:
                pass


