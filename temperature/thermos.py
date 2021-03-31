import sys


count = sum = 0
devices = {}
for l in sys.stdin:
   if l.strip():
       try:
           (id, temp_str) = l.split()
           temp = int(temp_str)
           # print(f"{id}||{temp}")
           count += 1
           sum += temp
           devices[id] = temp
       except ValueError:
           print(l, file=sys.stderr)

avg = sum / count
print(f"average temp: {round(avg/1000, 1)}")

for id, temp in sorted(devices.items()):
    print(f"{id} {round(temp/1000, 1)} {round((temp - avg)/1000, 2)}")
