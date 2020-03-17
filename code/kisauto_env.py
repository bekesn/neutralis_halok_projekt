import gym
import math
from gym import error, spaces, utils
from gym.utils import seeding
import perception
import physics
import kirajzolas
import numpy as np


class Kisauto(gym.Env):

	def __init__(self):  # egyetlenegy alkalommal használjuk, nem kell értelmes értékeket adni még
		self.pos = (0, 0, 0)
		self.reward = 0.0
		self.info = {'a': 0, 'b': 0}  #TODO kókány
		self.i = 0
		self.observation_space = spaces.Box(low=np.zeros(len(kirajzolas.SearchLineAngles)+1),
											high=np.ones(len(kirajzolas.SearchLineAngles)+1)*1000, dtype=np.float32)
		self.init_space = spaces.Box(low=np.zeros(len(kirajzolas.SearchLineAngles)+1),
											high=np.ones(len(kirajzolas.SearchLineAngles)+1) * 1000, dtype=np.float32)
		self.action_space = spaces.Box(low=np.array([-0.01,-0.4]), high=np.array([0.01,0.4]), dtype=np.float32)
		self.steps = 0
		self.distTraveled = 0

	def step(self, command):  # ez fut a modellben minden lépésben
		self.steps += 1
		speed = physics.speed+command[0]
		self.distTraveled += speed
		self.pos = physics.move(self.pos[0], self.pos[1], self.pos[2], command[0], command[1])
		obs = np.append(perception.calcDistances(self.pos[0], self.pos[1], self.pos[2]), [speed])
		#TODO: ezt jól megírni:
		#self.reward += np.amin(obs)*np.amin(obs)*self.distTraveled/math.sqrt(float(self.steps))/10000000  # nagy átlagsebesség
		reward = self.distTraveled/(1+(speed-1)*(speed-1))

		return [obs, reward, physics.collision, self.info] # a háló bemenete, jutalom, vége van-e (ütközés), random info

	def reset(self):  # ha vége a szimulációnak, ez állít alaphelyzetbe ismét
		self.steps = 0
		self.distTraveled = 0
		self.i = kirajzolas.nextTrackIndex()
		self.pos = (kirajzolas.tracks[self.i].startPos[0], kirajzolas.tracks[self.i].startPos[1],
				kirajzolas.tracks[self.i].startDir)
		physics.reset()
		self.info = {'a': 0, 'b': 0}#TODO kókány
		self.reward = 0.0
		obs = np.append(perception.calcDistances(self.pos[0], self.pos[1], self.pos[2]),[physics.speed])
		return obs

	def render(self, mode='human', close=False):  # kirajzolás
		kirajzolas.drawPalya(self.pos[0], self.pos[1], self.pos[2])
