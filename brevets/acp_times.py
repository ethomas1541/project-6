"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow
from math import modf

#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#

# Brevet table as determined by the algorithm above.
# Originally stored as a tuple of tuples. This is not necessary because min speeds are always either
# 15km/h or 11.428. Not enough data to warrant storage in a tuple, or even a loop.

brev_table = (
   (200, 15,      34),
   (200, 15,      32),
   (200, 15,      30),
   (400, 11.428,  28),
   (300, 13.333,  26)
)

# Nominal brevet lengths, as shown in the docstrings below
valid_brev_lens = (200, 300, 400, 600, 1000)

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
   """
   Args:
      control_dist_km:  number, control distance in kilometers
      brevet_dist_km: number, nominal distance of the brevet
         in kilometers, which must be one of 200, 300, 400, 600,
         or 1000 (the only official ACP brevet distances)
      brevet_start_time:  An arrow object
   Returns:
      An arrow object indicating the control open time.
      This will be in the same time zone as the brevet start time.
   """ 

   if 0 <= control_dist_km <= 1200 and brevet_dist_km in valid_brev_lens and control_dist_km <= brevet_dist_km * 1.2:
      # Time shift expressed as decimal hours (1.5 = 1 hour 30 min)
      timeshift_decimal = 0

      # Subtract from this to iterate through the fields of the chart as shown on the website
      cdist_composite = control_dist_km
      for i in range(5):

         if cdist_composite > brev_table[i][0]:
            timeshift_decimal += brev_table[i][0]/brev_table[i][2]
            print(f"{i}\t{brev_table[i][0]}/{brev_table[i][2]} -> {timeshift_decimal}")
         else:
            timeshift_decimal += cdist_composite/brev_table[i][2]
            print(f"{i}\t{cdist_composite}/{brev_table[i][2]} -> {timeshift_decimal}")
         cdist_composite -= brev_table[i][0]
         if cdist_composite <= 0:
            break

      # Break it into an integer and decimal component
      tshift_parts = modf(timeshift_decimal)

      # For debugging
      print(f"{round(tshift_parts[1])}H{str(round(tshift_parts[0] * 60)).zfill(2)}")

      return brevet_start_time.shift(hours = round(tshift_parts[1]), minutes = round(tshift_parts[0] * 60))

   elif not 0 <= control_dist_km <= 1200:
      raise OverflowError
   
   elif brevet_dist_km not in valid_brev_lens:
      raise IndexError
   
   elif control_dist_km > brevet_dist_km * 1.2:
      raise ArithmeticError

def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
   """
   Args:
      control_dist_km:  number, control distance in kilometers
         brevet_dist_km: number, nominal distance of the brevet
         in kilometers, which must be one of 200, 300, 400, 600, or 1000
         (the only official ACP brevet distances)
      brevet_start_time:  An arrow object
   Returns:
      An arrow object indicating the control close time.
      This will be in the same time zone as the brevet start time.
   """

   if 0 <= control_dist_km <= 1200 and brevet_dist_km in valid_brev_lens and control_dist_km <= brevet_dist_km * 1.2:
      # Time shift expressed as decimal hours (1.5 = 1 hour 30 min)
      timeshift_decimal = 0

      cdist_composite = control_dist_km

      for i in range(5):

         if cdist_composite > brev_table[i][0]:
            timeshift_decimal += brev_table[i][0]/brev_table[i][1]
            print(f"{i}\t{brev_table[i][0]}/{brev_table[i][1]} -> {timeshift_decimal}")
         else:
            timeshift_decimal += cdist_composite/brev_table[i][1]
            print(f"{i}\t{cdist_composite}/{brev_table[i][1]} -> {timeshift_decimal}")
         cdist_composite -= brev_table[i][0]
         if cdist_composite <= 0:
            break

      # Break apart
      tshift_parts = modf(timeshift_decimal)

      # Debugging
      print(f"{round(tshift_parts[1])}H{str(round(tshift_parts[0] * 60)).zfill(2)}")

      print(brevet_start_time.shift(hours = round(tshift_parts[1]), minutes = round(tshift_parts[0] * 60)))

      return brevet_start_time.shift(hours = round(tshift_parts[1]), minutes = round(tshift_parts[0] * 60))

   elif not 0 <= control_dist_km <= 1200:
      raise OverflowError
   
   elif not brevet_dist_km in valid_brev_lens:
      raise IndexError
   
   elif control_dist_km > brevet_dist_km * 1.2:
      raise ArithmeticError
   
if __name__ == "__main__":
   open_time(1140, 1000, arrow.get('1970-01-01T00:00:00+00:00'))
   close_time(1140, 1000, arrow.get('1970-01-01T00:00:00+00:00'))