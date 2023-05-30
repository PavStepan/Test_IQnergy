import random
import time

from proccess_controller import ProcessController


def task(num):
    print(f'задача {num} старт')
    time.sleep(random.randint(1, 5))
    print(f'задача {num} конец')


def main():
    pc = ProcessController()
    pc.set_max_proc(n=2)
    tasks = [(task, (i, )) for i in range(10)]
    pc.start(tasks=tasks, max_exec_time=2)

    print(f"\n\nВыполняемые задачи: {pc.alive_count()}, Задачи в ожидании: {pc.wait_count()}\n\n")

    print('Запускаем wait')
    pc.wait()

    print("Все задачи выполнены")


if __name__ == "__main__":
    main()
