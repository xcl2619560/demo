#-*- coding: utf-8 -*-

from pylab import *

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
t = arange(-4*pi, 4*pi, 0.01)
y = sin(t)/t
plt.plot(t, y)
plt.title(u'钟形函数')
plt.xlabel(u'时间')
plt.ylabel(u'幅度')
plt.show()