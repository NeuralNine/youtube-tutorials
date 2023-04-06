import random
import gym  # pip install gym==0.25.2

env = gym.make("CartPole-v1", render_mode="human")

episodes = 10
for episode in range(1, episodes+1):
    state = env.reset()
    done = False
    score = 0

    while not done:  # try alternatively while True to see full fail
        action = random.choice([0, 1])
        n_state, reward, done, info = env.step(action)  # in newer version five arguments (truncated between done and info)
        score += reward
        env.render()  # need pip install pyglet

    print(f"Episode; {episode} Score: {score}")

env.close()
