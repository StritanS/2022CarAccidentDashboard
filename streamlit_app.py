import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Load your data

caracteristiques = pd.read_csv('carcteristiques-2022.csv', sep=";")
lieux = pd.read_csv('lieux-2022.csv', sep=";")


# %%
lieux.rename(columns={'Num_Acc': 'Accident_Id'}, inplace=True)
print("Lieux columns:", lieux.columns)

# %%
lieux_caracteristiques_data = pd.merge(
    caracteristiques, lieux, on='Accident_Id', how='inner')

# %%


# %%
usagers = pd.read_csv("usagers-2022.csv", sep=";")
vehicules = pd.read_csv("vehicules-2022.csv", sep=';')

# %%
lieux_caracteristiques_data.rename(
    columns={'Accident_Id': 'Num_Acc'}, inplace=True)

# %%
usagers = pd.read_csv("usagers-2022.csv", sep=";")

# %%
# Merge the two DataFrames on 'Num_Acc'
merged_data = pd.merge(lieux_caracteristiques_data,
                       usagers, on='Num_Acc', how='inner')

# Group by 'Num_Acc' and count the number of rows for each group (i.e., the number of persons per accident)
persons_per_accident = merged_data.groupby(
    'Num_Acc').size().reset_index(name='nb_of_persons')

# Merge the count back to the original 'lieux_caracteristiques_data' DataFrame
lieux_caracteristiques_data = pd.merge(
    lieux_caracteristiques_data, persons_per_accident, on='Num_Acc', how='left')

# Display the resulting DataFrame


# %%
lieux_caracteristiques_data.describe()

# %%
vehicules = pd.read_csv("vehicules-2022.csv", sep=";")

# %%
# Merge the two DataFrames on 'Num_Acc'
merged_data = pd.merge(lieux_caracteristiques_data,
                       vehicules, on='Num_Acc', how='inner')

# Group by 'Num_Acc' and count the number of rows for each group (i.e., the number of vehicles per accident)
vehicles_per_accident = merged_data.groupby(
    'Num_Acc').size().reset_index(name='nb_of_vehicles')

# Merge the count back to the original 'lieux_caracteristiques_data' DataFrame
lieux_caracteristiques_data = pd.merge(
    lieux_caracteristiques_data, vehicles_per_accident, on='Num_Acc', how='left')

# Display the resulting DataFrame


# %%

# %%
lieux_caracteristiques_data['long'] = pd.to_numeric(
    lieux_caracteristiques_data['long'].str.replace(',', '.'), errors='coerce')

# %%

lieux_caracteristiques_data['long'] = lieux_caracteristiques_data['long'].astype(
    float)

# %%
lieux_caracteristiques_data['lat'] = pd.to_numeric(
    lieux_caracteristiques_data['lat'].str.replace(',', '.'), errors='coerce')

# %%
lieux_caracteristiques_data['lat'] = lieux_caracteristiques_data['lat'].astype(
    float)

# Assuming you have a DataFrame named 'merged_data'

# Page configuration
st.set_page_config(layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to", ["🏡Home🏡", "🗺️Map🗺️", "☀️Lighting Condition☀️", "🛤️Surface Condition🛤️", "🚦User involved in accident Info🚦", "🚗Info about categorie Vehicule🚗"])

# Define the data visualization functions


def show_home_page():
    st.title("FRANCE'S 2022 CAR ACCIDENT Dashboard")
    st.write(
        "Welcome to the 2022 France's Road Accidents Dashboard. 🚗 Use the sidebar to navigate to different sections. 🛣️ In 'Map, ' you will find a visual representation of accidents across France. 🗺️ 'Lighting Condition' provides insights into accidents under different lighting conditions. ☀️ 'Surface Condition' covers the road conditions during accidents. 🛤️ Explore 'User involved in accident Info' to see details about individuals involved in accidents. 🚦 And finally, 'Info about categorie Vehicule' offers information about different vehicle categories. 🚗")
    st.image("road_safety_image.jpg")

    st.write("Here you can see the 4 datasets that i used and also a link to understand the labels : https://static.data.gouv.fr/resources/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2021/20231005-094302/description-des-bases-de-donnees-annuelles-2022.pdf")
    # Display dataset information
    st.header('Caracteristiques Dataset')
    st.write(caracteristiques)

    st.header('Lieux Dataset')
    st.write(lieux)

    st.header('Usagers Dataset')
    st.write(usagers)

    st.header('Vehicules Dataset')
    st.write(vehicules)


def show_map_page():
    st.title("🗺️Map of Accidents🗺️")
    # Set the center of France
    center_lat = 46.6031
    center_long = 1.8883
    zoom_level = 5
    custom_color_scale = ["blue", "yellow", "purple", "orange", "red"]

    # Create a multi-select box for hover data attributes
    selected_hover_data = st.multiselect(
        "Select Hover Data Attributes",
        ['Num_Acc', 'mois', 'an', 'hrmn', 'lum', 'com', 'agg',
         'col', 'lat', 'long', 'catr',
         'circ', 'nbv', 'surf', 'infra', 'situ', 'vma', 'nb_of_persons', 'nb_of_vehicles'],
    )

    # Create a slider for selecting "mois"
    selected_month = st.slider("Select Month", 1, 12, (1, 12))

    # Filter the data by selected month
    filtered_data = lieux_caracteristiques_data[(lieux_caracteristiques_data['mois'] >= selected_month[0]) & (
        lieux_caracteristiques_data['mois'] <= selected_month[1])]

    # Create the map with filtered data
    fig = px.scatter_mapbox(
        filtered_data,
        lat='lat',
        lon='long',
        color='nb_of_persons',
        color_continuous_scale=custom_color_scale,
        size='nb_of_vehicles',
        hover_data=selected_hover_data,
        zoom=zoom_level,
        center={'lat': center_lat, 'lon': center_long}
    )

    fig.update_layout(mapbox_style="carto-positron")
    fig.update_geos(fitbounds="locations", visible=False, showcoastlines=False)
    st.plotly_chart(fig)
    st.write(
        "Here you can see the map of every accident that happened in 2022, you can par default see the number of vehicles and persons involved. You can also choose to add other attributes that you can see when you hover a point !")


def show_lighting_condition_page():

    st.title("☀️Lighting Condition Analysis☀️")
    lum_mapping = {
        1: 'Plein jour',
        2: 'Crépuscule ou aube',
        3: 'Nuit sans éclairage public',
        4: 'Nuit avec éclairage public non allumé',
        5: 'Nuit avec éclairage public allumé'
    }


# Apply the mapping to create a new column 'lum_category'
    lieux_caracteristiques_data['lum_category'] = lieux_caracteristiques_data['lum'].map(
        lum_mapping)

    # Group by 'lum_category' and count the number of accidents
    accident_count = lieux_caracteristiques_data['lum_category'].value_counts(
    ).reset_index()
    accident_count.columns = ['lum_category', 'accident_count']

    # Create a bar chart using Plotly Express
    fig = px.bar(
        accident_count,
        x='lum_category',
        y='accident_count',
        color='lum_category',
        title='Number of Accidents for Each Lighting Condition',
        labels={'accident_count': 'Number of Accidents',
                'lum_category': 'Lighting Conditions'},
    )

    # Show the plot
    st.plotly_chart(fig)

    # Apply the mapping to create a new column 'lum_category'
    lieux_caracteristiques_data['lum_category'] = lieux_caracteristiques_data['lum'].map(
        lum_mapping)

    # Create subplots
    figs, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))

    # Flatten the axes array for easy indexing
    axes = axes.flatten()

    # Iterate through each 'lum' level and create a histogram in each subplot
    for i, (level, category) in enumerate(lum_mapping.items()):
        # Filter data for the specific level
        level_data = lieux_caracteristiques_data[lieux_caracteristiques_data['lum'] == level]

        # Plotting a histogram for the current level
        axes[i].hist(level_data['nb_of_vehicles'], bins=20,
                     color='skyblue', edgecolor='black')

        axes[i].set_title(
            f'Distribution of Vehicles per Accident - {category}')
        axes[i].set_xlabel('Number of Vehicles')
        axes[i].set_ylabel('Frequency')

    # Adjust layout
    st.write("Distribution of Vehicles per Accident depending on Light conditions")
    st.pyplot(figs)


def show_surface_condition_page():
    import math
    st.title("🛤️Surface Condition Analysis🛤️")

    # Mapping for 'surf' categories
    surf_mapping = {
        -1: 'Non renseigné',
        1: 'Normale',
        2: 'Mouillée',
        3: 'Flaques',
        4: 'Inondée',
        5: 'Enneigée',
        6: 'Boue',
        7: 'Verglacée',
        8: 'Corps gras – huile',
        9: 'Autre'
    }

    # Apply the mapping to create a new column 'surf_category'
    lieux_caracteristiques_data['surf_category'] = lieux_caracteristiques_data['surf'].map(
        surf_mapping)

    # Group by 'surf_category' and count the number of accidents
    surf_accident_count = lieux_caracteristiques_data['surf_category'].value_counts(
    ).reset_index()
    surf_accident_count.columns = ['surf_category', 'accident_count']

    # Create a bar chart using Plotly Express
    fig = px.bar(
        surf_accident_count,
        x='surf_category',
        y='accident_count',
        color='surf_category',
        title='Number of Accidents for Each Surface Condition',
        labels={'accident_count': 'Number of Accidents',
                'surf_category': 'Surface Condition'},
    )

    # Show the plot

    st.plotly_chart(fig)
    # Your visualization code for surface condition goes here
    # Create subplots
    num_subplots = len(surf_mapping)
    num_cols = 2
    num_rows = math.ceil(num_subplots / num_cols)

    # Create figure and axis objects
    figs, axes = plt.subplots(num_rows, num_cols, figsize=(15, 10))

    # Flatten the axes array for easy indexing
    axes = axes.flatten()

    # Iterate through each 'surf' level and create a histogram in each subplot
    for i, (level, category) in enumerate(surf_mapping.items()):
        # Filter data for the specific level
        level_data = lieux_caracteristiques_data[lieux_caracteristiques_data['surf'] == level]

        # Plotting a histogram for the current level
        axes[i].hist(level_data['nb_of_vehicles'], bins=20,
                     color='skyblue', edgecolor='black')

        axes[i].set_title(f'Distribution of Vehicles - {category}')
        axes[i].set_xlabel('Number of Vehicles')
        axes[i].set_ylabel('Frequency')

    st.pyplot(figs)


def show_user_accident_info():

    st.title("🚦Info  about Perons involved in accidents🚦")
    # Mapping numeric values to labels for better readability
    catu_labels = {
        1: 'Driver',
        2: 'Passenger',
        3: 'Pedestrian'
    }

    # Create a new column with mapped labels
    usagers['catu_label'] = usagers['catu'].map(catu_labels)

    fig = plt.figure(figsize=(8, 6))
    sns.countplot(x='catu_label', data=usagers)
    plt.title('Distribution of User Categories')
    plt.xlabel('User Category')
    plt.ylabel('Count')
    st.pyplot(fig)

    # Mapping numeric values to labels for better readability
    sexe_labels = {
        1: 'Male',
        2: 'Female'
    }

    # Create a new column with mapped labels
    usagers['sexe_label'] = usagers['sexe'].map(sexe_labels)

    fig_gender = plt.figure(figsize=(8, 6))
    sns.countplot(x='sexe_label', data=usagers)
    plt.title('Distribution of Gender')
    plt.xlabel('Gender')
    plt.ylabel('Count')
    st.pyplot(fig_gender)

    # Mapping numeric values to labels for better readability
    trajet_labels = {
        -1: 'Non renseigné',
        0: 'Non renseigné',
        1: 'Domicile – travail',
        2: 'Domicile – école',
        3: 'Courses – achats',
        4: 'Utilisation professionnelle',
        5: 'Promenade – loisirs',
        9: 'Autre'
    }

    # Create a new column with mapped labels
    usagers['trajet_label'] = usagers['trajet'].map(trajet_labels)

    # Count the occurrences of each label
    trajet_counts = usagers['trajet_label'].value_counts()

    # Create a bar plot
    fig_trajet = plt.figure(figsize=(10, 6))
    trajet_counts.plot(kind='bar', color='skyblue')
    plt.title('Distribution of Trajet')
    plt.xlabel('Trajet')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig_trajet)
    # Mapping numeric values to labels for better readability
    grav_labels = {
        1: 'Indemne',
        2: 'Tué',
        3: 'Blessé hospitalisé',
        4: 'Blessé léger'
    }

    # Create a new column with mapped labels
    usagers['grav_label'] = usagers['grav'].map(grav_labels)

    # Count the occurrences of each label
    grav_counts = usagers['grav_label'].value_counts()

    # Create a bar plot
    fig_grav = plt.figure(figsize=(10, 6))
    grav_counts.plot(kind='bar', color='skyblue')
    plt.title('Distribution of Gravité de blessure (grav) in Usagers')
    plt.xlabel('Gravité de blessure')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    st.pyplot(fig_grav)

    st.image("injuries_depending_on_vma.jpg")


def show_cat_vehicules():
    st.title("🚗Info  about category of vehicule involved in accidents🚗")
    import matplotlib.cm as cm
    # Mapping numeric values to labels for better readability
    catv_labels = {
        0: 'Indéterminable',
        1: 'Bicyclette',
        2: 'Cyclomoteur <50cm3',
        3: 'Voiturette',
        4: 'Scooter immatriculé',
        5: 'Motocyclette',
        6: 'Side-car',
        7: 'VL seul',
        8: 'VL + caravane',
        9: 'VL + remorque',
        10: 'VU seul 1,5T <= PTAC <= 3,5T',
        11: 'VU (10) + caravane',
        12: 'VU (10) + remorque',
        13: 'PL seul 3,5T <PTCA <= 7,5T',
        14: 'PL seul > 7,5T',
        15: 'PL > 3,5T + remorque',
        16: 'Tracteur routier seul',
        17: 'Tracteur routier + semi-remorque',
        18: 'Transport en commun',
        19: 'Tramway',
        20: 'Engin spécial',
        21: 'Tracteur agricole',
        30: 'Scooter < 50 cm3',
        31: 'Motocyclette > 50 cm3 et <= 125 cm3',
        32: 'Scooter > 50 cm3 et <= 125 cm3',
        33: 'Motocyclette > 125 cm3',
        34: 'Scooter > 125 cm3',
        35: 'Quad léger <= 50 cm3',
        36: 'Quad lourd > 50 cm3',
        37: 'Autobus',
        38: 'Autocar',
        39: 'Train',
        40: 'Tramway',
        41: '3RM <= 50 cm3',
        42: '3RM > 50 cm3 <= 125 cm3',
        43: '3RM > 125 cm3',
        50: 'EDP à moteur',
        60: 'EDP sans moteur',
        80: 'VAE',
        99: 'Autre véhicule'
    }

    # Apply the mapping to create a new column 'catv_label'
    vehicules['catv_label'] = vehicules['catv'].map(catv_labels)

    # Create a Streamlit app
    st.title('Distribution of Catégorie du véhicule (catv)')

    # Allow the user to select categories to display
    selected_categories = st.multiselect('Select Categories to Display', list(
        catv_labels.values()), list(catv_labels.values())[:5])

    # Filter the data based on user selection
    filtered_data = vehicules[vehicules['catv_label'].isin(
        selected_categories)]

    # Count the occurrences of each label in the filtered data
    catv_counts = filtered_data['catv_label'].value_counts()

    colors = cm.viridis(catv_counts / max(catv_counts))

    # Create a bar chart
    fig = plt.figure(figsize=(14, 8))
    plt.bar(catv_counts.index, catv_counts.values, color=colors)
    plt.title('Distribution of Catégorie du véhicule (catv)')
    plt.xlabel('Catégorie du véhicule')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')

    # Display the bar chart
    st.pyplot(fig)

    st.title('Vehicle Category Fatality Analysis')
    import plotly.express as px
    import plotly.graph_objects as go

    # Assuming 'usagers' and 'vehicules' are your DataFrames
    # Replace 'Your_Column_Name' with the actual name of your DataFrame columns

    # Merge the two DataFrames on 'id_vehicule'
    merged_df = pd.merge(usagers, vehicules, on='id_vehicule')

    merged_df['catv'] = merged_df['catv'].map(catv_labels)

    # Calculate the total count for each catv
    total_count_by_catv = merged_df.groupby(
        'catv').size().reset_index(name='total_count')

    # Calculate the count of grav == 2 for each catv
    fatality_count_by_catv = merged_df[merged_df['grav'] == 2].groupby(
        'catv').size().reset_index(name='fatality_count')

    # Merge the two counts DataFrames
    merged_count_df = pd.merge(
        total_count_by_catv, fatality_count_by_catv, on='catv', how='left').fillna(0)

    # Calculate the percentage
    merged_count_df['fatality_percentage'] = (
        merged_count_df['fatality_count'] / merged_count_df['total_count']) * 100

    # Create a bar chart using Plotly
    fig = px.bar(
        merged_count_df,
        x='catv',
        y='fatality_percentage',
        text='fatality_percentage',
        color='fatality_percentage',
        labels={
            'catv': 'Vehicle Category (catv)', 'fatality_percentage': 'Percentage of Fatalities (grav = 2)'},
        title='Percentage of Fatalities by Vehicle Category',
        width=1200,

    )

    fig.update_xaxes(tickangle=45, tickmode='array',
                     tickvals=merged_count_df['catv'])
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')

    st.plotly_chart(fig)


# Main content based on selected page
if page == "🏡Home🏡":
    show_home_page()
elif page == "🗺️Map🗺️":
    show_map_page()
elif page == "☀️Lighting Condition☀️":
    show_lighting_condition_page()
elif page == "🛤️Surface Condition🛤️":
    show_surface_condition_page()

elif page == "🚦User involved in accident Info🚦":
    show_user_accident_info()
elif page == "🚗Info about categorie Vehicule🚗":
    show_cat_vehicules()

# %%
