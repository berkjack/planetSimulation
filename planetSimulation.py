import pygame
import math
import time

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1080, 960
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

class Planet():
	AU = 149.6e6 * 1000 # Astronomical Unit, m
	G = 6.67428e-11 # Gravitational Constant (m^3)/(kg.s^2)
	SCALE = 250 / AU # 1AU = 100px
	TIMESTEP = 3600 * 24 # 1 day

	def __init__(self, x, y, radius, colour, mass):
		self.x = x
		self.y = y
		self.radius = radius
		self.colour = colour
		self.mass = mass

		self.orbit = []
		self.sun = False
		self.distanceToSun = 0

		self.xVel = 0
		self.yVel = 0

	def draw(self, win):
		x = self.x * self.SCALE + WIDTH / 2
		y = self.y * self.SCALE + HEIGHT / 2
		if len(self.orbit) > 2:
			updatedPoints = []
			for point in self.orbit:
				x, y = point
				x = x * self.SCALE + WIDTH / 2
				y = y * self.SCALE + HEIGHT / 2
				updatedPoints.append((x, y))

			pygame.draw.lines(win, self.colour, False, updatedPoints, 2)
		pygame.draw.circle(win, self.colour, (x, y), self.radius)


	def attraction(self, other):
		otherX, otherY = other.x, other.y
		distanceX = other.x - self.x
		distanceY = other.y - self.y
		distance = math.sqrt(distanceX**2 + distanceY**2)

		if other.sun:
			self.distanceToSun = distance

		force = self.G * self.mass * other.mass / distance**2
		theta = math.atan2(distanceY, distanceX)
		forceX = math.cos(theta) * force
		forceY = math.sin(theta) * force
		return forceX, forceY

	def updatePosition(self, planets):
		totalFX = totalFY = 0
		for planet in planets:
			if self == planet:
				continue

			fX, fY = self.attraction(planet)
			totalFX += fX
			totalFY += fY

		self.xVel += totalFX / self.mass * self.TIMESTEP # F = ma
		self.yVel += totalFY / self.mass * self.TIMESTEP # F = ma
		self.x += self.xVel * self.TIMESTEP
		self.y += self.yVel * self.TIMESTEP
		self.orbit.append((self.x, self.y))

def main():
	run = True
	clock = pygame.time.Clock()
	BLACK = (0, 0, 0)
	YELLOW = (255, 191, 0)
	BLUE = (40, 122, 184)
	RED = (156, 46, 53)
	DARKGREY = (80, 78, 81)
	WHITE = (255, 255, 255)

	sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
	sun.sun = True
	earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
	earth.yVel = 29.783 * 1000
	mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
	mars.yVel = 24.077 * 1000
	mercury = Planet(0.367 * Planet.AU, 0, 8, DARKGREY, 3.30 * 10**23)
	mercury.yVel = 47.4 * 1000
	venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
	venus.yVel = -35.02 * 1000
	planets = [sun, earth, mars, mercury, venus]

	music = pygame.mixer.Sound(file="aloneWithNumbers.wav")
	music.set_volume(0.6)
	music.play(loops=-1)
	
	time.sleep(6.5) #Daha verimli bir yolu bulunacak.

	while run:
		clock.tick(60)
		WIN.fill(BLACK)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		for planet in planets:
			planet.updatePosition(planets)
			planet.draw(WIN)

		pygame.display.update()
	
	pygame.quit()

main()
