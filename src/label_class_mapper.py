"""
LabelClassMapper class is responsible for mapping labels and predicted classes.
"""

from predicted_class import PredictedClass


class LabelClassMapper:
    """
    Class is sharing interface for mapping predicted labels into classes
    stored in PredictedClass enum.
    """

    @staticmethod
    def map_label_to_class(label: str) -> PredictedClass:
        """
        Static method for mapping
        """
        predicted_class = None
        match label:
            case "forward":
                predicted_class = PredictedClass.FORWARD
            case "back":
                predicted_class = PredictedClass.BACK
            case "right":
                predicted_class = PredictedClass.RIGHT
            case "left":
                predicted_class = PredictedClass.LEFT
            case "slight-right":
                predicted_class = PredictedClass.SLIGHT_RIGHT
            case "slight-left":
                predicted_class = PredictedClass.SLIGHT_LEFT
            case "thrash":
                predicted_class = PredictedClass.THRASH_IMAGE
            case _:
                predicted_class = PredictedClass.THRASH_IMAGE
                print("Unknown label. Returning thrash image!")

        return predicted_class
