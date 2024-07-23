import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("final_updated_maharashtra_agriculture_data.csv")

# Function to provide feedback
def provide_feedback(city, soil_type, fertilizer_cost, total_cultivating_cost, outcome):
    subset = df[(df["City"] == city) & (df["Soil Type"] == soil_type)]

    if subset.empty:
        return "No data available for the selected city and soil type.", None, None, None

    best_crop_row = subset.loc[subset["Income per Acre"].idxmax()]
    best_crop = best_crop_row["Best Crop"]
    best_crop_income = best_crop_row["Income per Acre"]

    if outcome < best_crop_income:
        feedback = f"Consider switching to {best_crop}, which can earn you {best_crop_income} per acre."
    else:
        feedback = "You are in the right direction!"

    return feedback, best_crop, best_crop_income

# Function to visualize crop prices
def visualize_crop_prices():
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x="Best Crop", y="Income per Acre", data=df, ax=ax)
    ax.set_title("Income per Acre for Different Crops")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)

# Function to plot bar chart for analysis
def plot_bar_chart(city, fertilizer_cost, total_cultivating_cost, outcome, best_crop_income):
    parameters = ["Fertilizer Cost", "Total Cultivating Cost", "Total Outcome per Acre", "Best Crop Income per Acre"]
    values = [fertilizer_cost, total_cultivating_cost, outcome, best_crop_income]

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=parameters, y=values, palette="viridis", ax=ax)
    ax.set_title(f"Analysis for {city} - {df.iloc[0]['Soil Type']} Soil")
    ax.set_ylabel("Value")
    ax.set_ylim(10000, 80000)  # Set y-axis limit from 10000 to 80000

    for i, v in enumerate(values):
        ax.text(i, v + 1000, str(v), ha='center', va='bottom', fontsize=10, color='black')  # Display value on top of each bar

    st.pyplot(fig)

# Main function
def main():
    st.title("Agricultural Finance Advisor")

    # Sidebar inputs
    st.sidebar.title("Input Parameters")
    city = st.sidebar.text_input("Enter your city")
    soil_type = st.sidebar.selectbox("Select your soil type", df["Soil Type"].unique())
    fertilizer_cost = st.sidebar.number_input("Enter your fertilizer cost", min_value=0.0)
    total_cultivating_cost = st.sidebar.number_input("Enter your total cultivating cost", min_value=0.0)
    outcome = st.sidebar.number_input("Enter your outcome", min_value=0.0)

    if st.sidebar.button("Get Advice"):
        feedback, best_crop, best_crop_income = provide_feedback(city, soil_type, fertilizer_cost, total_cultivating_cost, outcome)
        st.subheader("Feedback")
        st.write(feedback)

        if feedback != "No data available for the selected city and soil type.":
            st.subheader("Crop Prices Visualization")
            visualize_crop_prices()

            if best_crop_income:
                st.subheader("Best Crop Income per Acre")
                st.write(f"Income per acre for best crop: {best_crop_income}")

            st.subheader("Analysis: Bar Chart")
            plot_bar_chart(city, fertilizer_cost, total_cultivating_cost, outcome, best_crop_income)

if __name__ == "__main__":
    main()
