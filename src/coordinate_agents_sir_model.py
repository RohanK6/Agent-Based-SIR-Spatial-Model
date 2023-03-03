import pygame
import random
import matplotlib.pyplot as plt

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
AGENT_RADIUS = 5
AGENT_COUNT = 150
INITIAL_INFECTED_AGENT_COUNT = 30
INFECTION_RADIUS = 10
INFECTION_PROBABILITY = 0.5
INFECTION_DURATION = 20  # Infected remain sick for 20 days
INFECTION_DURATION_IMMUNOCOMPROMISED = 30  # Immunocompromised infected remain sick for 30 days
RECOVERY_DURATION = 0  # Instantly become 'immune' if recovered
SIMULATION_DURATION = 365  # 1 year in days

# Define colors
COLOR_SUSCEPTIBLE = (0, 0, 255)  # Blue
COLOR_SUSCEPTIBLE_IMMUNOCOMPROMISED = (160, 32, 240)  # Purple
COLOR_INFECTED = (255, 0, 0)  # Red
COLOR_RECOVERED = (0, 255, 0)  # Green

INTERVALED_COLOR_SUSCEPTIBLE = (0, 0, 255 / 255)
INTERVALED_COLOR_IMMUNOCOMPROMISED = (168 / 255, 32 / 255, 240 / 255)
INTERVALED_COLOR_INFECTED = (255 / 255, 0, 0)
INTERVALED_COLOR_RECOVERED = (0, 255 / 255, 0)

# Useful for matplotlib
susceptible_normal_list = []
susceptible_immunocompromised_list = []
infected_list = []
recovered_list = []


class Agent:
    def __init__(self, x, y, immunocompromised=False):
        self.x = x
        self.y = y
        self.vx = random.uniform(-10, 10)
        self.vy = random.uniform(-10, 10)
        self.state = 'susceptible'
        if immunocompromised:
            self.immunocompromised = True
        else:
            self.immunocompromised = False
            self.infection_time = 0
            self.recovery_time = 0

    def update(self, agents, day):
        # Move the agent
        self.x += self.vx
        self.y += self.vy

        # Bounce the agent off the edges of the screen
        if self.x < AGENT_RADIUS or self.x > SCREEN_WIDTH - AGENT_RADIUS:
            self.vx *= -1
        if self.y < AGENT_RADIUS or self.y > SCREEN_HEIGHT - AGENT_RADIUS:
            self.vy *= -1

        # Check for collisions with other agents
        for other_agent in agents:
            if other_agent == self:
                continue
            distance = ((self.x - other_agent.x) ** 2 + (self.y - other_agent.y) ** 2) ** 0.5
            if distance < INFECTION_RADIUS:
                if other_agent.state == 'infected' and self.state != 'immune':
                    if random.random() < INFECTION_PROBABILITY:
                        self.state = 'infected'
                        self.infection_time = day
                        # Set the state of the other agent to infected
                        other_agent.state = 'infected'
                        other_agent.infection_time = day
                        break
                    elif other_agent.state == 'immune' and self.state == 'infected':
                        # Skip infection check if other agent is immune and self is infected
                        break
                    elif other_agent.state == 'susceptible' and self.immunocompromised and not other_agent.immunocompromised:
                        if random.random() < INFECTION_PROBABILITY * 2:
                            self.state = 'infected'
                            self.infection_time = day
                            # Set the state of the other agent to infected
                            other_agent.state = 'infected'
                            other_agent.infection_time = day
                            break

            # Update the agent's state
            if self.state == 'infected':
                if self.immunocompromised:
                    if day - self.infection_time > INFECTION_DURATION_IMMUNOCOMPROMISED:
                        self.state = 'recovered'
                        self.recovery_time = day
                else:
                    if day - self.infection_time > INFECTION_DURATION:
                        self.state = 'recovered'
                        self.recovery_time = day
            elif self.state == 'recovered':
                if day - self.recovery_time > RECOVERY_DURATION:
                    self.state = 'immune'

    def draw(self, screen, day):
        if self.state == 'susceptible':
            if self.immunocompromised:
                color = COLOR_SUSCEPTIBLE_IMMUNOCOMPROMISED
                pygame.draw.circle(screen, color, (int(self.x), int(self.y)), AGENT_RADIUS)
            else:
                color = COLOR_SUSCEPTIBLE
                pygame.draw.circle(screen, color, (int(self.x), int(self.y)), AGENT_RADIUS)
        elif self.state == 'infected':
            color = COLOR_INFECTED
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), AGENT_RADIUS * 1.5)
        else:
            color = COLOR_RECOVERED
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), AGENT_RADIUS)

        # Display the day on the screen
        font = pygame.font.Font(None, 36)
        day_text = font.render(f"Day {day}", True, (0, 0, 0))
        screen.blit(day_text, (10, 10))

        # Draw key
        font = pygame.font.Font(None, 24)

        color_rect_size = 20
        color_rect_x = 10
        color_rect_y = SCREEN_HEIGHT - 150

        # Draw susceptible key
        pygame.draw.rect(screen, COLOR_SUSCEPTIBLE, (color_rect_x, color_rect_y, color_rect_size, color_rect_size))
        text = font.render("Susceptible (Agent: Norma)", True, (0, 0, 0))
        screen.blit(text, (color_rect_x + color_rect_size + 10, color_rect_y))

        # Draw immunocompromised key
        color_rect_y += color_rect_size + 10
        pygame.draw.rect(screen, COLOR_SUSCEPTIBLE_IMMUNOCOMPROMISED,
                         (color_rect_x, color_rect_y, color_rect_size, color_rect_size))
        text = font.render("Susceptible (Agent: Immunocompromised)", True, (0, 0, 0))
        screen.blit(text, (color_rect_x + color_rect_size + 10, color_rect_y))

        # Draw infected key
        color_rect_y += color_rect_size + 10
        pygame.draw.rect(screen, COLOR_INFECTED, (color_rect_x, color_rect_y, color_rect_size, color_rect_size))
        text = font.render("Infected", True, (0, 20, 0))
        screen.blit(text, (color_rect_x + color_rect_size + 10, color_rect_y))

        # Draw recovered key
        color_rect_y += color_rect_size + 10
        pygame.draw.rect(screen, COLOR_RECOVERED, (color_rect_x, color_rect_y, color_rect_size, color_rect_size))
        text = font.render("Recovered", True, (0, 0, 0))
        screen.blit(text, (color_rect_x + color_rect_size + 10, color_rect_y))


def count_agents_states():
    s_normal_count = 0
    s_immunocomrpomised = 0
    i_count = 0
    r_count = 0
    for agent in agents:
        if agent.state == 'susceptible' and not agent.immunocompromised:
            s_normal_count += 1
        if agent.state == 'susceptible' and agent.immunocompromised:
            s_immunocomrpomised += 1
        if agent.state == 'infected':
            i_count += 1
        if agent.state == 'recovered' or agent.state == 'immune':
            r_count += 1
    susceptible_normal_list.append(s_normal_count)
    susceptible_immunocompromised_list.append(s_immunocomrpomised)
    infected_list.append(i_count)
    recovered_list.append(r_count)


# Initialize pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('SIR Model Simulation')

agents = []
for i in range(AGENT_COUNT):
    immunocompromised = random.choices([True, False], weights=[0.3, 0.7])[0]
    if immunocompromised:
        x = SCREEN_WIDTH - 50
        y = 50
    else:
        x = SCREEN_WIDTH - 50
        y = SCREEN_HEIGHT - 50
    agent = Agent(x, y, immunocompromised)
    agents.append(agent)

for i in range(INITIAL_INFECTED_AGENT_COUNT):
    agents[i].state = 'infected'
    agents[i].infection_time = 0
    agents[i].x = 50
    agents[i].y = 50

current_day = 0

clock = pygame.time.Clock()
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the agents
    for agent in agents:
        agent.update(agents, current_day)

    # Store the updated counts
    count_agents_states()

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the agents
    for agent in agents:
        agent.draw(screen, current_day)

    # Update the screen
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

    # Increment the timestamp by one day
    current_day += 1

    # Print the current day
    print(f"Day {current_day}")

    # Stop the simulation after 365 days
    if current_day > SIMULATION_DURATION:
        running = False

pygame.quit()

# Plot the SIR graph
plt.plot(susceptible_normal_list, color=INTERVALED_COLOR_SUSCEPTIBLE, label='Susceptible | Normal')
plt.plot(susceptible_immunocompromised_list, color=INTERVALED_COLOR_IMMUNOCOMPROMISED,
         label='Susceptible | Immunocompromised')
plt.plot(infected_list, color=INTERVALED_COLOR_INFECTED, label='Infected')
plt.plot(recovered_list, color=INTERVALED_COLOR_RECOVERED, label='Recovered')

plt.xlim([0, SIMULATION_DURATION])
plt.ylim(0, AGENT_COUNT)

plt.xlabel('Time (days)')
plt.ylabel('Number of agents')
plt.title('SIR Simulation')
plt.legend()

plt.show()