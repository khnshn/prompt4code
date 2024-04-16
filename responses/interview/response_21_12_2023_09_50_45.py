import random
import simpy
import matplotlib.pyplot as plt


RANDOM_SEED = 42
SIM_DURATION = 100
PAIN_THRESHOLD = 5
NOTIFICATIONS_PER_DAY = [1, 2, 3]
QUESTION_TYPES = ["Personalized", "Non-Personalized"]


class Patient(object):
    def __init__(self, env, name):
        self.env = env
        self.name = name
        self.pain = 0
        self.responses = 0
        self.notifications_sent = 0

    def process_notifications(self):
        while True:
            if self.pain >= PAIN_THRESHOLD:
                question_type = random.choice(QUESTION_TYPES)
                self.env.process(self.send_notification(question_type))
                self.notifications_sent += 1

            yield self.env.timeout(24)

    def send_notification(self, question_type):
        if question_type == "Personalized":
            response_rate = random.uniform(0.6, 0.9)
        else:
            response_rate = random.uniform(0.2, 0.5)

        self.responses += response_rate

    def experience_pain(self):
        while True:
            self.pain += random.uniform(0.5, 2)
            yield self.env.timeout(random.uniform(1, 5))


def run_simulation(env, num_patients):
    patients = []
    for i in range(num_patients):
        patient = Patient(env, f"Patient{i+1}")
        patients.append(patient)
        env.process(patient.experience_pain())
        env.process(patient.process_notifications())

    yield env.timeout(SIM_DURATION)

    return patients


def visualize_results(results):
    fig, ax = plt.subplots()
    plt.xlabel("Number of Notifications Per Day")
    plt.ylabel("Average Response Rate")
    for question_type in QUESTION_TYPES:
        response_rates = []
        for num_notifications in NOTIFICATIONS_PER_DAY:
            response_rate = results[question_type][num_notifications] / SIM_DURATION
            response_rates.append(response_rate)

        ax.plot(NOTIFICATIONS_PER_DAY, response_rates, label=question_type)

    ax.legend()

    plt.show()


print("Oncology Patients Simulation")

random.seed(RANDOM_SEED)
env = simpy.Environment()
results = {
    question_type: {num_n: 0 for num_n in NOTIFICATIONS_PER_DAY}
    for question_type in QUESTION_TYPES
}

for num_notifications in NOTIFICATIONS_PER_DAY:
    env.process(run_simulation(env, 100))

env.run(until=SIM_DURATION)

visualize_results(results)
