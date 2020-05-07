import gym
import math
from gym import spaces
import perception
import physics
import kirajzolas
import numpy as np


class Kisauto(gym.Env):

	def __init__(self):  # egyetlenegy alkalommal használjuk, nem kell értelmes értékeket adni még
		self.pos = (0, 0, 0)
		self.reward = 0.0
		self.info = {}
		self.i = 0
		self.observation_space = spaces.Box(low=np.ones(len(kirajzolas.SearchLineAngles)+1)*(-2),
											high=np.ones(len(kirajzolas.SearchLineAngles)+1)*2, dtype=np.float32)
		self.init_space = spaces.Box(low=np.ones(len(kirajzolas.SearchLineAngles)+1)*(-2),
											high=np.ones(len(kirajzolas.SearchLineAngles)+1) * 2, dtype=np.float32)
		self.action_space = spaces.Box(low=np.array([-1.0,-1.0]), high=np.array([1.0,1.0]), dtype=np.float32)
		self.steps = 0
		self.distTraveled = 0

	def step(self, command):  # ez fut a modellben minden lépésben
		self.steps += 1
		speed = physics.speed+0.1*command[0]
		self.distTraveled += speed
		self.pos = physics.move(self.pos[0], self.pos[1], self.pos[2], 0.5*command[0], 0.4*command[1])
		obs = np.append(normalize(perception.calcDistances(self.pos[0], self.pos[1], self.pos[2])), [speed])

		#TODO: ezt jól megírni, bár most jónak tűnik
		reward = 1 - math.exp(-speed/100)
		return [np.copy(obs), reward, physics.collision, self.info] # a háló bemenete, jutalom, vége van-e (ütközés), random info

	def reset(self):  # ha vége a szimulációnak, ez állít alaphelyzetbe ismét
		self.steps = 0
		self.distTraveled = 0
		self.i = kirajzolas.nextTrackIndex()
		self.pos = (kirajzolas.tracks[self.i].startPos[0], kirajzolas.tracks[self.i].startPos[1],
				kirajzolas.tracks[self.i].startDir)
		physics.reset()
		self.info = {}
		self.reward = 0.0
		obs = np.append(perception.calcDistances(self.pos[0], self.pos[1], self.pos[2]),[physics.speed])
		return obs

	def render(self, mode='human', close=False):  # kirajzolás
		kirajzolas.drawPalya(self.pos[0], self.pos[1], self.pos[2])


def normalize(array):
	centered=array-np.average(array)
	return centered/np.std(centered)