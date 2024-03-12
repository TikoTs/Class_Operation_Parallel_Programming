import concurrent.futures
import configparser
import random as rd
import time

config = configparser.ConfigParser()

config.read('config.ini')

sample_number = int(config['ThreadConfig']['sample_number'])
processes_number = int(config['ThreadConfig']['processes_number'])
threads_per_processes = int(config['ThreadConfig']['threads_per_processes'])


class Trapezoid:
    def __init__(self, trap=None):
        if trap is None:
            trap = [0, 0, 0]
        self.a = trap[0]
        self.b = trap[1]
        self.h = trap[2]

    def __str__(self):
        return f'Base1 -> {self.b}, Base2 -> {self.a}, Height ->{self.h}'

    def area(self):
        base_sum = self.a + self.b
        return self.h * base_sum / 2

    def __lt__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() < other.area()
        return False

    def __eq__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() == other.area()
        return False

    def __ge__(self, other):
        if isinstance(other, Trapezoid):
            return not self.__lt__(other)
        return False


class Rectangle(Trapezoid):
    def __init__(self, re=None):
        if re is None:
            re = [0, 0]
        super().__init__(re)

    def __str__(self):
        return f'Height -> {self.a}, Width -> {self.h}'


class Square(Rectangle):
    def __init__(self, c):
        super().__init__(c)

    def __str__(self):
        return f'Side -> {self.a}'


def generate_areas():
    Trapezoid([rd.randint(1, 200), rd.randint(1, 200), rd.randint(1, 200)]).area()
    Rectangle([rd.randint(1, 200), rd.randint(1, 200)]).area()
    Square([rd.randint(1, 200)]).area()


def generate_areas_for_threadpool(_):
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads_per_processes) as executor:
        executor.map(generate_areas, range(sample_number // processes_number))


def main():
    start = time.perf_counter()
    with (concurrent.futures.ThreadPoolExecutor(max_workers=threads_per_processes * processes_number)
          as executor):
        executor.map(generate_areas, range(sample_number))
    finish = time.perf_counter()
    print(f'Threads take: {finish - start} seconds')

    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor(max_workers=processes_number) as executor:
        executor.map(generate_areas, range(sample_number))
    finish = time.perf_counter()
    print(f'ProcessPoolExecutor takes: {finish - start} seconds')

    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor(max_workers=processes_number) as executor:
        executor.map(generate_areas_for_threadpool, range(processes_number))
    finish = time.perf_counter()
    print(f'Both take: {finish - start} seconds')


if __name__ == '__main__':
    main()
