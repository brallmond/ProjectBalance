import calendar
from datetime import date

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--bal', help='enter starting balance')
parser.add_argument('--payday', help='enter numerical day of your next paycheck')
parser.add_argument('--avgWeeklyExp', help='True/False include average weekly expenses', default=False)
args = parser.parse_args()

# options, add arg parse w defaults for paycheck
balance = float(args.bal)
paycheckAmt = 873.67
paycheckDay = int(args.payday)
addWeeklyExpenses = bool(args.avgWeeklyExp) # should be input variable

paycheckFreq = "biweekly" #arg parse for monthly version as well

# get today's date
currentMonth = date.today().month
currentDay = date.today().day

# make list of months, days, and weekdays
cal = calendar.Calendar(6) #tells cal that start of the week is Sunday
fullCalendar = []
for month in range(currentMonth,12+1):
  for day, weekday in cal.itermonthdays2(2022, month):
    if day != 0:
      if (month == currentMonth):
        if (day >= currentDay):
          fullCalendar.append((month,day,weekday))
      if (month != currentMonth):
        fullCalendar.append((month,day,weekday))

# make list of paydays
paydays = []
dayCount = 0
for month, day, weekday in fullCalendar:
  if ((not (day == currentDay and month == currentMonth)) \
     and ((day == paycheckDay and len(paydays) == 0) or dayCount == 14)):
    paydays.append((month,day))
    dayCount = 0
  dayCount += 1

print("paydays")
print(paydays)

# make list of static charges from csv
import pandas
df = pandas.read_csv('DaysAndCharges.csv')
listOfDays = df["Day"].tolist()
listOfCharges = df["Charge"].tolist()
recurringCharges = [(listOfDays[i], float(listOfCharges[i])) for i in range(0,len(listOfDays))]
#print(recurringCharges)

# anticipated one-time costs
oneTimeExpenses = [(1,20,-500)]

# averaged weekly expenses
groceryWeeklyCost = 50
restarauntWeeklyCost = 28
coffeeWeeklyCost = 12

print("projected costs")
prevBalance = -1
for month, day, weekday in fullCalendar:

  if month > (currentMonth + 2): break

  # recurring charges
  for dayRC, chargeRC in recurringCharges:
    if dayRC == day:
      balance += chargeRC  

  # paychecks
  for monthPD, dayPD in paydays:
    if (monthPD == month and dayPD == day):
      balance += paycheckAmt


  # weekly predicted costs
  # grocery avg is 200 per month
  # restraunt avg is 150 per month
  # ignoring coffee avg (we're significantly reducing it)
  if (addWeeklyExpenses):
    # every Sunday, $40 at dillons for groceries
    if (weekday == 6): balance -= groceryWeeklyCost
    # every Monday, $20 at AJs for beer, $8 for union lunch on Fridays
    if (weekday == 0): balance -= restarauntWeeklyCost
    # every Tuesday, $12 for avg weekly coffees
    if (weekday == 1): balance -= coffeeWeeklyCost
  
  # anticipated one time costs
  for monthOTE, dayOTE, chargeOTE in oneTimeExpenses:
    if ( (monthOTE == month) and (dayOTE == day) ):
      balance += chargeOTE

  # print output each day balance changes
  if prevBalance != balance:
    print("{} {}: {:.2f}".format(month, day, balance))
  prevBalance = balance
