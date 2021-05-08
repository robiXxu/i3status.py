import GPUtil

gpus =  GPUtil.getGPUs()
nvidia = gpus[0]

print(f"{nvidia.temperature}°C")
