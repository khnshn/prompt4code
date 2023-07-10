import simpy
import random
import statistics


class Status(Enum):
    IDLE = 0
    WORKING = 1


class Teacher:
    def __init__(self, env, response_rate):
        self.env = env
        self.routine = env.process(self.run())
        self.status = Status.IDLE
        self.response_rate = response_rate

    def run(self):
        while True:
            yield self.env.timeout(2)
            if random.random() < self.response_rate:
                self.routine.interrupt("notification")

    def respond_to_notification(self):
        print(f"Teacher responded to notification at time {self.env.now}")


def simulate_teachers(env, num_teachers, response_rate):
    teachers = []
    for _ in range(num_teachers):
        teacher = Teacher(env, response_rate)
        teachers.append(teacher)

    while True:
        yield env.timeout(1)
        for teacher in teachers:
            if teacher.status == Status.IDLE:
                try:
                    teacher.routine.interrupt("activity")
                except simpy.Interrupt as interrupt:
                    if interrupt.cause == "notification":
                        teacher.respond_to_notification()
                        teacher.status = Status.WORKING
            elif teacher.status == Status.WORKING:
                try:
                    teacher.routine.interrupt("activity")
                except simpy.Interrupt as interrupt:
                    if interrupt.cause == "notification":
                        teacher.respond_to_notification()


env = simpy.Environment()
response_rate = 0.8  # 80% response rate
num_teachers = 50
env.process(simulate_teachers(env, num_teachers, response_rate))
env.run(until=10)  # Run the simulation for 10 hours

response_rates = []
for teacher in env.processes.items:
    teacher_response_rate = teacher.response_rate
    response_rates.append(teacher_response_rate)

mean_response_rate = statistics.mean(response_rates)
print(f"Mean response rate: {mean_response_rate}")
