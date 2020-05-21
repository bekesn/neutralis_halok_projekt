import gym
import math
from gym import spaces
import perception
import physics
import kirajzolas
import numpy as np


class Kisauto(gym.Env):

	def __init__(self):  # egyetlenegy alkalommal használjuk, nem kell értelmes értékeket adni még
		self.state = (0, 0, 0, 0)
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
		self.state = physics.move(self.state[0], self.state[1], self.state[2], 0.5 * command[0], 0.4 * command[1])
		speed = physics.speed
		self.distTraveled += speed
		obs = np.append(normalize(perception.calcDistances(self.state[0], self.state[1], self.state[2])), [speed])

		self.centerized = 0.4*perception.centerized(self.state[0], self.state[1])+0.6*self.centerized
		#TODO: ezt jól megírni, bár most jónak tűnik
		self.reward= 0.04*max(-2,1-math.exp(1-speed*20))+0.96*min(1,math.exp((self.centerized*(speed>0)-1)*12))
		return [np.copy(obs), self.reward, self.state[3], self.info] # a háló bemenete, jutalom, vége van-e (ütközés), random info

	def reset(self):  # ha vége a szimulációnak, ez állít alaphelyzetbe ismét
		self.steps = 0
		self.distTraveled = 0
		self.i = kirajzolas.nextTrackIndex()
		self.state = (kirajzolas.tracks[self.i].startPos[0], kirajzolas.tracks[self.i].startPos[1],
				kirajzolas.tracks[self.i].startDir, 0)
		physics.reset()
		self.centerized = perception.centerized(self.state[0], self.state[1])
		self.info = {}
		self.reward = 0.0
		obs = np.append(normalize(perception.calcDistances(self.state[0], self.state[1], self.state[2])),[physics.speed])
		return obs

	def render(self, mode='human', close=False):  # kirajzolás
		kirajzolas.drawPalya(self.state[0], self.state[1], self.state[2])


def normalize(array):
	centered=array-np.average(array)
	return centered/np.std(centered)