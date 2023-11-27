from pandas import read_excel
import matplotlib.pyplot as plt

class Analyser:
    def __init__(self, path):
        self.path = path
        self.read()

    def read(self):
        self.data = read_excel(self.path)

    @classmethod
    def get_index(cls, par, data):
        for a, b in enumerate(data.keys()):
            if b == par:
                ind = a
        return ind if 'ind' in locals() else None

    def find_revenue(self):
        ind_num = self.get_index("number", self.data)
        ind_price = self.get_index("price per unit", self.data)

        sum = 0
        for a in self.data.values:
            sum += a[ind_num] * a[ind_price]
        return sum

    def find_need_par(self, par):
        ind = self.get_index(par, self.data)
        if ind == None: return None

        list = []
        for a in self.data.values:
            list.append(a[ind])
        return list

    def sort_need(self, data):
        return sorted(data) if data != None else None

    def do_graph(self, list1, list2, value):
        plt.title(value)
        plt.plot(list1, list2)
        plt.show()

class Interface:

    def print_menu(self, message, list_var, list_func):
        print(message)
        for num, var in enumerate(list_var):
            print(f"{num+1}. {var}")

        otv = input("What? : ")
        while (int(otv) not in range(len(list_func)+1)):
            print(otv, range(len(list_func)))
            otv = input("Error\nWhat? : ")
        try:
            data = list_func[int(otv)-1]()
            if data != None: print(data)
        except: print("error func")

def main():
    an = Analyser("need.xlsx")
    inter = Interface()

    while True:
        inter.print_menu("Main menu", ["Find need value", "Sort need value", "Find revenue", "Build graph"],
                         [lambda: an.find_need_par(input("Value: ")), lambda: an.sort_need(an.find_need_par(input("What sort? (value) : "))), lambda: an.find_revenue(),
                          lambda: inter.print_menu( "Where give data?",
                              ["Ourself", "Program finction"],
                              [lambda: an.do_graph(eval(input("Enter list data 1 (Example: [1, 2, 3] ): ")), eval(input("Enter list data 2 (Example: [1, 2, 3] ): ")), input("Name graph: ")),
                               lambda: an.do_graph(an.find_need_par(input("Values 1: ")), an.find_need_par(input("Values 2: ")), input("Name graph: "))]
                              )]
                         )

if __name__ == '__main__':
    main()


