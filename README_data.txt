The data have been collected for about 14600 restaurants in Paris from the TripAdvisor page 
https://www.tripadvisor.com/Restaurants-g187147-Paris_Ile_de_France.html

A Python script has been used to scrape the data: tripadvisor_scraper.py
The data are in the file restaurants.csv
These files can be found in the Github repository: https://github.com/drocca/TripAdvisor

At this early exploratory stage a limited amount of data has been collected from the page of each restaurant. 
The file restaurants.csv is structured in the following way:   
-Each line corresponds to a different restaurant
-First column: name of the restaurant
-Second column: type of cuisine 
-All the other columns correspond to the different languages supported by TripAdvisor (French,English,Italian,Chinese,Arabic,Czech,Danish,Dutch,German,Greek,Hebrew,Hungarian,Indonesian,Japanese,Korean,Norwegian,Polish,Portuguese,Russian,Serbian,Slovak,Spanish,Swedish,Thai,Turkish,Vietnamese)
-For each restaurant and language the number of reviews has been collected
