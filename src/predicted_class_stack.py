"""
PredictedClassStack is responsible for storing history of predicted labels of classificated photos
from robotic car.
"""

from predicted_class import PredictedClass


class PredictedClassStack:
    """
    Class is representing stack for next predicted labels of classified photos
    from robotic car.
    """

    def __init__(self):
        self._stack = list()
        self._max_size = 2


    def push(self, predicted_class: PredictedClass):
        """
        Push predicted class on top of the stack.
        """
        self._stack.insert(0, predicted_class)
        if len(self._stack) > self._max_size:
            self._stack.pop()


    def check_if_stack_contains_only_thrash(self) -> bool:
        """
        Check if there are only 'thrash' classes in the stack.
        """
        is_only_thrash = True
        for predicted_class in self._stack:
            if predicted_class != PredictedClass.THRASH_IMAGE:
                is_only_thrash = False
                break

        return is_only_thrash


    def print_stack(self):
        """
        Print stack on console.
        """
        print("Current predicted classes stack:")
        for elem in self._stack:
            print(elem)
        print("")


    def get_stack_top(self):
        """
        Last pushed predicted class getter.
        """
        return self._stack[0]


    def get_stack_second_element(self):
        """
        Previously pushed predicted class getter.
        """
        return self._stack[1]


    def get_stack(self):
        """
        Predicted classes stack getter.
        """
        return self._stack


if __name__ == "__main__":
    stack = PredictedClassStack()
    stack.push(PredictedClass.FORWARD)
    stack.push(PredictedClass.FORWARD)
    stack.push(PredictedClass.RIGHT)
    stack.push(PredictedClass.FORWARD)
    stack.push(PredictedClass.LEFT)
    stack.push(PredictedClass.LEFT)
    stack.push(PredictedClass.THRASH_IMAGE)
    stack.push(PredictedClass.THRASH_IMAGE)
    stack.push(PredictedClass.FORWARD)

    stack.print_stack()
    print(f"Last pushed: {stack.get_stack_top()}")
    print(f"Is only thrash: {stack.check_if_stack_contains_only_thrash()}")
