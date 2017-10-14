# logger.py
# by James Fulford


def log(errors, path):
    """
    utils.logger.log
    Dumps errors into file at given path
    (Doesn't write if there are no errors.)
    """
    from utils.saveload import save
    if(len(errors) > 0):
        save(errors, path)


class Logger():
    """
    utils.logger.Logger
    Class that logs different types of errors into a json file.
    """
    def __init__(self, path):
        """
        Saves .json file to the path specified
        """
        import os
        self.path = path
        self.errors = {
            "default": []
        }

    def log(self, error, error_type=None):
        """
        Adds an error to the log.
        If error_type is specified, adds error to that category
        Otherwise, adds error to "default" category.
        """
        category = "default"
        if error_type:
            category = str(error_type)
            if category not in self.errors:
                self.errors[category] = []
        self.errors[category].append(error)

    def save(self):
        """
        Writes all errors to log file.
        """
        log(self.errors, self.path)
        from analytics import frequency
        print("Error frequencies: ")
        freq = {}
        for key in self.errors.keys():
            freq[key] = len(self.errors[key])
        print freq

