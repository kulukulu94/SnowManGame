class ScoreManager:
    
    def __init__(self):
        open('records.txt', 'a')   # Opens file for appending
        with open('records.txt', 'r+') as f:
            try:
                self.record = int(f.read())
                # Extracts all characters in file as a string
            except:
                self.record = 0
    
    # Finds previous high score 
    def get_records(self):
        return self.record

    def set_new_record(self, score):
        with open('records.txt', 'w') as f: 
            f.write(str(score)) # Adds score to file
        self.record = score
   
