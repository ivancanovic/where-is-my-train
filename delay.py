  # Checking if there is a delay, and there is, converting response from seconds to minutes
  delay_check = int(delay)
  if delay_check != 0:
    delay_update = ("delayed " + str(int(delay_check / 60)) + " min")
  else:
    delay_update = "on time"