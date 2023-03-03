import pygame
import random
import matplotlib.pyplot as plt

# Define constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
AGENT_RADIUS = 5
AGENT_COUNT = 500
INITIAL_INFECTED_AGENT_COUNT = 50
INFECTION_RADIUS = 10
INFECTION_PROBABILITY = 0.5
INFECTION_DURATION = 10 # Infected remain sick for 10 days
RECOVERY_DURATION = 0 # Instantly become 'immune' if recovered
SIMULATION_DURATION = 365  # 1 year in days

# Define colors
COLOR_SUSCEPTIBLE = (0, 0, 255)  # Blue
COLOR_INFECTED = (255, 0, 0)    # Red
COLOR_RECOVERED = (0, 255, 0)   # Green
INTERVALED_COLOR_SUSCEPTIBLE = (0, 0, 255/255)
INTERVALED_COLOR_INFECTED = (255/255, 0, 0)
INTERVALED_COLOR_RECOVERED = (0, 255/255, 0)

# Useful for matplotlib
susceptible_list = []
infected_list = []
recovered_list = []

class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)
        self.state = 'susceptible'
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
        
        # Update the agent's state
        if self.state == 'infected':
            if day - self.infection_time > INFECTION_DURATION:
                self.state = 'recovered'
                self.recovery_time = day
        elif self.state == 'recovered':
            if day - self.recovery_time > RECOVERY_DURATION:
                self.state = 'immune'
    
    def draw(self, screen, day):
        if self.state == 'susceptible':
            color = COLOR_SUSCEPTIBLE
        elif self.state == 'infected':
            color = COLOR_INFECTED
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
        text = font.render("Susceptible", True, (0, 0, 0))
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
    s_count = 0
    i_count = 0
    r_count = 0
    for agent in agents:
        if agent.state == 'susceptible':
            s_count += 1
        if agent.state == 'infected':
            i_count += 1
        if agent.state == 'recovered' or agent.state == 'immune':
            r_count += 1
    susceptible_list.append(s_count)
    infected_list.append(i_count)
    recovered_list.append(r_count)

# Initialize pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('SIR Model Simulation')


agents = []
for i in range(AGENT_COUNT):
  x = random.randint(AGENT_RADIUS, SCREEN_WIDTH - AGENT_RADIUS)
  y = random.randint(AGENT_RADIUS, SCREEN_HEIGHT - AGENT_RADIUS)
  agent = Agent(x, y)
  agents.append(agent)

for i in range(INITIAL_INFECTED_AGENT_COUNT):
  agents[i].state = 'infected'
  agents[i].infection_time = 0


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
plt.plot(susceptible_list, color=INTERVALED_COLOR_SUSCEPTIBLE, label='Susceptible')
plt.plot(infected_list, color=INTERVALED_COLOR_INFECTED, label='Infected')
plt.plot(recovered_list, color=INTERVALED_COLOR_RECOVERED, label='Recovered')

plt.xlim([0, SIMULATION_DURATION])
plt.ylim(0, AGENT_COUNT)

plt.xlabel('Time (days)')
plt.ylabel('Number of agents')
plt.title('SIR Simulation')
plt.legend()

plt.show()
