import multiprocessing
import time


class ProcessController:
    """ Класс, который организует очередь задач и параллельное их выполнение """
    def __init__(self):
        self.max_proc = 1
        self.tasks = multiprocessing.Queue()
        self.run_tasks = multiprocessing.Queue()
        print('nen')
        print(self.tasks.empty())
        multiprocessing.Process(target=self.process_handler, args=(self.tasks, self.run_tasks)).start()

    def set_max_proc(self, n: int):
        self.max_proc = n

    def start(self, tasks, max_exec_time=0):
        self.tasks.put([[i_task[0], i_task[1], max_exec_time] for i_task in tasks])
        print(self.tasks.get())

    def process_handler(self, tasks):
        print('nen!!')
        if not tasks.empty():
            print(tasks)
            print('Start')
            # while True:
            #     print(self.tasks)
            #     if len(self.run_tasks) < self.max_proc and len(tasks) > 0:
            #         i_task, count_time = tasks.get()
            #         process = multiprocessing.Process(target=self.run_task, args=(i_task, count_time))
            #         self.run_tasks.append(process)
            #         process.start()
            #
            #     for i_process in self.run_tasks:
            #         if not i_process.is_alive():
            #             self.run_tasks.remove(i_process)

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
        pass


    # def wait_count(self):
    #     return len(self.tasks)
    #
    # def alive_count(self):
    #     return len(self.run_tasks)
