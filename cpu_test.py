import psutil
from functools import reduce
from operator import add,truediv

temps = psutil.sensors_temperatures()
cpu = temps['coretemp']
cpuAvgTemp = int(truediv(reduce(add,list(map(lambda v: v.current,cpu))), len(cpu)))


print(temps)
amdGPU = temps['amdgpu']
