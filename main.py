import csv
from mongoConfig import *

def initData():
    db = connectMongo()
    count = 0
    stackOverflow = getCollection('stackoverflow', db)
    print("Loading...")
    languages = []
    with open('survey_results_public.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row["Country"] == "United States":
                if row["SalaryType"] == "Yearly":
                    rowLanguages = row["LanguageWorkedWith"].split(';')
                    for language in rowLanguages:
                        if language not in languages:
                            languages.append(language)
                    result = {
                    "country": row["Country"],
                    "salary": row["Salary"],
                    "languages": rowLanguages
                    }
                    count += 1
                    stackOverflow.insert_one(result)
    print('Finished')
    print(count)
    setLanguages(languages)

def setLanguages(languagesArr):
    db = connectMongo()
    languages = getCollection('languages', db)
    document = {
        "count": len(languagesArr),
        "languages": languagesArr
    }
    languages.insert_one(document)

def main(): 
    while 1:
        print("1.-Init The Data\n2.-Exit")
        option = input("Enter the option: ")
        switcher = {
            "1": initData
        }
        operation = switcher.get(option, lambda: "Invalid operation")
        operation()
    
main()
