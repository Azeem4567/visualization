import pandas as pd
import matplotlib.pyplot as plt
import os  # To create directories and handle paths
import re  # Regular expressions module

# Load your CSV data into DataFrame
df = pd.read_csv('data.csv')

# Melt the DataFrame to make it long-form
df_melted = df.melt(id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
                    var_name="Year", value_name="Value")

# Convert 'Year' to numeric
df_melted['Year'] = pd.to_numeric(df_melted['Year'], errors='coerce')

# Drop rows with NaN values in 'Year' or 'Value' columns
df_melted.dropna(subset=['Year', 'Value'], inplace=True)

# Choose the indicator you want to plot
indicator_to_plot = "Mortality rate, under-5 (per 1,000 live births)"
escaped_indicator = re.escape(indicator_to_plot)

# Create a directory for plots if it doesn't exist
plots_directory = "plots"
if not os.path.exists(plots_directory):
    os.makedirs(plots_directory)

df_filtered = df_melted[df_melted['Indicator Name'].str.contains(escaped_indicator, case=False)]

# Get a list of unique countries
countries = df_filtered['Country Name'].unique()

# Loop through each country and create plots
for country in countries:
    print(f"Creating plots for {country}")
    df_country = df_filtered[df_filtered['Country Name'] == country]
    
    # Create line plot
    plt.figure(figsize=(10, 5))
    plt.plot(df_country['Year'], df_country['Value'], marker='o')
    plt.title(f'{indicator_to_plot} over time for {country}')
    plt.xlabel('Year')
    plt.ylabel('Value')
    plt.grid(True)
    plt.savefig(f'{plots_directory}/line_plot_{country.replace(" ", "_")}.png')
    plt.show()  # Show the plot inline
    
    # Create bar chart
    plt.figure(figsize=(10, 5))
    plt.bar(df_country['Year'], df_country['Value'])
    plt.title(f'{indicator_to_plot} distribution for {country}')
    plt.xlabel('Year')
    plt.ylabel('Value')
    plt.grid(axis='y')
    plt.savefig(f'{plots_directory}/bar_chart_{country.replace(" ", "_")}.png')
    plt.show()  # Show the plot inline
    
    # Create box plot
    plt.figure(figsize=(10, 5))
    plt.boxplot([df_country[df_country['Year'] == year]['Value'].tolist() for year in sorted(df_country['Year'].unique())])
    plt.title(f'{indicator_to_plot} distribution for {country}')
    plt.xlabel('Year')
    plt.xticks(range(1, len(df_country['Year'].unique()) + 1), sorted(df_country['Year'].unique()), rotation=45)
    plt.ylabel('Value')
    plt.grid(axis='y')
    plt.savefig(f'{plots_directory}/box_plot_{country.replace(" ", "_")}.png')
    plt.show()  # Show the plot inline

print("Plots created for each country.")
