import os

class Chart:
    def __init__(self):
        self.temp_file_name = ".tmp.chrt"

    def generate_chart(self, filename):
        raise NotImplementedError

    def create_temp_file(self):
        try:
            with open(self.temp_file_name, "w") as f:
                f.write("")
        except IOError as e:
            raise IOError(e.errno, e.strerror)

    def delete_temp_file(self):
        try:
            if os.path.exists(self.temp_file_name):
                os.remove(self.temp_file_name)
        except OSError as e:
            raise IOError(e.errno, e.strerror)