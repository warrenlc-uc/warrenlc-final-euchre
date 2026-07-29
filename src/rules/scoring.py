class Scoring:
    @staticmethod
    def calculate(
        caller_tricks,
        going_alone=False
    ):
        # Euchred
        if caller_tricks < 3:
            return 2
                
        # Sweep / march
        if caller_tricks == 5:
            # Successful lone hand
            if going_alone:
                return 4

            return 2
        
        return 1