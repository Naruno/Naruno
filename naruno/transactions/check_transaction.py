import datetime

class TransactionLogger:
    def __init__(self, transaction_file):
        self.transaction_file = transaction_file

    def _write_log(self, level, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} - {self.transaction_file} - {level} - {message}\n"
        with open("transaction_logs.txt", "a") as log_file:
            log_file.write(log_message)

    def info(self, message):
        self._write_log("INFO", message)

    def warning(self, message):
        self._write_log("WARNING", message)

    def error(self, message):
        self._write_log("ERROR", message)