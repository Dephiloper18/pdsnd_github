# No guarantee for functioning dataset of Washington

import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('For which city do you want to see the data? Data is available for Washington, New York City and Chicago: ')
    city = city.casefold()
    while city not in CITY_DATA: 
        city = input('The city name you have entered is invalid. Please enter again: ')
        city = city.casefold()


    # get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = input('Please enter the month you want to see the data for. Available are the months from January to June. You can also enter "all" to see the results for all six months. Month filter: ')
    month = month.casefold()
    while month not in months :
        month = input('Invalid entry for month. Please enter again: ')
        month = month.casefold()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    weekdays = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    weekday = input('Please enter the weekday you want to see the data for. Available are all weekdays. You can also enter "all" to see the results for all days. Weekday filter: ')
    weekday = weekday.casefold()
    while weekday not in weekdays:
        weekday = input('Invalid entry for weekday. Please enter again:')
        weekday = weekday.casefold()
        

    print('-'*40)
    return city, month, weekday


def load_data(city, month, weekday):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = months.index(month)

    if month != 0:
        df = df[df['month'] == month]

    if weekday != 'all':
        df = df[df['day_of_week'] == weekday.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    popular_month_name = df['Start Time'].dt.strftime('%B').mode()[0]
    print('Most Popular Month:', popular_month_name)

    # display the most common day of week

    popular_weekday = df['Start Time'].dt.strftime('%A').mode()[0]
    print('Most Popular Day:', popular_weekday)

    # display the most common start hour
    popular_hour = df['Start Time'].dt.hour.mode()[0]
    print('Most Popular Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    frequent_combination = df.groupby(['Start Station', 'End Station']).size().nlargest(1)

    print('Most Popular Start Station:', start_station)
    print('Most Popular End Station:', end_station)
    print('\nMost Frequent Combination of Start and End Station Trips:\n\n', frequent_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # calculate total travel time
    # calculate mean travel time
    total_duration = df['Trip Duration'].sum()
    mean_duration = df['Trip Duration'].mean()
   
   
    # display total travel time
    # display mean travel time
    print('Total Trip Duration:', total_duration)
    print('Mean Trip Duration:', mean_duration)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types,'\n')

    # Display counts of gender
    if 'Gender' in df.columns:    
        gender = df['Gender'].value_counts()
        print(gender,'\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Earliest year of birth:', int(df['Birth Year'].min()))
        print('Most recent year of birth:', int(df['Birth Year'].max()))
        print('Most common year of birth:', int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, weekday = get_filters()
        df = load_data(city, month, weekday)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        answer = ['yes', 'no']
        user_input = input('Do you want to see the raw data? Please answer Yes or No.\n')

        while user_input.lower() not in answer:
            user_input = input('Please answer Yes or No:\n')
            user_input = user_input.lower()

        if user_input.lower() == 'yes':
            n = 0
            while True:
                print(df.iloc[n : n + 5])
                n += 5
                user_input = input('\nDo you want to see more raw data? Please answer Yes or No.\n')
                while user_input.lower() not in answer:
                    user_input = input('Please answer Yes or No:\n')
                    user_input = user_input.lower()
                if user_input.lower() != 'yes':
                    break
        else:
            break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()

# In case you encounter an error please contact the developer at tim@bikeshare.us
