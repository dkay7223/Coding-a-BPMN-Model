import simpy
import random

RANDOM_SEED = 42
SIM_TIME = 120

NUM_AGENTS = 2
NUM_CALLS = 5

def generate_calls(env, num_calls, call_center):
    for i in range(num_calls):
        call = Call(i)
        call_center.put(call)
        print(f"Call {call.id} generated at {env.now}")
        yield env.timeout(random.randint(1, 10))

class Call:
    def __init__(self, id):
        self.id = id
        self.arrival_time = 0
        self.service_time = 0
        self.departure_time = 0

class Agent:
    def __init__(self, id, env, call_center):
        self.id = id
        self.env = env
        self.call_center = call_center
        self.busy = False

    def agent_process(self):
        while True:
            call = yield self.call_center.get()
            self.busy = True
            call.arrival_time = self.env.now
            print(f"Call {call.id} taken by agent {self.id} at {self.env.now}")
            yield self.env.timeout(random.randint(5, 15))
            call.service_time = self.env.now - call.arrival_time
            call.departure_time = self.env.now
            self.busy = False
            print(f"Call {call.id} completed by agent {self.id} at {self.env.now}")

def main():
    print("Call Complaint BPMN Simulation")
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    call_center = simpy.Store(env)

    for i in range(NUM_AGENTS):
        agent = Agent(i, env, call_center)
        env.process(agent.agent_process())

    env.process(generate_calls(env, NUM_CALLS, call_center))
    env.run(until=SIM_TIME)

if __name__ == '__main__':
    main()


