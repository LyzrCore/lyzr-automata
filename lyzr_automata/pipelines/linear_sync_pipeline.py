import time
from typing import List

from lyzr_automata.tasks.task_base import Task
from lyzr_automata.utils.resource_handler import ResourceBox


class LinearSyncPipeline:
    def __init__(
        self,
        tasks: List[Task],
        completion_message: str = "",
        name: str = "",
        resource_box: ResourceBox = ResourceBox(base_folder="resources"),
    ):
        self.tasks = tasks
        self.completion_message = completion_message
        self.name = name
        for task in self.tasks:
            task.set_resource_box(resource_box=resource_box)

    def _execute(self):
        previous_output = ""
        tasks_output = []
        tasks_map = {}
        for task in self.tasks:
            if task.input_tasks is None or len(task.input_tasks) == 0:
                task.previous_output = str(previous_output)
            else:
                dependency_task_output = ""
                for dependency_task in task.input_tasks:
                    if dependency_task.instructions in tasks_map.keys():
                        dependency_task_output = (
                            tasks_map[dependency_task.instructions]
                            + dependency_task_output
                        )
                task.previous_output = dependency_task_output

            previous_output = task.execute()
            tasks_map[task.instructions] = str(previous_output)
            tasks_output.append(
                {"task_id": task.task_id, "task_output": previous_output}
            )
        return tasks_output

    def run(self):
        # TODO create a better logger
        execution_stat_time = time.time()
        print(
            f" ------- START PIPELINE {self.name} :: start time : {str(execution_stat_time)} ------- "
        )
        self.output = self._execute()
        execution_end_time = time.time()
        execution_time = execution_end_time - execution_stat_time
        print(
            f" ------- END PIPELINE {self.name} :: end time :  {str(execution_end_time)} :: execution time : {execution_time} ------- "
        )
        print(self.completion_message)
        return self.output
