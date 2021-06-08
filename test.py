class Angle():
    def __init__(self, l, w) -> None:
        self.l = l
        self.w = w
        self.o = 0
        self.name = 'Angle'

    def rotate(self):
        self.o = (self.o + 1) % 4

    def default(self):
        self.o = 0

class Square():
    def __init__(self, l, w) -> None:
        self.w = w
        self.l = l
        self.name = 'Square'

    def default(self):
        pass

class Field():
    figure_number = 0

    def __init__(self, w, l) -> None:
        self.l = l
        self.w = w
        self.field = [[0 for j in range(w)] for i in range(l)]

    def __findCoords(self, i, j, figure):
        coords = []
        if figure.name == 'Square':
            if (figure.l + i > self.l) or (figure.w + j > self.w):
                raise ValueError('Out of bounds')
            else:
                for l in range(i, i+figure.l):
                    for w in range(j, j+figure.w):
                        coords.append([l, w])
        else:
            if figure.o == 0 or figure.o == 2:
                fig_w = figure.w
                fig_l = figure.l
            else:
                fig_w = figure.l
                fig_l = figure.w
            
            if (fig_l + i > self.l) or (fig_w + j > self.w):
                raise ValueError('Out of bounds')
            else:
                for l in range(i, fig_l+i):
                    coords.append([l, j if figure.o < 2 else j + fig_w - 1])
                for w in range(j, fig_w+j):
                    coords.append([i if 0 < figure.o < 3 else i + fig_l - 1, w])
        return coords

    def place(self, i, j, figure):
        coords = self.__findCoords(i, j, figure)
        if self.checkPlace(coords):
            Field.figure_number += 1
            for coord in coords:
                self.field[coord[0]][coord[1]] = Field.figure_number
        else:
            raise ValueError('Already taken')

    def checkPlace(self, coords):
        for coord in coords:
            if self.field[coord[0]][coord[1]] != 0:
                return False
        return True

    def remove(self, i, j, figure):
        coords = self.__findCoords(i, j, figure)
        Field.figure_number -= 1
        for coord in coords:
                self.field[coord[0]][coord[1]] = 0

    def __str__(self):
        s = ''
        for row in self.field:
            for cell in row:
                if cell != 0:
                    s+=str(cell)
                else:
                    s+='o'
            s+='\n'
        return s

def try_place(field, idx, figures, stop):
    if idx == stop:
        return True
    for i in range(field.l):
        for j in range(field.w):
            if figures[idx].name == 'Angle':
                max_r = 4
            else:
                max_r = 1
            for r in range(max_r):
                try:
                    field.place(i, j, figures[idx])
                    # print(field)
                    if try_place(field, idx + 1, figures, stop):
                        return True
                    field.remove(i, j, figures[idx])
                except:
                    pass
                if max_r == 4:
                    figures[idx].rotate()
        figures[idx].default()
    return False
            

def solve(size, squares, angles):
    figures = []
    field = Field(size[0], size[1])
    for square in squares:
        for i in range(square[1]):
            figures.append(Square(square[0][0], square[0][1]))
    for angle in angles:
        for i in range(angle[1]):
            figures.append(Angle(angle[0][0], angle[0][1]))
    return try_place(field, 0, figures, len(figures))


if __name__ == '__main__': 
    '''
    Закомментированные строчки кода - ручной ввод, построчно уточняется количество фигур каждого типа, их количество и размер.
    Также, для удобства, я выводил получившееся поле. Разными цифрами я отделял разные фигуры. Строчка 101, ее можно разкомментировать чтобы посмотреть!
    '''
    # field_size = tuple(map(int, input('enter size of field\n').split(' ')))
    # squares =[]
    # for i in range(int(input('enter count of square types\n'))):
    #     sq_count = int(input('enter count of squares\n'))
    #     square_size = tuple(map(int, input('enter size of square\n').split(' ')))
    #     squares.append((square_size, sq_count))
    # angles = []
    # for i in range(int(input('enter count of angle types\n'))):
    #     angle_count = int(input('enter count of angles\n'))
    #     angle_size = tuple(map(int, input('enter size of angle\n').split(' ')))
    #     angles.append((angle_size, angle_count))
    # print(solve(field_size, squares, angles))
    print(solve((3, 5), [((1, 1), 1), ((2, 2), 1)], [((3, 2), 1), ((2,2), 2)]))
