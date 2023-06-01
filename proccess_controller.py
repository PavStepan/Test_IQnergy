import multiprocessing
import time


class ProcessController:
    """ Класс, который организует очередь задач и параллельное их выполнение """
    def __init__(self):
        self.max_proc = multiprocessing.Queue()
        self.tasks = multiprocessing.Queue()
        self.max_proc.put(1)
        self.is_wait = multiprocessing.Queue()
        self.count_run_tasks = multiprocessing.Queue()
        self.count_tasks = multiprocessing.Queue()

        multiprocessing.Process(target=self.process_handler, args=(self.tasks, self.max_proc, self.is_wait)).start()

    def set_max_proc(self, n: int):
        self.max_proc.put(n)

    def start(self, tasks, max_exec_time=0):
        self.tasks.put([[(i_task[0], i_task[1]), max_exec_time] for i_task in tasks])

    def process_handler(self, tasks, max_proc, is_wait):
        proc_task = []
        proc_run_task = []
        max_proc_count = 1
        wait_process = False

        while True:
            if not is_wait.empty():
                wait_process = is_wait.get()

            if not max_proc.empty():
                max_proc_count = max_proc.get()

            if not tasks.empty():
                proc_task.extend(tasks.get())

            if len(proc_task) > 0 and max_proc_count > len(proc_run_task):
                i_task, count_time = proc_task.pop(0)
                process = multiprocessing.Process(target=self.run_task, args=(i_task, count_time))
                proc_run_task.append(process)
                process.start()
                print('запустили', process)
                if wait_process:
                    print(process, 'запуск с ожиданием')
                    process.join()
                    time.sleep(count_time)
            for i in proc_run_task:
                if not i.is_alive():
                    proc_run_task.remove(i)
            time.sleep(1)
            self.count_run_tasks.put(len(proc_run_task))
            self.count_tasks.put(len(proc_task))

    @staticmethod
    def run_task(task, max_exec_time):
        print(f'start {multiprocessing.current_process()}')
        run_func, args = task
        start = time.time()
        process = multiprocessing.Process(target=run_func, args=args)
        process.start()

        if max_exec_time > 0:
            while time.time() - start < max_exec_time:
                time.sleep(1)
            process.terminate()

        print(f'end {multiprocessing.current_process()}')

    def wait(self):
        self.is_wait.put(True)

    def wait_count(self):
        count = self.count_tasks.get()
        return count

    def alive_count(self):
        count = self.count_run_tasks.get()
        return count
