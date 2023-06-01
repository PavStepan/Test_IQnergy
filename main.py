import random
import time

from proccess_controller import ProcessController


def task(num):
    print(num)
    time.sleep(random.randint(1, 10))

# вызывать несколько раз старт
# alive отличный от нуля
#

def main():
    pc = ProcessController()
    pc.set_max_proc(n=2)
    tasks = [(task, (i, )) for i in range(10)]
    pc.start(tasks=tasks, max_exec_time=2)
    pc.start(tasks=tasks, max_exec_time=2)

    # while pc.alive_count() > 0:
    #     print(f"\n\nВыполняемые задачи: {pc.alive_count()}, Задачи в ожидании: {pc.wait_count()}\n\n")

    print('Запускаем wait')
    #pc.wait()

    print("Все задачи выполнены")


if __name__ == "__main__":
    main()
