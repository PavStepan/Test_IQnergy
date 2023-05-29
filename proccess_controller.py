import multiprocessing
import pickle
import time


class ProcessController:
    """ Класс, который организует очередь задач и параллельное их выполнение """
    def __init__(self):
        self.max_proc = 1
        self.tasks = list()
        self.start_tasks = list()

    def set_max_proc(self, n: int):
        self.max_proc = n

    def start(self, tasks, max_exec_time):
        self.tasks = tasks
        while len(multiprocessing.active_children()) < self.max_proc and len(self.tasks) > 0:
            i_task = self.tasks.pop(0)
            process = multiprocessing.Process(target=self.run_task, args=(i_task, max_exec_time))
            process.start()

    def run_task(self, task, max_exec_time):
        self.start_tasks.append(multiprocessing.current_process())
        start_task = time.time()
        run_func, args = task
        run_func(*args)
        end_task = time.time() - start_task
        if max_exec_time > 0:
            count_second = 0 if (max_exec_time - end_task) < 0 else (max_exec_time - end_task)
            time.sleep(count_second)

    def wait(self):
        while len(self.tasks) > 0:
            if len(multiprocessing.active_children()) > 0:
                for i_process in multiprocessing.active_children():
                    i_process.join()
                self.start_tasks = []
            else:
                self.start(self.tasks, self.max_proc)

    def wait_count(self):
        return len(self.tasks)

    @staticmethod
    def alive_count():
        return len(multiprocessing.active_children())
