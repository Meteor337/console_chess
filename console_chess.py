from random import randint

# === НАЧАЛЬНЫЕ НАСТРОЙКИ ===
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

# Кто каким цветом играет
if randint(0, 1) == 0:
    white_player = player1
    black_player = player2
    print(f'\n{player1} играет БЕЛЫМИ')
    print(f'{player2} играет ЧЕРНЫМИ')
else:
    white_player = player2
    black_player = player1
    print(f'\n{player2} играет БЕЛЫМИ')
    print(f'{player1} играет ЧЕРНЫМИ')

# === ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ===
current = 0  # 0 - белые, 1 - черные
game_over = False

# Для рокировки
white_king_moved = False
white_rook_a_moved = False
white_rook_h_moved = False
black_king_moved = False
black_rook_a_moved = False
black_rook_h_moved = False

# Для взятия на проходе
en_passant_target = None

# === ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ===
def is_white(piece):
    return piece in ['♙', '♘', '♗', '♖', '♕', '♔']

def is_black(piece):
    return piece in ['♟', '♞', '♝', '♜', '♛', '♚']

def get_current_player():
    return white_player if current == 0 else black_player

def col_to_index(col):
    return 'abcdefgh'.find(col)

def index_to_col(index):
    return 'abcdefgh'[index] if 0 <= index <= 7 else ''

def parse_square(square):
    """Преобразует 'e2' в [row, col]"""
    if len(square) != 2:
        return None
    col = col_to_index(square[0])
    if col == -1:
        return None
    try:
        row = 8 - int(square[1])
        return [row, col] if 0 <= row <= 7 else None
    except:
        return None

def parse_move(move):
    """Парсит ход: 'e2e4', '0-0', '0-0-0'"""
    move = move.strip().lower()
    
    if move in ['0-0', 'o-o']:
        return ('castle', 'kingside')
    if move in ['0-0-0', 'o-o-o']:
        return ('castle', 'queenside')
    
    if len(move) == 4:
        from_pos = parse_square(move[0:2])
        to_pos = parse_square(move[2:4])
        if from_pos and to_pos:
            return ('move', from_pos, to_pos)
    return None

def get_piece_at(row, col):
    return board[row][col] if 0 <= row <= 7 and 0 <= col <= 7 else None

def get_king_pos(color):
    king = '♔' if color == 0 else '♚'
    for i in range(8):
        for j in range(8):
            if board[i][j] == king:
                return [i, j]
    return None

# === ПРОВЕРКА БЕЗОПАСНОСТИ КОРОЛЯ ===
def square_under_attack(row, col, color):
    """Проверяет, атакована ли клетка фигурами противника"""
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece == '.':
                continue
            if color == 0 and is_white(piece):
                continue
            if color == 1 and is_black(piece):
                continue
            if can_attack(i, j, row, col, piece):
                return True
    return False

def is_check(color):
    king = get_king_pos(color)
    return square_under_attack(king[0], king[1], color) if king else False

def move_leaves_king_in_check(from_row, from_col, to_row, to_col, color):
    """Проверяет, не подставит ли ход короля под шах"""
    # Сохраняем текущее состояние
    piece = board[from_row][from_col]
    target = board[to_row][to_col]
    
    # Пробуем сделать ход
    board[to_row][to_col] = piece
    board[from_row][from_col] = '.'
    
    # Проверяем, остался ли король под шахом
    in_check = is_check(color)
    
    # Возвращаем всё обратно
    board[from_row][from_col] = piece
    board[to_row][to_col] = target
    
    return in_check

# === ПРАВИЛА ХОДОВ ФИГУР ===
def can_attack(from_row, from_col, to_row, to_col, piece):
    """Может ли фигура атаковать клетку (без проверки пути)"""
    dr = to_row - from_row
    dc = to_col - from_col
    
    if piece in ['♙', '♟']:  # пешка
        if is_white(piece):
            return dr == -1 and abs(dc) == 1
        else:
            return dr == 1 and abs(dc) == 1
    
    if piece in ['♘', '♞']:  # конь
        return (abs(dr) == 2 and abs(dc) == 1) or (abs(dr) == 1 and abs(dc) == 2)
    
    if piece in ['♗', '♝']:  # слон
        return abs(dr) == abs(dc)
    
    if piece in ['♖', '♜']:  # ладья
        return dr == 0 or dc == 0
    
    if piece in ['♕', '♛']:  # ферзь
        return dr == 0 or dc == 0 or abs(dr) == abs(dc)
    
    if piece in ['♔', '♚']:  # король
        return abs(dr) <= 1 and abs(dc) <= 1
    
    return False

def path_is_clear(from_row, from_col, to_row, to_col):
    """Проверяет, нет ли фигур на пути (кроме коня)"""
    dr = to_row - from_row
    dc = to_col - from_col
    
    # Коню всё равно на фигуры на пути
    if (abs(dr) == 2 and abs(dc) == 1) or (abs(dr) == 1 and abs(dc) == 2):
        return True
    
    # Определяем шаг
    step_r = 0 if dr == 0 else (1 if dr > 0 else -1)
    step_c = 0 if dc == 0 else (1 if dc > 0 else -1)
    
    r = from_row + step_r
    c = from_col + step_c
    
    # Проверяем каждую клетку на пути
    while r != to_row or c != to_col:
        if board[r][c] != '.':
            return False
        r += step_r
        c += step_c
    
    return True

def can_move_pawn(from_row, from_col, to_row, to_col, piece):
    """Проверка хода пешки"""
    dr = to_row - from_row
    dc = to_col - from_col
    target = board[to_row][to_col]
    
    if is_white(piece):
        # Ход вперед
        if dc == 0 and target == '.':
            if dr == -1:
                return True
            if from_row == 6 and dr == -2 and board[5][from_col] == '.':
                return True
        # Взятие
        if dr == -1 and abs(dc) == 1:
            if target != '.' and is_black(target):
                return True
            # Взятие на проходе
            if target == '.' and en_passant_target == [to_row, to_col]:
                return True
    else:
        # Ход вперед
        if dc == 0 and target == '.':
            if dr == 1:
                return True
            if from_row == 1 and dr == 2 and board[2][from_col] == '.':
                return True
        # Взятие
        if dr == 1 and abs(dc) == 1:
            if target != '.' and is_white(target):
                return True
            # Взятие на проходе
            if target == '.' and en_passant_target == [to_row, to_col]:
                return True
    
    return False

def can_move_piece(from_row, from_col, to_row, to_col):
    """Основная функция проверки хода"""
    piece = board[from_row][from_col]
    if piece == '.':
        return False
    
    # Специальная проверка для пешки
    if piece in ['♙', '♟']:
        return can_move_pawn(from_row, from_col, to_row, to_col, piece)
    
    # Для остальных фигур
    if not can_attack(from_row, from_col, to_row, to_col, piece):
        return False
    
    # Проверка пути (кроме коня)
    if piece not in ['♘', '♞'] and not path_is_clear(from_row, from_col, to_row, to_col):
        return False
    
    # Нельзя бить свои фигуры
    target = board[to_row][to_col]
    if target != '.':
        if (is_white(piece) and is_white(target)) or (is_black(piece) and is_black(target)):
            return False
    
    return True

# === РОКИРОВКА ===
def can_castle(color, side):
    if is_check(color):
        return False
    
    if color == 0:  # белые
        if white_king_moved:
            return False
        if side == 'kingside':
            if white_rook_h_moved:
                return False
            return (board[7][5] == '.' and board[7][6] == '.' and
                    not square_under_attack(7, 5, color) and
                    not square_under_attack(7, 6, color))
        else:  # queenside
            if white_rook_a_moved:
                return False
            return (board[7][1] == '.' and board[7][2] == '.' and board[7][3] == '.' and
                    not square_under_attack(7, 3, color) and
                    not square_under_attack(7, 2, color))
    else:  # черные
        if black_king_moved:
            return False
        if side == 'kingside':
            if black_rook_h_moved:
                return False
            return (board[0][5] == '.' and board[0][6] == '.' and
                    not square_under_attack(0, 5, color) and
                    not square_under_attack(0, 6, color))
        else:  # queenside
            if black_rook_a_moved:
                return False
            return (board[0][1] == '.' and board[0][2] == '.' and board[0][3] == '.' and
                    not square_under_attack(0, 3, color) and
                    not square_under_attack(0, 2, color))

def do_castle(color, side):
    global white_king_moved, white_rook_a_moved, white_rook_h_moved
    global black_king_moved, black_rook_a_moved, black_rook_h_moved
    global en_passant_target
    
    if color == 0:  # белые
        if side == 'kingside':
            board[7][6] = board[7][4]  # король
            board[7][5] = board[7][7]  # ладья
            board[7][4] = '.'
            board[7][7] = '.'
            white_king_moved = True
            white_rook_h_moved = True
        else:
            board[7][2] = board[7][4]  # король
            board[7][3] = board[7][0]  # ладья
            board[7][4] = '.'
            board[7][0] = '.'
            white_king_moved = True
            white_rook_a_moved = True
    else:  # черные
        if side == 'kingside':
            board[0][6] = board[0][4]  # король
            board[0][5] = board[0][7]  # ладья
            board[0][4] = '.'
            board[0][7] = '.'
            black_king_moved = True
            black_rook_h_moved = True
        else:
            board[0][2] = board[0][4]  # король
            board[0][3] = board[0][0]  # ладья
            board[0][4] = '.'
            board[0][0] = '.'
            black_king_moved = True
            black_rook_a_moved = True
    
    en_passant_target = None
    print(f"Рокировка {'0-0' if side == 'kingside' else '0-0-0'} выполнена!")

# === ПРЕВРАЩЕНИЕ ПЕШКИ ===
def check_promotion(row, col):
    piece = board[row][col]
    if piece == '♙' and row == 0:
        return True
    if piece == '♟' and row == 7:
        return True
    return False

def get_promotion_choice():
    print('\nПешка дошла до края! Выбери фигуру:')
    if current == 0:
        print('1 - Ферзь (♕)  2 - Ладья (♖)  3 - Слон (♗)  4 - Конь (♘)')
        pieces = ['♕', '♖', '♗', '♘']
    else:
        print('1 - Ферзь (♛)  2 - Ладья (♜)  3 - Слон (♝)  4 - Конь (♞)')
        pieces = ['♛', '♜', '♝', '♞']
    
    while True:
        choice = input('Твой выбор (1-4): ').strip()
        if choice in ['1', '2', '3', '4']:
            return pieces[int(choice) - 1]
        print('Неверный выбор!')

# === ВЫПОЛНЕНИЕ ХОДА ===
def make_move(from_row, from_col, to_row, to_col):
    global current, game_over, en_passant_target
    global white_king_moved, white_rook_a_moved, white_rook_h_moved
    global black_king_moved, black_rook_a_moved, black_rook_h_moved
    
    piece = board[from_row][from_col]
    
    # Обновляем флаги рокировки
    if piece == '♔':
        white_king_moved = True
    elif piece == '♚':
        black_king_moved = True
    elif piece == '♖':
        if from_row == 7 and from_col == 0:
            white_rook_a_moved = True
        elif from_row == 7 and from_col == 7:
            white_rook_h_moved = True
    elif piece == '♜':
        if from_row == 0 and from_col == 0:
            black_rook_a_moved = True
        elif from_row == 0 and from_col == 7:
            black_rook_h_moved = True
    
    # Взятие на проходе
    if piece in ['♙', '♟'] and en_passant_target and [to_row, to_col] == en_passant_target:
        if piece == '♙':
            board[to_row + 1][to_col] = '.'  # убираем черную пешку
        else:
            board[to_row - 1][to_col] = '.'  # убираем белую пешку
    
    # Делаем ход
    board[to_row][to_col] = piece
    board[from_row][from_col] = '.'
    
    # Обновляем взятие на проходе
    en_passant_target = None
    if piece in ['♙', '♟'] and abs(to_row - from_row) == 2:
        if piece == '♙':
            en_passant_target = [to_row + 1, to_col]
        else:
            en_passant_target = [to_row - 1, to_col]
    
    # Превращение пешки
    if check_promotion(to_row, to_col):
        board[to_row][to_col] = get_promotion_choice()
        print('Пешка превратилась!')
    
    # Проверка окончания игры
    result = check_game_over()
    if result != 0:
        game_over = True
        return
    
    # Смена игрока
    current = 1 if current == 0 else 0

# === ПРОВЕРКА ОКОНЧАНИЯ ИГРЫ ===
def check_game_over():
    # Проверяем, есть ли короли
    white_king = any('♔' in row for row in board)
    black_king = any('♚' in row for row in board)
    
    if not white_king:
        print(f'\n{black_player} (ЧЕРНЫЕ) ПОБЕДИЛИ!')
        return 2
    if not black_king:
        print(f'\n{white_player} (БЕЛЫЕ) ПОБЕДИЛИ!')
        return 1
    
    # Проверяем, есть ли ходы
    if not any_valid_moves(current):
        if is_check(current):
            winner = black_player if current == 0 else white_player
            print(f'\nМАТ! {winner} ПОБЕДИЛ{"А" if winner == white_player else "И"}!')
            return 2 if current == 0 else 1
        else:
            print('\nПАТ! НИЧЬЯ!')
            return 3
    
    return 0

def any_valid_moves(color):
    """Проверяет, есть ли у игрока хотя бы один возможный ход"""
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
                    if can_move_piece(i, j, ti, tj):
                        if not move_leaves_king_in_check(i, j, ti, tj, color):
                            return True
    return False

# === ОТОБРАЖЕНИЕ ДОСКИ ===
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

# === СТАРЫЙ ФОРМАТ (ДЛЯ СОВМЕСТИМОСТИ) ===
piece_names = {
    'пешка': {'♙': '♙', '♟': '♟'}, 'п': {'♙': '♙', '♟': '♟'},
    'конь': {'♘': '♘', '♞': '♞'}, 'к': {'♘': '♘', '♞': '♞'},
    'слон': {'♗': '♗', '♝': '♝'}, 'с': {'♗': '♗', '♝': '♝'},
    'ладья': {'♖': '♖', '♜': '♜'}, 'л': {'♖': '♖', '♜': '♜'},
    'ферзь': {'♕': '♕', '♛': '♛'}, 'ф': {'♕': '♕', '♛': '♛'},
    'король': {'♔': '♔', '♚': '♚'}, 'кр': {'♔': '♔', '♚': '♚'}
}

def find_piece_by_name(piece_name, target_row, target_col, color):
    """Ищет фигуру по названию, которая может пойти на target"""
    piece_unicode = piece_names.get(piece_name.lower(), {}).get('♙' if color == 0 else '♟')
    if not piece_unicode:
        return None
    
    possible = []
    for i in range(8):
        for j in range(8):
            if board[i][j] != piece_unicode:
                continue
            if can_move_piece(i, j, target_row, target_col):
                if not move_leaves_king_in_check(i, j, target_row, target_col, color):
                    possible.append([i, j])
    
    return possible

# === ОСНОВНОЙ ЦИКЛ ИГРЫ ===
print('\n' + '='*50)
print('Форматы ввода:')
print('1. Координатный: e2e4')
print('2. Рокировка: 0-0 или 0-0-0')
print('3. Простой: конь e4, пешка d5')
print('exit - выход')
print('='*50 + '\n')

while not game_over:
    print_board()
    
    if en_passant_target:
        col = index_to_col(en_passant_target[1])
        row = 8 - en_passant_target[0]
        print(f"⚠️  Можно взять на проходе на {col}{row}")
    
    print(f'ХОДИТ: {get_current_player()} {"(БЕЛЫЕ)" if current == 0 else "(ЧЕРНЫЕ)"}')
    
    move = input('> ').strip().lower()
    
    if move == 'exit':
        print('Игра прервана')
        break
    
    # Пробуем распарсить ход
    parsed = parse_move(move)
    
    if parsed and parsed[0] == 'castle':
        if can_castle(current, parsed[1]):
            do_castle(current, parsed[1])
            result = check_game_over()
            if result != 0:
                game_over = True
            else:
                current = 1 if current == 0 else 0
        else:
            print('❌ Рокировка невозможна!')
            input('Нажми Enter...')
        continue
    
    if parsed and parsed[0] == 'move':
        from_pos, to_pos = parsed[1], parsed[2]
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Проверяем, что это фигура текущего игрока
        piece = get_piece_at(from_row, from_col)
        if piece == '.' or (current == 0 and not is_white(piece)) or (current == 1 and not is_black(piece)):
            print('❌ Там нет вашей фигуры!')
            input('Нажми Enter...')
            continue
        
        # Проверяем возможность хода
        if not can_move_piece(from_row, from_col, to_row, to_col):
            print('❌ Фигура не может так ходить!')
            input('Нажми Enter...')
            continue
        
        # Проверяем, не подставим ли короля
        if move_leaves_king_in_check(from_row, from_col, to_row, to_col, current):
            print('❌ Ход оставляет короля под шахом!')
            input('Нажми Enter...')
            continue
        
        # Делаем ход
        make_move(from_row, from_col, to_row, to_col)
        continue
    
    # Старый формат
    parts = move.split()
    if len(parts) == 2:
        piece_name, target = parts
        target_pos = parse_square(target)
        
        if target_pos:
            possible = find_piece_by_name(piece_name, target_pos[0], target_pos[1], current)
            
            if not possible:
                print(f'❌ Нет фигуры "{piece_name}", которая может пойти на {target}')
            elif len(possible) > 1:
                print(f'❌ Несколько фигур могут пойти на {target}. Используй координаты (например: e2e4)')
            else:
                from_pos = possible[0]
                make_move(from_pos[0], from_pos[1], target_pos[0], target_pos[1])
            
            input('Нажми Enter...')
            continue
    
    print('❌ Неверный формат! Используй: e2e4, 0-0, или конь e4')
    input('Нажми Enter...')

if game_over:
    print_board()
    print('\n' + '='*40)
    print('ИГРА ОКОНЧЕНА!')
    print('='*40)
