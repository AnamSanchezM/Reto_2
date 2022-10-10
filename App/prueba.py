
from time import strptime


fecha="   ".strip()
fecha=strptime(fecha,"%B %d, %Y")
print(fecha[0])
