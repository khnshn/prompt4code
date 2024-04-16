import random

import simpy


RANDOM_SEED = 42
SIM_TIME = 24 * 60 * 60
NOTIFICATION_INTERVAL = 2 * 60 * 60


def teacher(env, name, response_rate):
    while True:
        yield env.timeout(NOTIFICATION_INTERVAL)

        response = random.random() < response_rate
        if response:
            print("%s responded to the notification." % name)
        else:
            print("%s ignored the notification." % name)


print("Teacher activity simulation")
random.seed(RANDOM_SEED)
env = simpy.Environment()


response_rates = [random.uniform(0.5, 1.0) for _ in range(50)]

teachers = []
for i in range(50):
    teacher_name = "Teacher %02d" % i
    response_rate = response_rates[i]
    teachers.append(env.process(teacher(env, teacher_name, response_rate)))

env.run(until=SIM_TIME)


response_count = sum(1 for teacher in teachers if teacher.triggered)
response_rate = (response_count / len(teachers)) * 100

print("Response Rate: %.2f%%" % response_rate)
