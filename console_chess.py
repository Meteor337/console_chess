from random import randint

# доска
board = [
    ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜'],
    ['♟', '♟', '♟', '♟', '♟', '♟', '♟', '♟'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['♙', '♙', '♙', '♙', '♙', '♙', '♙', '♙'],
    ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖'],
]

print('Добро пожаловать в Консольные Шахматы')
player1 = input('Введите имя первого игрока: ')
player2 = input('Введите имя второго игрока: ')

# рандомное определение цвета каждого из игроков
if randint(0, 1) == 0:
    white_player = player1
    black_player = player2
    print(f'\n{player1} играет БЕЛЫМИ(♔♕♖♗♘♙)')
    print(f'{player2} играет ЧЕРНЫМИ(♚♛♜♝♞♟)')
else:
    white_player = player2
    black_player = player1
    print(f'\n{player2} играет БЕЛЫМИ(♔♕♖♗♘♙)')
    print(f'{player1} играет ЧЕРНЫМИ(♚♛♜♝♞♟)')

current = 0  # 0 - белые, 1 - черные
game_over = False

# отслеживаем, двигались ли король и ладьи (для рокировки)
white_king_moved = False
white_rook_a_moved = False
white_rook_h_moved = False
black_king_moved = False
black_rook_a_moved = False
black_rook_h_moved = False

# соответствие русских названий юникод-символам
def piece_name_to_unicode(name, color):
    name = name.lower()
    if color == 0:
        if name == 'пешка' or name == 'п':
            return '♙'
        elif name == 'конь' or name == 'к':
            return '♘'
        elif name == 'слон' or name == 'с':
            return '♗'
        elif name == 'ладья' or name == 'л':
            return '♖'
        elif name == 'ферзь' or name == 'ф':
            return '♕'
        elif name == 'король' or name == 'кр':
            return '♔'
    else:
        if name == 'пешка' or name == 'п':
            return '♟'
        elif name == 'конь' or name == 'к':
            return '♞'
        elif name == 'слон' or name == 'с':
            return '♝'
        elif name == 'ладья' or name == 'л':
            return '♜'
        elif name == 'ферзь' or name == 'ф':
            return '♛'
        elif name == 'король' or name == 'кр':
            return '♚'
    return None

def unicode_to_piece_name(uni):
    if uni == '♙' or uni == '♟':
        return 'пешка'
    elif uni == '♘' or uni == '♞':
        return 'конь'
    elif uni == '♗' or uni == '♝':
        return 'слон'
    elif uni == '♖' or uni == '♜':
        return 'ладья'
    elif uni == '♕' or uni == '♛':
        return 'ферзь'
    elif uni == '♔' or uni == '♚':
        return 'король'
    return ''

def get_promotion_choice(color):
    print('\n ПЕШКА ДОШЛА ДО КРАЯ! ')
    print('Выбери фигуру для превращения: ')
    if color == 0:
        print('1 - Ферзь (♕)')
        print('2 - Ладья (♖)')
        print('3 - Слон (♗)')
        print('4 - Конь (♘)')
    else:
        print('1 - Ферзь (♛)')
        print('2 - Ладья (♜)')
        print('3 - Слон (♝)')
        print('4 - Конь (♞)')

    while True:
        choice = input('Твой выбор (1-4): ').strip()
        if color == 0:
            if choice == '1':
                return '♕'
            elif choice == '2':
                return '♖'
            elif choice == '3':
                return '♗'
            elif choice == '4':
                return '♘'
        else:
            if choice == '1':
                return '♛'
            elif choice == '2':
                return '♜'
            elif choice == '3':
                return '♝'
            elif choice == '4':
                return '♞'
        print('Неверный выбор! Попробуй снова.')

def is_white(piece):
    return piece in ['♙', '♘', '♗', '♖', '♕', '♔']


def is_black(piece):
    return piece in ['♟', '♞', '♝', '♜', '♛', '♚']


def get_current_player_name():
    if current == 0:
        return white_player
    else:
        return black_player


def get_current_color_name():
    if current == 0:
        return 'БЕЛЫЕ (♔♕♖♗♘♙)'
    else:
        return 'ЧЁРНЫЕ (♚♛♜♝♞♟)'


def col_to_index(col_letter):
    if col_letter == 'a':
        return 0
    elif col_letter == 'b':
        return 1
    elif col_letter == 'c':
        return 2
    elif col_letter == 'd':
        return 3
    elif col_letter == 'e':
        return 4
    elif col_letter == 'f':
        return 5
    elif col_letter == 'g':
        return 6
    elif col_letter == 'h':
        return 7
    return -1

def index_to_col(index):
    cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    if 0 <= index <= 7:
        return cols[index]
    return ''

def print_board():
    print('\n    a   b   c   d   e   f   g   h')
    print('  ┌───┬───┬───┬───┬───┬───┬───┬───┐')
    for i in range(8):
        print(8 - i, end=' │')
        for j in range(8):
            print(f' {board[i][j]} ', end='│')
        print(f' {8 - i}')
        if i < 7:
            print('  ├───┼───┼───┼───┼───┼───┼───┼───┤')
    print('  └───┴───┴───┴───┴───┴───┴───┴───┘')
    print('    a   b   c   d   e   f   g   h\n')


def get_king_pos(color):
    if color == 0:
        king = '♔'
    else:
        king = '♚'
    for i in range(8):
        for j in range(8):
            if board[i][j] == king:
                return [i, j]
    return None

def can_atack(from_pos, to_pos, piece):
    fr = from_pos[0]
    fc = from_pos[1]
    tr = to_pos[0]
    tc = to_pos[1]

    # для правильной логики используем буквенные обозначения
    p_map = {'♙':'P', '♘':'N', '♗':'B', '♖':'R', '♕':'Q', '♔':'K',
             '♟':'p', '♞':'n', '♝':'b', '♜':'r', '♛':'q', '♚':'k'}
    piece_letter = p_map.get(piece, '.')
    p = piece_letter.lower()

    if p == 'p':
        if is_white(piece):
            return (tr == fr - 1) and (tc == fc + 1 or tc == fc - 1)
        else:
            return (tr == fr + 1) and (tc == fc + 1 or tc == fc - 1)

    if p == 'n':
        dr = abs(tr - fr)
        dc = abs(tc - fc)
        return (dr == 2 and dc == 1) or (dr == 1 and dc == 2)

    if p == 'r':
        if fr == tr or fc == tc:
            step_r = 0
            step_c = 0
            if fr == tr:
                if tc > fc:
                    step_c = 1
                else:
                    step_c = -1
            else:
                if tr > fr:
                    step_r = 1
                else:
                    step_r = -1

            r = fr + step_r
            c = fc + step_c
            while r != tr or c != tc:
                if board[r][c] != '.':
                    return False
                if step_r != 0:
                    r += step_r
                if step_c != 0:
                    c += step_c
            return True
        return False

    if p == 'b':
        if abs(tr - fr) == abs(tc - fc):
            if tr > fr:
                step_r = 1
            else:
                step_r = -1
            if tc > fc:
                step_c = 1
            else:
                step_c = -1
            r = fr + step_r
            c = fc + step_c
            while r != tr and c != tc:
                if board[r][c] != '.':
                    return False
                r += step_r
                c += step_c
            return True
        return False

    if p == 'q':
        if fr == tr or fc == tc:
            step_r = 0
            step_c = 0
            if fr == tr:
                if tc > fc:
                    step_c = 1
                else:
                    step_c = -1
            else:
                if tr > fr:
                    step_r = 1
                else:
                    step_r = -1
            
            r = fr + step_r
            c = fc + step_c
            while r != tr or c != tc:
                if board[r][c] != '.':
                    return False
                if step_r != 0:
                    r += step_r
                if step_c != 0:
                    c += step_c
            return True

        if abs(tr - fr) == abs(tc - fc):
            if tr > fr:
                step_r = 1
            else:
                step_r = -1
            if tc > fc:
                step_c = 1
            else:
                step_c = -1
            r = fr + step_r
            c = fc + step_c
            while r != tr and c != tc:
                if board[r][c] != '.':
                    return False
                r += step_r
                c += step_c
            return True
        return False

    if p == 'k':
        return abs(tr - fr) <= 1 and abs(tc - fc) <= 1

    return False

def is_under_atack(pos, color):
    row = pos[0]
    col = pos[1]

    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece == '.':
                continue
            if color == 0 and is_white(piece):
                continue
            if color == 1 and is_black(piece):
                continue
            if can_atack([i, j], [row, col], piece):
                return True
    return False

def is_check(color):
    king_pos = get_king_pos(color)
    if king_pos is None:
        return False
    return is_under_atack(king_pos, color)

def can_castle(color, side):
    global white_king_moved, white_rook_a_moved, white_rook_h_moved
    global black_king_moved, black_rook_a_moved, black_rook_h_moved
    
    if is_check(color):
        return False
    
    if color == 0:  # белые
        if white_king_moved:
            return False
        if side == 'kingside':  # короткая рокировка (0-0)
            if white_rook_h_moved:
                return False
            # клетки между королем и ладьей должны быть пусты
            if board[7][5] != '.' or board[7][6] != '.':
                return False
            # король не должен проходить через битое поле
            if is_under_atack([7, 5], color) or is_under_atack([7, 6], color):
                return False
            return True
        elif side == 'queenside':  # длинная рокировка (0-0-0)
            if white_rook_a_moved:
                return False
            # клетки между королем и ладьей должны быть пусты
            if board[7][1] != '.' or board[7][2] != '.' or board[7][3] != '.':
                return False
            # король не должен проходить через битое поле
            if is_under_atack([7, 3], color) or is_under_atack([7, 2], color):
                return False
            return True
    else:  # черные
        if black_king_moved:
            return False
        if side == 'kingside':  # короткая рокировка (0-0)
            if black_rook_h_moved:
                return False
            if board[0][5] != '.' or board[0][6] != '.':
                return False
            if is_under_atack([0, 5], color) or is_under_atack([0, 6], color):
                return False
            return True
        elif side == 'queenside':  # длинная рокировка (0-0-0)
            if black_rook_a_moved:
                return False
            if board[0][1] != '.' or board[0][2] != '.' or board[0][3] != '.':
                return False
            if is_under_atack([0, 3], color) or is_under_atack([0, 2], color):
                return False
            return True
    return False

def can_move(from_pos, to_pos, piece):
    fr = from_pos[0]
    fc = from_pos[1]
    tr = to_pos[0]
    tc = to_pos[1]

    dr = tr - fr
    dc = tc - fc

    p_map = {'♙':'P','♘':'N','♗':'B','♖':'R','♕':'Q','♔':'K',
             '♟':'p','♞':'n','♝':'b','♜':'r','♛':'q','♚':'k'}
    piece_letter = p_map.get(piece, '.')
    p = piece_letter.lower()

    if p == 'p':
        target = board[tr][tc]
        if is_white(piece):
            if dr == -1 and dc == 0 and target == '.':
                return True
            if fr == 6 and dr == -2 and dc == 0 and board[5][fc] == '.' and target == '.':
                return True
            if dr == -1 and abs(dc) == 1 and target != '.' and is_black(target):
                return True
        else:
            if dr == 1 and dc == 0 and target == '.':
                return True
            if fr == 1 and dr == 2 and dc == 0 and board[2][fc] == '.' and target == '.':
                return True
            if dr == 1 and abs(dc) == 1 and target != '.' and is_white(target):
                return True
        return False

    if p == 'n':
        return (abs(dr) == 2 and abs(dc) == 1) or (abs(dr) == 1 and abs(dc) == 2)

    if p == 'r':
        if fr == tr or fc == tc:
            step_r = 0 if fr == tr else (1 if tr > fr else -1)
            step_c = 0 if fc == tc else (1 if tc > fc else -1)
            
            r = fr + step_r
            c = fc + step_c
            while r != tr or c != tc:
                if board[r][c] != '.':
                    return False
                r += step_r
                c += step_c
            return True
        return False

    if p == 'b':
        if abs(dr) == abs(dc):
            step_r = 1 if dr > 0 else -1
            step_c = 1 if dc > 0 else -1
            r = fr + step_r
            c = fc + step_c
            while r != tr and c != tc:
                if board[r][c] != '.':
                    return False
                r += step_r
                c += step_c
            return True
        return False

    if p == 'q':
        if fr == tr or fc == tc:
            step_r = 0 if fr == tr else (1 if tr > fr else -1)
            step_c = 0 if fc == tc else (1 if tc > fc else -1)
            
            r = fr + step_r
            c = fc + step_c
            while r != tr or c != tc:
                if board[r][c] != '.':
                    return False
                r += step_r
                c += step_c
            return True
        
        if abs(dr) == abs(dc):
            step_r = 1 if dr > 0 else -1
            step_c = 1 if dc > 0 else -1
            r = fr + step_r
            c = fc + step_c
            while r != tr and c != tc:
                if board[r][c] != '.':
                    return False
                r += step_r
                c += step_c
            return True
        return False

    if p == 'k':
        return abs(dr) <= 1 and abs(dc) <= 1

    return False

def parse_square(square):
    """Преобразует строку типа 'e2' в координаты (row, col)"""
    if len(square) != 2:
        return None
    col = col_to_index(square[0])
    if col == -1:
        return None
    try:
        row = 8 - int(square[1])
        if row < 0 or row > 7:
            return None
        return [row, col]
    except ValueError:
        return None

def parse_move(move_text):
    """Парсит ход в формате 'e2e4' или '0-0', '0-0-0'"""
    move_text = move_text.strip().lower()
    
    # Проверка на рокировку
    if move_text == '0-0' or move_text == 'o-o':
        return ('castle', 'kingside')
    if move_text == '0-0-0' or move_text == 'o-o-o':
        return ('castle', 'queenside')
    
    # Проверка формата e2e4
    if len(move_text) == 4:
        from_sq = move_text[0:2]
        to_sq = move_text[2:4]
        
        from_pos = parse_square(from_sq)
        to_pos = parse_square(to_sq)
        
        if from_pos and to_pos:
            return ('move', from_pos, to_pos)
    
    return None

def find_piece_by_position(from_row, from_col, color):
    """Проверяет, что на указанной позиции стоит фигура нужного цвета"""
    if from_row < 0 or from_row > 7 or from_col < 0 or from_col > 7:
        return None
    
    piece = board[from_row][from_col]
    if piece == '.':
        return None
    
    if color == 0 and not is_white(piece):
        return None
    if color == 1 and not is_black(piece):
        return None
    
    return piece

def update_castling_flags(piece, from_row, from_col):
    """Обновляет флаги рокировки после хода"""
    global white_king_moved, white_rook_a_moved, white_rook_h_moved
    global black_king_moved, black_rook_a_moved, black_rook_h_moved
    
    if piece == '♔':  # белый король
        white_king_moved = True
    elif piece == '♚':  # черный король
        black_king_moved = True
    elif piece == '♖':  # белая ладья
        if from_row == 7 and from_col == 0:
            white_rook_a_moved = True
        elif from_row == 7 and from_col == 7:
            white_rook_h_moved = True
    elif piece == '♜':  # черная ладья
        if from_row == 0 and from_col == 0:
            black_rook_a_moved = True
        elif from_row == 0 and from_col == 7:
            black_rook_h_moved = True

def make_castle(color, side):
    """Выполняет рокировку"""
    global white_king_moved, white_rook_a_moved, white_rook_h_moved
    global black_king_moved, black_rook_a_moved, black_rook_h_moved
    
    if color == 0:  # белые
        if side == 'kingside':  # 0-0
            # перемещаем короля
            board[7][6] = board[7][4]
            board[7][4] = '.'
            # перемещаем ладью
            board[7][5] = board[7][7]
            board[7][7] = '.'
            white_king_moved = True
            white_rook_h_moved = True
            print(" Белые сделали короткую рокировку (0-0)!")
        else:  # queenside
            board[7][2] = board[7][4]
            board[7][4] = '.'
            board[7][3] = board[7][0]
            board[7][0] = '.'
            white_king_moved = True
            white_rook_a_moved = True
            print(" Белые сделали длинную рокировку (0-0-0)!")
    else:  # черные
        if side == 'kingside':  # 0-0
            board[0][6] = board[0][4]
            board[0][4] = '.'
            board[0][5] = board[0][7]
            board[0][7] = '.'
            black_king_moved = True
            black_rook_h_moved = True
            print(" Черные сделали короткую рокировку (0-0)!")
        else:  # queenside
            board[0][2] = board[0][4]
            board[0][4] = '.'
            board[0][3] = board[0][0]
            board[0][0] = '.'
            black_king_moved = True
            black_rook_a_moved = True
            print(" Черные сделали длинную рокировку (0-0-0)!")

def make_move(from_row, from_col, to_row, to_col):
    global current, game_over
    global white_king_moved, white_rook_a_moved, white_rook_h_moved
    global black_king_moved, black_rook_a_moved, black_rook_h_moved

    piece = board[from_row][from_col]
    
    # Обновляем флаги рокировки
    update_castling_flags(piece, from_row, from_col)
    
    # Выполняем ход
    board[to_row][to_col] = piece
    board[from_row][from_col] = '.'

    # проверка превращения пешки
    if check_promotion(to_row, to_col, current):
        new_piece = get_promotion_choice(current)
        board[to_row][to_col] = new_piece
        print(f' Пешка превратилась в {unicode_to_piece_name(new_piece)}! ')

    state = check_game_state()
    if state != 0:
        game_over = True
        return

    if current == 0:
        current = 1
    else:
        current = 0

# функция которая ищет фигуру, которая может пойти на target клетку
def find_piece(piece_unicode, target_row, target_col, color):
    possible_pieces = []

    for i in range(8):
        for j in range(8):
            p = board[i][j]
            if p == '.':
                continue
            if color == 0 and not is_white(p):
                continue
            if color == 1 and not is_black(p):
                continue
            if p != piece_unicode:
                continue

            if can_move([i, j], [target_row, target_col], p):
                # проверка не подставим ли мы короля
                temp = board[target_row][target_col]
                board[target_row][target_col] = board[i][j]
                board[i][j] = '.'

                if not is_check(color):
                    possible_pieces.append([i, j])

                board[i][j] = board[target_row][target_col]
                board[target_row][target_col] = temp

    return possible_pieces

def get_all_moves(color):
    moves = []
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece == '.':
                continue
            if color == 0 and not is_white(piece):
                continue
            if color == 1 and not is_black(piece):
                continue

            for ti in range(8):
                for tj in range(8):
                    if not can_move([i, j], [ti, tj], piece):
                        continue

                    temp = board[ti][tj]
                    board[ti][tj] = board[i][j]
                    board[i][j] = '.'

                    if not is_check(color):
                        moves.append([i, j, ti, tj])

                    board[i][j] = board[ti][tj]
                    board[ti][tj] = temp

    return moves

# функция, проверяющая нужно ли превратить пешку
def check_promotion(row, col, color):
    piece = board[row][col]
    if color == 0 and piece == '♙' and row == 0:
        return True
    if color == 1 and piece == '♟' and row == 7:
        return True
    return False

def check_game_state():
    global game_over

    white_king = False
    black_king = False
    for i in range(8):
        for j in range(8):
            if board[i][j] == '♔':
                white_king = True
            if board[i][j] == '♚':
                black_king = True

    if not white_king:
        print(f'\n♛ {black_player} (ЧЁРНЫЕ) ПОБЕДИЛ! ♛')
        return 2
    if not black_king:
        print(f'\n♔ {white_player} (БЕЛЫЕ) ПОБЕДИЛ! ♔')
        return 1

    moves = get_all_moves(current)

    if len(moves) == 0:
        if is_check(current):
            if current == 0:
                print(f'\n♛ МАТ! {black_player} (ЧЁРНЫЕ) ПОБЕДИЛ! ♛')
                return 2
            else:
                print(f'\n♔ МАТ! {white_player} (БЕЛЫЕ) ПОБЕДИЛ! ♔')
                return 1
        else:
            print('\n🤝 ПАТ! НИЧЬЯ! 🤝')
            return 3 

    return 0

# основной цикл игры
print('\n' + '='*50)
print('Форматы ввода:')
print('1. Координатный: e2e4, g1f3')
print('2. Рокировка: 0-0 (короткая), 0-0-0 (длинная)')
print('3. Старый формат: конь e4, пешка d5')
print('exit - выход')
print('='*50 + '\n')

while not game_over:
    print_board()

    current_name = get_current_player_name()
    current_color = get_current_color_name()
    print(f'▶ ХОДИТ: {current_name} ({current_color}) ◀')

    move_text = input('> ').strip().lower()

    if move_text == 'exit':
        print('Игра прервана')
        break

    # Пробуем распарсить как координатный ход или рокировку
    parsed = parse_move(move_text)
    
    if parsed and parsed[0] == 'castle':
        # Рокировка
        side = parsed[1]
        if can_castle(current, side):
            make_castle(current, side)
            state = check_game_state()
            if state != 0:
                game_over = True
                break
            current = 1 if current == 0 else 0
            continue
        else:
            print('❌ Рокировка невозможна!')
            input('Нажми Enter...')
            continue
    
    elif parsed and parsed[0] == 'move':
        # Координатный ход
        from_pos, to_pos = parsed[1], parsed[2]
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = find_piece_by_position(from_row, from_col, current)
        if piece is None:
            print(f'❌ На клетке {move_text[0:2]} нет вашей фигуры!')
            input('Нажми Enter...')
            continue
        
        if not can_move([from_row, from_col], [to_row, to_col], piece):
            print(f'❌ Фигура {unicode_to_piece_name(piece)} не может так ходить!')
            input('Нажми Enter...')
            continue
        
        # Проверка не подставим ли мы короля
        temp = board[to_row][to_col]
        board[to_row][to_col] = board[from_row][from_col]
        board[from_row][from_col] = '.'
        
        if is_check(current):
            print('❌ Ход оставляет вашего короля под шахом!')
            board[from_row][from_col] = board[to_row][to_col]
            board[to_row][to_col] = temp
            input('Нажми Enter...')
            continue
        
        board[from_row][from_col] = board[to_row][to_col]
        board[to_row][to_col] = temp
        
        # Делаем ход
        make_move(from_row, from_col, to_row, to_col)
        continue
    
    # Если не координатный ход и не рокировка, пробуем старый формат
    parts = move_text.split() 
    if len(parts) != 2:
        print('❌ Неверный формат. Используйте: e2e4, 0-0, или конь e4')
        input('Нажми Enter...')
        continue

    piece_name = parts[0]
    target = parts[1]

    if len(target) != 2:
        print('❌ Клетка должна быть из буквы и цифры (например: e4)')
        input('Нажми Enter...')
        continue

    # получаем юникод фигуры
    piece_unicode = piece_name_to_unicode(piece_name, current)
    if piece_unicode is None:
        print('❌ Неизвестная фигура! Используй: пешка/п, конь/к, слон/с, ладья/л, ферзь/ф, король/кр')
        input('Нажми Enter...')
        continue

    # парсим целевую клетку
    target_col = col_to_index(target[0])
    target_row = 8 - int(target[1])

    if target_col == -1:
        print('❌ Неправильная буква в клетке! Используй a-h')
        input('Нажми Enter...')
        continue
    
    if target_row < 0 or target_row > 7:
        print('❌ Неправильная цифра! Используй 1-8')
        input('Нажми Enter...')
        continue
    
    # Ищем фигуру, которая может пойти
    possible = find_piece(piece_unicode, target_row, target_col, current)
    
    if len(possible) == 0:
        print(f"❌ Нет фигуры '{unicode_to_piece_name(piece_unicode)}', которая может пойти на {target}")
        input('Нажми Enter...')
        continue
    
    if len(possible) > 1:
        print(f'❌ Несколько фигур могут пойти на {target}. Используй координатный формат (например: e2e4)')
        input('Нажми Enter...')
        continue
    
    # Делаем ход
    from_pos = possible[0]
    make_move(from_pos[0], from_pos[1], target_row, target_col)

if game_over:
    print_board()
    print('\n' + '='*40)
    print('ИГРА ОКОНЧЕНА!')
    print('='*40)
