import tkinter as tk

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# Función para saber prioridad de operadores
def precedence(op):
    if op == '+' or op == '-':
        return 1
    if op == '*' or op == '/':
        return 2
    return 0

# Función para construir el árbol de la expresión
def construct_tree(expression):
    ops = []
    nodes = []

    i = 0
    while i < len(expression):
        if expression[i] == ' ':
            i += 1
            continue

        if expression[i] == '(':
            ops.append(expression[i])

        elif expression[i].isdigit():
            num = ''
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                num += expression[i]
                i += 1
            i -= 1
            nodes.append(Node(num))

        elif expression[i] == ')':
            while ops and ops[-1] != '(':
                op = ops.pop()
                right = nodes.pop()
                left = nodes.pop()
                operator_node = Node(op)
                operator_node.left = left
                operator_node.right = right
                nodes.append(operator_node)
            ops.pop()

        else:  # operador + - * /
            while (ops and precedence(ops[-1]) >= precedence(expression[i])):
                op = ops.pop()
                right = nodes.pop()
                left = nodes.pop()
                operator_node = Node(op)
                operator_node.left = left
                operator_node.right = right
                nodes.append(operator_node)
            ops.append(expression[i])

        i += 1

    while ops:
        op = ops.pop()
        right = nodes.pop()
        left = nodes.pop()
        operator_node = Node(op)
        operator_node.left = left
        operator_node.right = right
        nodes.append(operator_node)

    return nodes[-1]

# --------- Parte gráfica (Tkinter) ---------

class TreeDrawer:
    def __init__(self, root_node):
        self.root_node = root_node
        self.nodes_positions = {}
        self.width = 800
        self.height = 600
        self.level_gap = 80
        self.node_radius = 20
        self.x_counter = 0

        self.window = tk.Tk()
        self.window.title("Árbol de Expresiones")
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height, bg="white")
        self.canvas.pack()

        self.calculate_positions(self.root_node, 0)
        self.draw_tree(self.root_node)
        self.window.mainloop()

    def calculate_positions(self, node, depth):
        if node is None:
            return

        # Primero el hijo izquierdo
        self.calculate_positions(node.left, depth + 1)

        # Asignar posición X
        x = self.x_counter * 60 + 50
        y = depth * self.level_gap + 50
        self.nodes_positions[node] = (x, y)
        self.x_counter += 1

        # Luego el hijo derecho
        self.calculate_positions(node.right, depth + 1)

    def draw_tree(self, node):
        if node is None:
            return

        x, y = self.nodes_positions[node]

        # Dibujar líneas a hijos
        if node.left:
            x_left, y_left = self.nodes_positions[node.left]
            self.canvas.create_line(x, y, x_left, y_left)
        if node.right:
            x_right, y_right = self.nodes_positions[node.right]
            self.canvas.create_line(x, y, x_right, y_right)

        # Dibujar el nodo
        self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                x + self.node_radius, y + self.node_radius,
                                fill="lightblue")
        self.canvas.create_text(x, y, text=node.value, font=("Arial", 12, "bold"))

        # Recursivamente dibujar hijos
        self.draw_tree(node.left)
        self.draw_tree(node.right)

# --------- Programa principal ---------
if __name__ == "__main__":
    expr = input("Ingresa una expresión aritmética: ")

    root = construct_tree(expr)

    TreeDrawer(root)
