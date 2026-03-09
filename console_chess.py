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
            while r != tr and c != tc:
                if board[r][c] != '.':
                    return False
                if step_r != 0:
                    r += step_r
                if step_c != 0:
                    c += step_c
            return True
        return False

    if p == 'b':
        if abs(dr) == abs(dc):
            if dr > 0:
                step_r = 1
            else:
                step_r = -1
            if dc > 0:
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
                step_c = 1 if tc > fc else -1
            else:
                step_r = 1 if tr > fr else -1
            
            r = fr + step_r
            c = fc + step_c
            while r != tr or c != tc:
                if board[r][c] != '.':
                    return False
                if step_r != 0:
                    r = r + step_r
                if step_c != 0:
                    c = c + step_c
            return True
        
        if abs(dr) == abs(dc):
            step_r = 1 if dr > 0 else -1
            step_c = 1 if dc > 0 else -1
            r = fr + step_r
            c = fc + step_c
            while r != tr and c != tc:
                if board[r][c] != '.':
                    return False
                r = r + step_r
                c = c + step_c
            return True
        return False

    if p == 'k':
        return abs(dr) <= 1 and abs(dc) <= 1

    return False

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
                # проверка не пдставим ли мы короля
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

def make_move(from_row, from_col, to_row, to_col):
    global current, game_over

    piece = board[from_row][from_col]
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

# основной цикл игры
print('\n' + '='*50)
print('Формат ввода: фигура клетка')
print('Например: конь e4, пешка d5, ладья a1')
print('Коротко: к e4, п d5, л a1, ф c4, с f3, кр g1')
print('Пешки могут превращаться в любую фигуру на последней линии!')
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

    # разбираем ввод
    parts = move_text.split() 
    if len(parts) != 2:
        print('❌ Нужно: фигура клетка (например: конь e4)')
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
        print(f'❌ Несколько фигур могут пойти на {target}. Используй точные координаты (например: {piece_name} {target} уточни)')
        print('   Или используй формат: a2a4 для точного хода')
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

