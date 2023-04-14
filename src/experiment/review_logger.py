
import datetime
class ReviewLogger():
    def __init__(self, sum_type, place):
        # create logging file for location
        self.filename = f"reviews/{place}_{sum_type}.csv"
        with open(self.filename , "w") as f:
            f.write("Summary\n")

    def log_review(self ,original_text, summary):
        with open(self.filename , "a") as f:
            # log current review
            f.write(f"{summary}\n")
