# kernel_tasks.py
# BRANCH: main
# ROLE: Kernel task integration (SAFE)

from task_queue import TaskQueue


class KernelTasks:
    def __init__(self):
        self.queue = TaskQueue()

    def defer(self, fn, *args, **kwargs):
        self.queue.add(fn, *args, **kwargs)

    def flush(self):
        self.queue.run_all()
