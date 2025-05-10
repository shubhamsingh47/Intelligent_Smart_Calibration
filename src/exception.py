import sys


def error_message_details(error, error_details: sys):
    try:
        # Get the traceback object
        _, _, exc_tb = error_details.exc_info()

        # Extract details
        file_name = exc_tb.tb_frame.f_code.co_filename  # file where the error occurred
        line_number = exc_tb.tb_lineno  # line number of the error
        error_message = f"Error occurred in file: {file_name}, line: {line_number}, error: {str(error)}"

        return error_message
    except Exception as e:
        return f"Failed to retrieve error details. Error: {str(e)}"


class CustomException(Exception):
    def __init__(self, error_message, error_details: sys):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message, error_details)

    def __str__(self):
        return self.error_message
