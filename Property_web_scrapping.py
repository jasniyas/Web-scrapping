"""
Title: Property_web_scrapping.py
Description: A program that scraps real estate property data from the web.
Date: 04/28/2018
Python version: 3.6.4
Execution: python Property_web_scrapping.py
"""

# import relevant libraries.
import requests, pandas
from bs4 import BeautifulSoup

# Request data from the webpage desired to scrape.
r = requests.get("https://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/")
content = r.content

# Assign all html data of webpage to a variable.
soup = BeautifulSoup(content, "html.parser")

# Get number of pages in the website.
page_nr = soup.find_all("a", {"class": "Page"})[-1].text
print("Number of pages found:", page_nr)

# Create a dictionary with property info for each listing.
# Create a list of all dictionaries by crawling through each page in the website.

list = []
base_url = "https://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
for page in range(0, int(page_nr)*10, 10):
    print(base_url + str(page))
    r = requests.get(base_url + str(page) + ".html")
    content = r.content
    soup = BeautifulSoup(content, "html.parser")
    all = soup.find_all("div", {"class": "propertyRow"})

    for item in all:
        dict = {}
        dict["Address"] = item.find_all("span", {"class": "propAddressCollapse"})[0].text
        try:
            dict["Locality"] = item.find_all("span", {"class": "propAddressCollapse"})[1].text
        except:
            dict["Locality"] = None

        try:
            dict["Price"] = item.find("h4", {"class": "propPrice"}).text.replace("\n", "")
        except:
            dict["Price"] = None

        try:
            dict["Beds"] = item.find("span", {"class": "infoBed"}).find("b").text
        except:
            dict["Beds"] = None

        try:
            dict["Area"] = item.find("span", {"class": "infoSqFt"}).find("b").text
        except:
            dict["Area"] = None

        try:
            dict["Full Baths"] = item.find("span", {"class": "infoValueFullBath"}).find("b").text
        except:
            dict["Full Baths"] = None

        try:
            dict["Half Baths"] = item.find("span", {"class": "infoValueHalfBath"}).find("b").text
        except:
            dict["Half Baths"] = None

        for column_group in item.find_all("div", {"class": "columnGroup"}):
            for feature_group, feature_name in zip(column_group.find_all("span", {"class": "featureGroup"}),
                                                   column_group.find_all("span", {"class": "featureName"})):
                if "Lot Size" in feature_group.text:
                    dict["Lot Size"] = feature_name.text

        list.append(dict)

# Create a pandas dataframe using the list of dictionaries.
df = pandas.DataFrame(list)

# Convert dataframe to a .CSV file.
df.to_csv("Output.csv")