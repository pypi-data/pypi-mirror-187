#temperature
def tempconv(unit1,unit2,num1):
    if unit1=="faherenheit" and unit2=="celsius":
        cel=((num1-32)*5)/9
        return cel
    elif unit1=="celsius" and unit2=="faherenheit":
        fah=(num1*(9/5))+32
        return fah
    elif unit1=="kelvin" and unit2=="celsius":
        cel=num1-273.15
        return cel
    elif unit1=="celsius" and unit2=="fahrenheit":
        kel=num1+273.15
        return kel
    elif unit1=="kelvin" and unit2=="fahrenheit":
        fah=(((num1-273.15)*9 )/5) +32
        return fah
    elif unit1=="fahrenheit" and unit2=="kelvin":
        kel=((9/5)(num1-273.15))+32