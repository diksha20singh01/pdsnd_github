import time
import pandas as pd
import numpy as np
import datetime

#define the data dictionary for city
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
#define the list of values for month against which the input can be verified
MONTH_DATA =['all','january','february','march','april','may','june']
#define the list of values for day against which the input can be verified
DAY_DATA =['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs #text input into lower  --> .lower() .take a function and return 
    try:
        city=input("Would you like to see data for chicago, new york city, or washington? Please enter none if the country does not exists \n")
        month=input("Please enter a month from all, january, february, ... , june\n")
        day=input("Please enter a day of week from (all, monday, tuesday, ... sunday)\n")
        if city.lower() in CITY_DATA and month.lower() in MONTH_DATA and day.lower() in DAY_DATA :
            city=city.lower()
            month=month.lower()
            day=day.lower()
            print("You have entered city as {} and month as {} and day as {}".format, city,month,day)
        else:
            city='Error'
            month='Error'
            day='Error'
            print("Incorrect Input. Please start again")
    except Exception as e:
            print("Exception occurred: {}".format(e))     
    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
# load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
   
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month']==month]
        
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month
    common_month = df['month'].value_counts()
    print("the common month is :", common_month.index[0])

    # TO DO: display the most common day of week
    df['day'] = df['Start Time'].dt.day_name()
    #print(df['day'])
    common_day = df['day'].value_counts()
    print("the common day is :", common_day.index[0])

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].value_counts()
    print("The most common start hour is : ",common_hour.index[0])

    print("\nThis took %s seconds." % round((time.time() - start_time),1))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station_freq =df['Start Station'].value_counts()
    print("The most frequent start station is : ",start_station_freq.index[0])

    # TO DO: display most commonly used end station
    end_station_freq =df['End Station'].value_counts()
    print("The most frequent end station is : \n",end_station_freq.index[0])

    # TO DO: display most frequent combination of start station and end station trip with the total count
    #print(start_station.info())
    #print(end_station.info())
    grouped=df.groupby(['Start Station','End Station']).size().reset_index(name='count')
    grouped_sorted_data=grouped.sort_values(by='count', ascending=False)
    #print(grouped_sorted_data.head(1))
    print("The most frequent combination of start station and end station trip is : ",grouped_sorted_data.head(1))

    print("\nThis took %s seconds." % round((time.time() - start_time),1))
    print('-'*40)

def convert_seconds(seconds):
    """This function converts the seconds into hour mins and seconds"""
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return '%d hr :%02d min :%02d sec' % (hour, minutes, seconds)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time=df['Trip Duration'].sum()
    print("The total travel time is : " ,convert_seconds(total_travel_time))

    #TO DO: display mean travel time
    mean_travel_time=df['Trip Duration'].sum()/df['Trip Duration'].count()
    print("The mean travel time is : " ,convert_seconds(mean_travel_time))

    print("\nThis took %s seconds." % round((time.time() - start_time),1))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("The count of user types is as below : \n" ,df['User Type'].value_counts())
    
    if city != 'washington':
        # TO DO: Display counts of gender
        print("The count of gender is as below : \n" ,df['Gender'].value_counts())
        # TO DO: Display earliest, most recent, and most common year of birth
        birth_year_freq=df['Birth Year'].value_counts()
        print("The most common birth year is : ", int(birth_year_freq.index[0]))
        print("The earliest birth year is : ", int(df['Birth Year'].min()))
        print("The most recent birth year is : ", int(df['Birth Year'].max()))

    print("\nThis took %s seconds." % round((time.time() - start_time),1))
    print('-'*40)

def raw_data_display(df):
    """ Displays user data depending upon the input from user. 
    Initially it displays first 5 rows and then prompts user if the user wants to see next 5 rows """
    
    print('\n Displaying Raw Data...\n')
    start_time = time.time()
    i = 0
    raw_data_input = input("Would you like to see the raw data? yes or no?") 
    #converting the raw data into lowercase for case-insensitive comparison
    raw_data=raw_data_input.lower()
    #setting the max rows that the user can see
    pd.set_option('display.max_columns',200)

    while True:            
        if raw_data == 'no':
            break
        elif raw_data == 'yes':
            print(df.iloc[i:i+5]) # TO DO: appropriately subset/slice your dataframe to display next five rows
            raw_data_input = input("Would you like to see the raw data? yes or no?") 
            raw_data=raw_data_input.lower()
            i += 5
        else:
            raw_data = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()

    print("\nThis took %s seconds." % round((time.time() - start_time),1))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        #print(city)
        if city != 'Error' and month!='Error' and day!='Error':
            df = load_data(city, month, day)
            #print(df.describe())
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df,city) #exception
            raw_data_display(df)
            
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
        
if __name__ == "__main__":
	main()
