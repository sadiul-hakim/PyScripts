import psutil

print(f"Number of logical CPUs: {psutil.cpu_count(logical=True)}")
