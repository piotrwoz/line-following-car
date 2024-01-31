"""
In this source file there are class class NameGenerator which is accountable of generating
new filenames based on current date and time.
"""

from datetime import datetime

from date_name_type import DateNameType


class NameGenerator:
    """
    Class is responsible for generating new file names depends on actual time. 
    """
    @staticmethod
    def create_name(name_format: DateNameType) -> str:
        """
        Method creats new file name based on current date and time.
        """
        current_time = datetime.now()
        filename = None
        match name_format:
            case DateNameType.DATE_HOUR_MINUTE_SECONDS:
                day_part = current_time.strftime("%Y_%m_%d")
                hour_part = current_time.strftime("%H_%M_%S")
                filename = f"{day_part}-{hour_part}"
            case DateNameType.DATE_HOUR_MINUTE:
                day_part = current_time.strftime("%Y_%m_%d")
                hour_part = current_time.strftime("%H_%M")
                filename = f"{day_part}-{hour_part}"
            case _:
                print("Unknown file name type. Returning empty string")
                filename = ""

        return filename


if __name__ == "__main__":
    print(NameGenerator.create_name(DateNameType.DATE_HOUR_MINUTE_SECONDS))
    print(NameGenerator.create_name(DateNameType.DATE_HOUR_MINUTE))
