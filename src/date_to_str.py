"""
In this source file there is class DateToStr which is accountable of parsing current date
to string. User can specify details of date using DateNameType enum value as a method
parameter.
"""

from enum import Enum
from datetime import datetime


class DateNameType(Enum):
    """
    NameDateType enum represents types of available file names formats
    of robotic car.
    """
    DATE_HOUR_MINUTE_SECONDS = 0
    DATE_HOUR_MINUTE = 1
    DATE = 2


class DateToStr:
    """
    Class is responsible for generating new file names depends on actual time. 
    """
    @staticmethod
    def parse_date(name_format: DateNameType) -> str:
        """
        Method creats new file name based on current date and time.
        """
        current_time = datetime.now()
        filename = ""
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
    print(DateToStr.parse_date(DateNameType.DATE_HOUR_MINUTE_SECONDS))
    print(DateToStr.parse_date(DateNameType.DATE_HOUR_MINUTE))
