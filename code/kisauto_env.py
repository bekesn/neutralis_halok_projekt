import gym
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
		self.info = {'a': 0, 'b': 0} #TODO kókány
		self.i = 0
		self.observation_space = spaces.Box(low=np.zeros(len(kirajzolas.SearchLineAngles)),
											high=np.ones(len(kirajzolas.SearchLineAngles))*1000)
		self.init_space = spaces.Box(low=np.zeros(len(kirajzolas.SearchLineAngles)),
											high=np.ones(len(kirajzolas.SearchLineAngles)) * 1000)
		self.action_space = spaces.Box(low=np.array([-0.5]), high=np.array([0.5]))

	def step(self, command):  # ez fut a modellben minden lépésben
		self.pos = physics.move(self.pos[0], self.pos[1], self.pos[2], 0.01, command)
		#print(command)
		obs = np.array(perception.calcDistances(self.pos[0], self.pos[1], self.pos[2]))
		self.reward = self.reward+0.0001 #TODO: ezt jól megírni, most lépésekkel nő
		return [obs, self.reward, physics.collision, self.info] # a háló bemenete, jutalom, vége van-e (ütközés), random info

	def reset(self):  # ha vége a szimulációnak, ez állít alaphelyzetbe ismét
		self.i = kirajzolas.nextTrackIndex()
		self.pos = (kirajzolas.tracks[self.i].startPos[0], kirajzolas.tracks[self.i].startPos[1],
				kirajzolas.tracks[self.i].startDir)
		physics.reset()
		self.info = {'a': 0, 'b': 0}#TODO kókány
		self.reward = 0.0
		self.obs = perception.calcDistances(self.pos[0], self.pos[1], self.pos[2])
		return self.obs

	def render(self, mode='human', close=False):  # kirajzolás
		kirajzolas.drawPalya(self.pos[0], self.pos[1], self.pos[2])
