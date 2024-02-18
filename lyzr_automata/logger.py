import datetime
import requests


class Logger:
    def __init__(self, file_name: str = None, webhook_url: str = None, webview:bool=False):
        self.file_name = file_name
        self.webhook_url = webhook_url

    def log(self, message, level):
        """General logging method."""
        with open(self.file_name, "a") as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"[{timestamp}] {level.upper()}: {message}\n")

    def info(self, message):
        """Log an info message."""
        self.log(message, "info")

    def warning(self, message):
        """Log a warning message."""
        self.log(message, "warning")

    def error(self, message):
        """Log an error message."""
        self.log(message, "error")

    def task(self, execution_time, start_time, end_time, output, name):
        """Log an info message."""

        if self.file_name != None:
            self.log(
                f"Name: {name} :: Start Time: {start_time} :: End Time: {end_time} :: Execution Secs: {execution_time} :: Output: {output}",
                "task",
            )
        
        if self.webhook_url != None:
            self.post_log(
                start_time=start_time,
                end_time=end_time,
                execution_time=execution_time,
                output=output,
                name=name,
            )

    def post_log(self, start_time, end_time, execution_time, output, name):
        url = self.webhook_url
        headers = {"Content-Type": "application/json"}
        try:
            data = {
            "start_time": start_time,
            "end_time": end_time,
            "execution_time": execution_time,
            "output": str(output),
            "name": name,
        }

            requests.post(url, json=data, headers=headers)
        except Exception as e:
            print(e)
            
