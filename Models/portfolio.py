import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import interact, FloatText, Dropdown, Button, VBox, HBox

# Function to analyze financial goal (simplified)
def analyze_portfolio(assets, values):
    total_value = sum(values)
    percentages = [value / total_value * 100 for value in values]
    return total_value, percentages

# Function to plot portfolio allocation
def plot_portfolio_allocation(assets, values):
    total_value, percentages = analyze_portfolio(assets, values)
    plt.figure(figsize=(8, 6))
    plt.pie(percentages, labels=assets, autopct='%1.1f%%', startangle=140)
    plt.title('Portfolio Allocation')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

# Interactive function for managing portfolio
def manage_portfolio(assets, values):
    assets_widgets = [FloatText(value=value, description=asset) for asset, value in zip(assets, values)]
    assets_values = [widget.value for widget in assets_widgets]

    update_button = Button(description="Update Portfolio")

    def update_portfolio(button):
        assets_values = [widget.value for widget in assets_widgets]
        plot_portfolio_allocation(assets, assets_values)

    update_button.on_click(update_portfolio)

    widgets = VBox([HBox(assets_widgets), update_button])
    display(widgets)

# Example assets and values
assets = ['Corn', 'Wheat', 'Soybeans', 'Livestock', 'Dairy']
values = [20000, 15000, 30000, 40000, 25000]  # Example values (in dollars)

# Initial visualization
plot_portfolio_allocation(assets, values)

# Interactive portfolio manager
manage_portfolio(assets, values)
