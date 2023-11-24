class Quadruples:
    def __init__(self):
        # siguiente cuadruplo a generar
        self.counter = 0
        self.list = []

    # funcion para generar un nuevo cuadruplo
    def gen_quad(self, op, left, right, res):
        quad = [op, left, right, res]
        self.list.append(quad)
        self.counter += 1
        # print(self.counter,quad)

    # funcion para completar algun dato vacio de un cuadruplo
    # index es el dato a completar con val
    def fill_quad(self, quad, index, val):
        self.list[quad][index] = val