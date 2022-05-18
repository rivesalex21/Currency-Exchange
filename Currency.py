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
rdf = df.copy() # raw dataframe --> this is just for reference in the future

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
# The raw data shows the currency 
def rowUnit(rows):
    return rows.split('_Per_')[-1]

# Pass the columnNames function into the rename method, 
# this will change the names of the column into something easier to understand
df.rename(columns=columnNames, inplace=True)
df = df.transpose()

# Pandas is easier to work with using row by row operations
df[0] = df[0].apply(rowUnit)
df = df.transpose()

# Our 'Final' dataframe cuts down on the rows that we need.
# Rows 0, 2, [-1] correspond to the "from" currency, "to" currency, and latest exchange rate
Final = df.loc[[0,2,df.index[-1]]]
Final.drop(columns = 'SERIES',inplace=True)

# We transpose again to change the data type on the last column for our df.
Final = Final.transpose()
Final = Final.astype({df.index[-1]: float})

# To make the analysis and class creation easier, we make all "from" currencies equal USD, and 
# We apply the an inverse on the current exchange rate.
for index in Final.index:
    if Final.loc[index][0] != 'USD':
        
        currentCountry = Final.loc[index][0]
        newvalue = 1/Final.loc[index][df.index[-1]]
        
        Final.loc[index,0] = 'USD' 
        Final.loc[index,2] = currentCountry
        Final.loc[index,df.index[-1]] = round(newvalue,4)

# We rename out columns from what their indexes used to be to something intuitive
Final.rename(columns={0:'From',2:'To',df.index[-1]:'X_Rate'},inplace=True)

# The class is meant to take dictionaries as arguments, so we will transpose the df one more time
# this makes the countries the columns, it also makes our dictionary easier to read
# Final format should be: {Country: {From: XX, To: XX. X_Rate: XX}}
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

Xrates_2022_05_18 = CountryCurrency()
Xrates_2022_05_18.addCountries(CountryDictionary)
Xrates_2022_05_18.xchangeAmountByCurrency('USD','AUD',14000)
