Height=100.0
rate=0.6
for i in range(10):
    Height=Height*rate
    print(i+1,Height)
    
Height=100.0
# Use round() to round the height to 4 decimal places
for i in range(10):
    Height=Height*rate
    Height=round(Height,4)
    print(i+1,Height)