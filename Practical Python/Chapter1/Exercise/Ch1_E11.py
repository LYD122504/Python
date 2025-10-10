# mortgage.py
principal=500000.0
rate=0.05
payment=2684.11
extra_payment=1000.0
extra_start_month=61
extra_end_month=108
total_paid=0.0
total_months=1

while principal>0:
    principal=principal*(1+rate/12)-payment
    if total_months<=extra_end_month and total_months>=extra_start_month:
        principal-=extra_payment
        total_paid+=extra_payment
    total_months+=1
    total_paid+=payment
    if principal<0:
        total_paid+=principal
        principal=0
    print(total_months-1, round(total_paid, 2), round(principal, 2))

print('Total months', total_months-1, 'Total paid', round(total_paid, 2))