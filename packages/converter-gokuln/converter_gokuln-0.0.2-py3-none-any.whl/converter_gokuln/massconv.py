#mass converter
def mconv(unit1,unit2,num1):
    if unit1=="kg" and unit2=="g":
        g=num1*1000
        return g
    elif unit1=="g" and unit2=="kg":
        kg=num1/1000
        return kg
    elif unit1=="mg" and unit2=="g":
        g=num1/1000
        return g
    elif unit1=="g" and unit2=="mg":
        mg= num1*10000
        return mg
