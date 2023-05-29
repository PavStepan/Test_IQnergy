import multiprocessing
import time


class ProcessController:
    """ Класс, который организует очередь задач и параллельное их выполнение """
    def __init__(self):
        self.max_proc = 1
        self.tasks = list()
        self.max_exec_time = 0

    def set_max_proc(self, n: int):
        self.max_proc = n

    def start(self, tasks, max_exec_time):
        self.tasks = tasks
        self.max_exec_time = max_exec_time
        while len(multiprocessing.active_children()) < self.max_proc and len(self.tasks) > 0:
            i_task = self.tasks.pop(0)
            process = multiprocessing.Process(target=self.run_task, args=(i_task, ))
            process.start()

        for i_process in multiprocessing.active_children():
            i_process.join(timeout=max_exec_time)
            if i_process.is_alive():
                i_process.terminate()
                print(f'функция не успела выполнится за {max_exec_time} секунд!')
            else:
                print(f'функция выполнится менее чем за {max_exec_time} секунд!')

    @staticmethod
    def run_task(task):
        run_func, args = task
        start = time.time()
        run_func(*args)
        print(f'функция выполнена за {time.time() - start}')

    def wait(self):
        while len(self.tasks) > 0:
            if len(multiprocessing.active_children()) > 0:
                for i_process in multiprocessing.active_children():
                    i_process.join()
            else:
                print(self.max_exec_time)
                self.start(self.tasks, self.max_exec_time)

    def wait_count(self):
        return len(self.tasks)

    @staticmethod
    def alive_count():
        return len(multiprocessing.active_children())
