import csv
import matplotlib.pyplot as plt
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

def showGraphicLanguages():
    db = connectMongo()
    surveysCollection = getCollection('stackoverflow', db)
    data = {}
    languages = []
    while 1:
        language = input("Enter the language to compare: ")
        languages.append(language)
        if(input("Add another language? (y/n): ") == 'n'):
            break
    for language in languages:
        surveys = surveysCollection.find({"languages": language})
        surveysCount = surveysCollection.count_documents({"languages": language})
        sumSalary = 0
        for survey in surveys:
            if survey.get("salary") != "NA":
                salary = survey.get("salary").replace(',', '')
                sumSalary += float(salary)
        data[language] = sumSalary/surveysCount
    names = list(data.keys())
    values= list(data.values())
    plt.bar(names, values, width=0.5)
    plt.title('Salario Promedio En estados unidos')
    plt.xlabel('Language')
    plt.ylabel('Salario promedio')
    plt.show()

def main(): 
    while 1:
        print("1.-Init The Data\n2.-Salary comparison programming languages\n3.-Exit")
        option = input("Enter the option: ")
        if option == '3':
            break
        switcher = {
            "1": initData,
            "2": showGraphicLanguages
        }
        operation = switcher.get(option, lambda: "Invalid operation")
        operation()
    
main()
