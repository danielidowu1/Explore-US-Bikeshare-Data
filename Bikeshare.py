import time
import pandas as pd
from datetime import datetime as dt

# Mapping city names to their respective CSV data files
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york': 'new_york_city.csv',
    'washington': 'washington.csv'
}

# Lists of months and days for filtering purposes
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def filter_city():
    """Prompts user to select a city and returns the corresponding data file."""
    print("Hello! Let's explore some US bikeshare data!")
    while True:
        city = input('Would you like to see data for Chicago, New York or Washington? ').lower()
        if city in CITY_DATA:
            # Reading the CSV file for the selected city
            file = pd.read_csv(CITY_DATA[city])
            return city, file
        else:
            print("Invalid city name. Please try again.")


def filter_month_day(file):
    """Prompts user to select month and day filters for the dataset."""
    # Converting 'Start Time' to datetime format
    file['Start Time'] = pd.to_datetime(file['Start Time'])
    # Extracting month and day names from 'Start Time'
    file['month'] = file['Start Time'].dt.month_name().str.lower()
    file['day'] = file['Start Time'].dt.day_name().str.lower()

    month = input('Which month? January to June or "all": ').lower()
    if month != 'all' and month in MONTHS:
        file = file[file['month'] == month]  # Filtering data by month

    day = input('Which day? (e.g., Monday) or "all": ').lower()
    if day != 'all' and day in DAYS:
        file = file[file['day'] == day]  # Filtering data by day

    return file, month, day  # Returning filtered file and selected month/day


def time_stats(df):
    """Calculates and displays time-related statistics from the dataset."""
    if df.empty:
        print("No data for selected filters.")
        return

    print('\nCalculating The Most Frequent Times of Travel...\n')
    print('Most Common Month:', df['month'].mode()[0])  # Most common month
    print('Most Common Day of Week:', df['day'].mode()[0])  # Most common day
    print('Most Common Start Hour:', df['Start Time'].dt.hour.mode()[0])  # Most common hour


def trip_stats(df):
    """Calculates and displays statistics related to trips from the dataset."""
    if df.empty:
        return

    print('\nCalculating Trip Stats...\n')
    print('Most Common Start Station:', df['Start Station'].mode()[0])  # Most common start station
    print('Most Common End Station:', df['End Station'].mode()[0])  # Most common end station

    # Creating a new column for trip combinations and calculating the most frequent combination
    df['Trip Combo'] = df['Start Station'] + " to " + df['End Station']
    print('Most Frequent Combination:', df['Trip Combo'].mode()[0])


def trip_duration(df):
    """Calculates and displays statistics on trip duration."""
    if df.empty:
        return

    print('\nTrip Duration Stats...\n')
    print('Total Travel Time:', df['Trip Duration'].sum())  # Total travel time
    print('Average Travel Time:', df['Trip Duration'].mean())  # Average travel time


def user_type_stats(df, city):
    """Displays statistics about user types and demographics."""
    if df.empty:
        return

    print('\nUser Stats...\n')
    print(df['User Type'].value_counts())  # Counting user types

    if city != 'washington':
        # Uncomment if 'Gender' column is present and desired
        print('\nGender Breakdown:\n', df['Gender'].value_counts())  # Gender breakdown
        # Uncomment if 'Birth Year' column is present and desired
        print('\nEarliest Year:', int(df['Birth Year'].min()))  # Earliest birth year
        print('Most Recent Year:', int(df['Birth Year'].max()))  # Most recent birth year
        print('Most Common Year:', int(df['Birth Year'].mode()[0]))  # Most common birth year
    else:
        print("No gender and birth year data for Washington")


def main():
    """Main function to run the bikeshare data analysis program."""
    while True:
        city, file = filter_city()  # Filtering for the city and loading data
        df, month, day = filter_month_day(file)  # Applying month/day filters

        # Calling functions to display various statistics
        time_stats(df)
        trip_stats(df)
        trip_duration(df)
        user_type_stats(df, city)

        # Prompt to restart the data analysis process
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break  # Exit the loop if the user doesn't want to restart


if __name__ == "__main__":
    main()  # Start the program

