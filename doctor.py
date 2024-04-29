NO_ID = 0
BLANK = 0

class Doctor:
    def __init__(self):
        self.id = NO_ID
        self.username = BLANK
        self.name = BLANK
    
    def set_doctor(self, doctorInfo):
        self.id = int(doctorInfo[0])
        self.username = str(doctorInfo[1])
        self.name = str(doctorInfo[2] + " " + doctorInfo[3])
    
    def print_doctor_data(self):
        print("Doctor ID: ", self.id)
        print("Doctor username: ", self.username)
        print("Doctor name:", self.name)
