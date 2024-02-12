"""Задача_7.
Напишите программу на Python, которая будет находить
сумму элементов массива из 1000000 целых чисел.
� Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
� Массив должен быть заполнен случайными целыми числами от 1 до 100.
� При решении задачи нужно использовать многопоточность, многопроцессорность и асинхронность.
� В каждом решении нужно вывести время выполнения вычислений."""
import multiprocessing
from random import randint
import time


def sum_array_elements(arr, start, end):
    return sum(arr[start:end])


if __name__ == "__main__":
    start_time = time.time()
    process = []
    numbers = [randint(1, 100) for _ in range(1_000_000)]
    print(f'Сумма массива для проверки равна: {sum(numbers)}')
    tasks = [sum_array_elements(numbers, i * 250000, (i + 1) * 250000) for i in range(4)]

    for i in range(4):
        p = multiprocessing.Process(target=sum_array_elements, args=(numbers, i * 250000, (i + 1) * 250000))
        process.append(p)
        p.start()
    for t in process:
        t.join()

    print(f'Сумма с помощью многозадачности равна: {sum(tasks)}')
    print(f"Время выполнения вычислений: {(time.time() - start_time):.3f} секунд.")
