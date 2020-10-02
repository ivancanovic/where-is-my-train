# Making sure that we always send in params today's date correctly formated in order to avoid fluding with irelevant data for journeys in near future
  today = date.today()
  journey_date = today.strftime("%d%m%y")