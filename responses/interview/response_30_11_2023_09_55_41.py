import simpy
import random
import matplotlib.pyplot as plt

# Parameters
RANDOM_SEED = 42
SIM_TIME = 24  # Simulate for 24 hours
INTERVAL = 60  # Time interval in minutes

# Symptom duration in minutes
SYMPTOM_DURATION = {
    "Abdominal Pain": (20, 60),
    "Nausea": (30, 120),
    "Vomiting": (15, 30),
    "Diarrhea": (60, 120),
}

# Symptom probability per hour
SYMPTOM_PROBABILITY = {
    "Abdominal Pain": 0.5,
    "Nausea": 0.3,
    "Vomiting": 0.2,
    "Diarrhea": 0.4,
}

symptoms = list(SYMPTOM_DURATION.keys())
symptom_count = len(symptoms)


def patient(env):
    while True:
        # Generate symptom
        hour = env.now // 60
        for i, symptom in enumerate(symptoms):
            if random.random() < (SYMPTOM_PROBABILITY[symptom] / 60):
                # Determine symptom duration
                min_duration, max_duration = SYMPTOM_DURATION[symptom]
                duration = random.randint(min_duration, max_duration)

                # Display symptom information
                print(f"Time: {env.now:2} minutes - Symptom: {symptom} (Duration: {duration} minutes)")

                # Simulate symptom duration
                yield env.timeout(duration)

        # Wait for next hour
        yield env.timeout(60)


# Setup and start simulation
random.seed(RANDOM_SEED)
env = simpy.Environment()

env.process(patient(env))

env.run(until=SIM_TIME * 60)

# Plot the simulation results
times = range(SIM_TIME * 60)
symptom_lines = [[] for _ in range(symptom_count)]

for t in times:
    for i, symptom in enumerate(symptoms):
        if env.now < t < env.now + SYMPTOM_DURATION[symptom][1]:
            symptom_lines[i].append(t)

plt.figure(figsize=(12, 6))
plt.title("Gastrointestinal Symptoms Simulation")
plt.xlabel("Time (minutes)")
plt.ylabel("Symptoms")

for i, line in enumerate(symptom_lines):
    if line:
        plt.plot(line, [i] * len(line), ".", markersize=5)

plt.yticks(range(symptom_count), symptoms)
plt.ylim([-1, symptom_count])
plt.show()