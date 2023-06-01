import random
import time

from proccess_controller import ProcessController


def task(num):
    time.sleep(random.randint(1, 3))

# вызывать несколько раз старт
# alive отличный от нуля
#

def main():
    pc = ProcessController()
    pc.set_max_proc(n=2)
    tasks = [(task, (i, )) for i in range(10)]
    pc.start(tasks=tasks, max_exec_time=2)
    pc.start(tasks=tasks, max_exec_time=1)

    while pc.alive_count() > 0:
        print(f"\nВыполняемые задачи: {pc.alive_count()}, Задачи в ожидании: {pc.wait_count()}\n")
        time.sleep(1)

    print('Запускаем wait')
    pc.wait()

    print("Все задачи выполнены")


if __name__ == "__main__":
    main()
