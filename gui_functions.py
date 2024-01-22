class Solenoids:
    def __init__(self):
        print("solenoids initialized")
        self.state = [0, 0, 0, 0, 0]

    def changeSolenoid(self, sol):
        status = "opened"
        if self.state[sol]: status = "closed"
        self.state[sol] = ~self.state[sol]

        print("solenoid " + str(sol) + " " + status)
