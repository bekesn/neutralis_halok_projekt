import gym
import math
from gym import spaces
import perception
import map
import numpy as np


class Matchbox(gym.Env):

	# parameters of the car and simulation
	wheelBase = 20
	trackWidth = 10
	slipEnabled = True  	# False / True
	g = 9.81
	mu = 1.5  				# Friction coefficient
	px = 5 					# px/s to m/s
	pr = 10  				# m to px
	rand = 10
	skid_factor = 4  		# Defines changing of skid
	max_acceleration = 0.05
	speedlimit = 4
	turnLimit = 0.3  		# math.pi/4

	SearchLineAngles = []	# the angles where distances are measured

	# status of car
	x=0
	y=0
	speed = 0.0
	direction=0.0			# angle in rad
	slip = 0
	collision = False
	skid = 0.0
	turn = 0.0
	throttle = 0.0

	SearchLineDistances = []  # measured distances

	i = 0					# index of track


	def __init__(self, n=9):
		self.init_searchlines(n)
		self.observation_space = spaces.Box(low=np.ones(n+1)*(-2), high=np.ones(n+1)*2, dtype=np.float32)
		self.init_space = spaces.Box(low=np.ones(n+1)*(-2), high=np.ones(n+1) * 2, dtype=np.float32)
		self.action_space = spaces.Box(low=np.array([-1.0,-1.0]), high=np.array([1.0,1.0]), dtype=np.float32)
		self.info = {}

	# when training, this method is called every step, returning state, reward, terminal bool
	def step(self, command):
		# perform a step in the simulation
		self.steps += 1
		self.move(0.5 * command[0], 0.4 * command[1])

		# calculating reward
		obs = np.append(self.normalize(perception.calcDistances(self)), [self.speed])
		self.perf = 0.6*perception.performance(self)+0.4*self.perf
		self.reward= 0.04*max(-2,1-math.exp(1-self.speed*20))+0.96*min(1,math.exp((self.perf*(self.speed>0)-1)*12))
		return [np.copy(obs), self.reward, self.collision, self.info]

	# reset after each episode
	def reset(self):
		# reset status
		self.slip = 0
		self.collision = False
		self.skid = 0.0
		self.speed = 0.0
		self.turn = 0.0
		self.throttle = 0.0
		self.distTraveled = 0
		self.steps = 0
		self.reward = 0.0
		self.collision=False

		# placing car on other track
		self.i = map.nextTrackIndex()
		self.x=map.tracks[self.i].startPos[0]
		self.y=map.tracks[self.i].startPos[1]
		self.direction=map.tracks[self.i].startDir

		# calculating reward
		self.perf = perception.performance(self)
		obs = np.append(self.normalize(perception.calcDistances(self)),[self.speed])
		return obs

	# visualize environment
	def render(self, mode='human', close=False):
		map.drawEnv(self)

	# preprocessing the distances
	def normalize(self, array):
		centered=array-np.average(array)
		return centered/np.std(centered)

	# simplified physics of car
	def move(self,throttle, turn):
		self.turn = min(max(turn, -self.turnLimit), self.turnLimit)
		self.throttle = throttle
		self.speed = self.speed + throttle
		if self.speed > self.speedlimit:
			self.speed = self.speedlimit
		elif self.speed < -self.speedlimit:
			self.speed = -self.speedlimit
		self.slip = 0
		if self.turn == 0:
			self.x += math.sin(self.direction) * self.speed
			self.y += math.cos(self.direction) * self.speed
			self.skid = 0.0  # Ebben az esetben nem csúszik az autó
		else:
			rad = self.wheelBase / math.tan(self.turn)
			rad = math.sqrt(rad * rad + self.wheelBase * self.wheelBase / 4) * self.turn / abs(self.turn)
			origo = (self.x + math.cos(self.direction) * rad, self.y - math.sin(self.direction) * rad)
			v_max = math.sqrt(self.g * self.mu * abs(rad / self.pr))
			rad_min = self.speed * self.speed * self.px * self.px * self.pr / (self.g * self.mu)
			if self.slipEnabled and self.speed * self.px > v_max:
				if abs(rad) + self.skid < rad_min:  # Addig növeljük a csúszás értékét, amíg a megfelelő körpályára kerül
					mrad = rad / (abs(rad) + self.skid)
				else:
					mrad = rad / rad_min
					self.skid = rad_min - abs(
						rad) + 10  # Amint a megfelelő körpályán vagyunk, nem változik az értéke. 10 := biztonsági tényező
				# print(v_max, rad, rad_min, skid, mrad)
				self.x += math.sin(self.direction) * self.speed
				self.y += math.cos(self.direction) * self.speed
				self.direction = self.direction + self.speed / rad * abs(mrad)  # Ezzel a képlettel adjuk meg a csúszás mértékét
				self.slip = 1 - abs(mrad)
			else:
				self.skid = 0.0  # Ebben az esetben nem csúszik az autó
				self.direction = self.direction + self.speed / rad
				self.x = origo[0] - math.cos(self.direction) * rad
				self.y = origo[1] + math.sin(self.direction) * rad
		self.skid = self.skid + abs(self.speed) * self.skid_factor  # Csúszás értékének meghatározása a sebesség függvényében
		self.distTraveled += self.speed

	# defining the directions to measure distances
	def init_searchlines(self, n, angle1=-math.pi / 2, angle2=math.pi / 2):  # n vonal, szögtartomány: angle1-től angle2-ig
		self.SearchLineDistances = [0 for i in range(n)]
		self.SearchLineAngles = [0 for i in range(n)]
		for i in range(n):
			self.SearchLineAngles[i] = angle1 + (angle2 - angle1) * float(i) / float(n - 1)