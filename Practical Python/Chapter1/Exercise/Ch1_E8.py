# mortgage.py
principal=500000.0
rate=0.05
payment=2684.11
extra_payment=1000.0
extra_period=12
total_paid=0.0
total_months=1

while principal>0:
    principal=principal*(1+rate/12)-payment
    if total_months<=extra_period:
        principal-=extra_payment
    total_months+=1
    total_paid+=payment
total_paid+=extra_payment*min(total_months,extra_period)

print('Total months', total_months-1, 'Total paid', total_paid)