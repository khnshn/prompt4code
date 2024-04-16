import random
import simpy


class Teacher(object):
    
    def __init__(self, env, id):
        self.env = env
        self.id = id
        self.notifications = 0
        self.responses = 0
        self.env.process(self.check_notifications())

    def check_notifications(self):
        while True:
            yield self.env.timeout(2)
            self.notifications += 1
            if random.random() < 0.5:
                self.responses += 1


def simulate_teachers(env, num_teachers):
    teachers = []
    
    for i in range(num_teachers):
        teachers.append(Teacher(env, i + 1))
    
    yield env.timeout(8) # simulate 8-hour workday
    
    total_notifications = 0
    total_responses = 0
    
    for teacher in teachers:
        total_notifications += teacher.notifications
        total_responses += teacher.responses
    
    response_rate = total_responses / total_notifications if total_notifications > 0 else 0
    
    print("Response rate: {:.2%}".format(response_rate))


random.seed(42)
env = simpy.Environment()
env.process(simulate_teachers(env, 50))
env.run()