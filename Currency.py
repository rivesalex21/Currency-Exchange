import pandas as pd
from urllib import request

URL = 'https://www.federalreserve.gov/datadownload/\
Output.aspx?rel=H10&series=60f32914ab61dfab590e0e470153e3ae&lastobs=10&\
from=&to=&filetype=csv&label=include&layout=seriescolumn&type=package'

try:
    path != None
except:
    path,_ = request.urlretrieve(URL)
df = pd.read_csv(path)

# Renaming the columns:
def columnNames(columnName):
    # Notice that most countries are seperated by a double hyphen
    if '--' in columnName:
        splitName = columnName.split('--')
        return splitName[0].strip().upper()
    if '-' in columnName:
        splitName = columnName.split('-')
        return splitName[1].strip().upper()
    
    splitName = columnName.split(' ')
    return splitName[0].strip().upper()

def rowUnit(rows):
    return rows.split('_Per_')[-1]

df.rename(columns=columnNames, inplace=True)
df = df.transpose()
df[0] = df[0].apply(rowUnit)
df = df.transpose()

Final = df.loc[[0,2,df.index[-1]]]
Final.drop(columns = 'SERIES',inplace=True)
Final = Final.transpose()

Final = Final.astype({df.index[-1]: float})

for index in Final.index:
    if Final.loc[index][0] != 'USD':
        
        currentCountry = Final.loc[index][0]
        newvalue = 1/Final.loc[index][14]
        
        Final.loc[index,0] = 'USD' 
        Final.loc[index,2] = currentCountry
        Final.loc[index,14] = round(newvalue,4)

Final.rename(columns={0:'From',2:'To',14:'X_Rate'},inplace=True)
CountryDictionary = Final.transpose().to_dict()

class CountryCurrency:
    COUNTRIES = ['UNITED STATES']
    INFORMATION = {'UNITED STATES': {'From': 'USD', 'To': 'USD', 'X_Rate': 1.00} }
    RATES = {'USD':1.00}
    
    def __init__(self):
        self.Countries = None
        self.CountryInfo = None
        self.XCHANGE_RATES = None
    
    def getRate(self,Country):
        if self.Countries == None:
            return print('Please add countries to this function')
        if Country.upper() not in self.Countries:
            return print('Invalid country selection, you may need to add more')
        
        return print(f'The exchange rate of {Country} is {self.INFORMATION[Country.upper()]["X_Rate"]}')
    
    def addCountries(self,countryDict):
        if type(countryDict) != dict:
            print("Incorrect Data Type, must be a nested dictionary in the following format:")
            print('{COUNTRY: {From: COUNTRY_CURRENCY, To: USD, X_Rate: XCHANGE_RATE}}')
            return
        
        for cont in countryDict:
            keys = list(countryDict[cont].keys())
            if 'From' in keys and 'To' in keys and 'X_Rate' in keys and cont not in self.COUNTRIES:
                self.COUNTRIES.append(cont)  
                self.INFORMATION[cont] = countryDict[cont]
                self.RATES[countryDict[cont]['To']] = round(countryDict[cont]['X_Rate'],4)
        self.Countries = self.COUNTRIES
        self.CountryInfo = self.INFORMATION
        self.XCHANGE_RATES = self.RATES
    
    def xchangeRateByCurrency(self,from_currency, to_currency):
        if from_currency.upper() not in self.RATES or to_currency.upper() not in self.RATES:
            return print('Invalid currency selection, use showRates method to see current rates')
        
        Xrate = round((1/self.RATES[from_currency.upper()]) * self.RATES[to_currency.upper()],4)
        print(f'The exchange rate from {from_currency.upper()} to {to_currency.upper()} is {Xrate}')
        return Xrate
    
    def xchangeRateByCountry(self,from_country, to_country):
        if from_country.upper() not in self.Countries or from_country.upper() not in self.Countries:
            return print('Invalid country selection, use showCountries method to see current countries')
        fromPrice = (1/self.CountryInfo[from_country.upper()]['X_Rate'])
        toPrice = (self.CountryInfo[to_country.upper()]['X_Rate'])
        
        Xrate = round(fromPrice*toPrice,4)
        print(f'The exchange rate from {from_country} to {to_country} is {Xrate}')
        return Xrate
    
    def xchangeAmountByCurrency(self,from_currency, to_currency,amount):
        if from_currency.upper() not in self.RATES or to_currency.upper() not in self.RATES:
            return print('Invalid currency selection, use showRates method to see current rates')
        fromPrice = 1/self.RATES[from_currency.upper()]
        toPrice = self.RATES[to_currency.upper()]
        Xrate = fromPrice * toPrice
        total = round(amount*Xrate,2)
        print(f'From {amount} {from_currency} to: {total} {to_currency.upper()}')
        return total
    
    def xchangeAmountByCountry(self,from_country, to_country, amount):
        if from_country.upper() not in self.Countries or from_country.upper() not in self.Countries:
            return print('Invalid country selection, use showCountries method to see current countries')
        
        fromPrice = (1/self.CountryInfo[from_country.upper()]['X_Rate'])
        toPrice = (self.CountryInfo[to_country.upper()]['X_Rate'])
        Xrate = fromPrice * toPrice
        
        total = round(amount*Xrate,2)
        print(f'{amount} {self.CountryInfo[from_country.upper()]["To"]} in {from_country} is worth {total} {self.CountryInfo[to_country.upper()]["To"]} in {to_country}')
        return total
        
    
    @property
    def showRates(self):
        return (self.RATES)
    @property 
    def showCountries(self):
        return self.COUNTRIES

'''
Xrates_2022_05_18 = CountryCurrency()
Xrates_2022_05_18.addCountries(CountryDictionary)
Xrates_2022_05_18.xchangeAmountByCurrency('USD','AUD',14000)
'''
