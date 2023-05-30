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

    def start(self, tasks, max_exec_time=0):
        self.tasks = tasks
        self.max_exec_time = max_exec_time
        while len(multiprocessing.active_children()) < self.max_proc and len(self.tasks) > 0:
            i_task = self.tasks.pop(0)
            process = multiprocessing.Process(target=self.run_task, args=(i_task, ))
            process.start()

        start = time.time()

        while len(multiprocessing.active_children()) > 0:
            if max_exec_time > 0:
                for i_process in multiprocessing.active_children():
                    print(f'Процесс {i_process} работает {time.time() - start} Секунд')
                    if i_process.is_alive() and time.time() - start >= max_exec_time:
                        i_process.terminate()
                        print(f'Процесс {i_process} не успела выполнится за {max_exec_time} секунд! TERMINATE')
                    else:
                        if i_process.is_alive():
                            print(f'Процесс {i_process} продолжает свою работу свою работу!')
                        else:
                            print(f'Процесс {i_process} завершила свою работу!')
                time.sleep(1)

    @staticmethod
    def run_task(task):
        print(f'Процесс {multiprocessing.current_process()} начал работу!')
        run_func, args = task
        start = time.time()
        run_func(*args)
        print(f'Процесс {multiprocessing.current_process()} выполнен за {time.time() - start}')

    def wait(self):
        while len(self.tasks) > 0:
            if len(multiprocessing.active_children()) < self.max_proc:
                self.start(self.tasks, self.max_exec_time)

    def wait_count(self):
        return len(self.tasks)

    @staticmethod
    def alive_count():
        return len(multiprocessing.active_children())
