import random
import simpy

SIM_DURATION = 4 * 7 * 24 * 60  # 4 weeks in minutes
PATIENTS = 100

class Patient:
    def __init__(self, env, num_notifications):
        self.env = env
        self.num_notifications = num_notifications
        
        self.action = env.process(self.run())
        self.responses = 0
    
    def run(self):
        for day in range(SIM_DURATION // (24 * 60)):
            
            for notification in range(self.num_notifications):
                yield env.timeout(random.randint(0, 1440))  
                self.responses += 1

num_notifications = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

average_response_rates = []

for num_notification in num_notifications:
    env = simpy.Environment()
    patients = [Patient(env, num_notification) for _ in range(PATIENTS)]
    env.run(until=SIM_DURATION)
    
    total_responses = sum([patient.responses for patient in patients])
    average_response_rate = total_responses / (PATIENTS * num_notification * (SIM_DURATION // 1440))
    average_response_rates.append(average_response_rate)

print("Number of Notifications: ", num_notifications)
print("Average Response Rates: ", average_response_rates)