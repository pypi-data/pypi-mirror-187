import math
import time
def lenconv(unit1,unit2,num1):   
    if unit1 == "cm" and unit2 == "m":
        ans = float(num1)/100    
        return ans   
    elif unit1 == "mm" and unit2 == "cm":
        ans = float(num1)/10
        return ans
    elif unit1 == "m" and unit2 == "cm":
        ans = float(num1)*100
        return ans
    elif unit1 == "cm" and unit2 == "mm":
        ans = float(num1)*10
        return ans
    elif unit1 == "mm" and unit2 == "m":
        ans = float(num1)/1000
        return ans
    elif unit1 == "m" and unit2 == "mm":
        ans = float(num1)*1000  
        return ans
    elif unit1 == "km" and unit2 == "m":
        ans = float(num1)*1000
        return ans
    elif unit1 == "m" and unit2 == "km":
        ans = float(num1)/1000
        return ans
    elif unit1 == "mm" and unit2 == "km":
        ans = float(num1)/1000000
        return ans