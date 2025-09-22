import questionary
from rich.console import Console
from rich.text import Text
import os
import sys
import importlib

console = Console()

welcome_text = Text("Welcome to MermaidJS Chart Generator", style="bold magenta")
console.print(welcome_text)

chart_map = {
    "1. Flowchart": {"module": "charts.flowchart", "class": "Flowchart"},
}

while True:
    file_name = questionary.text("Enter the file name for your chart:").ask()

    if not os.path.exists(file_name):
        error_text = Text("File doesn't exist!", style="bold red")
        console.print(error_text)
        continue

    # choice = questionary.select(
    #     "Select a chart type:",
    #     choices=[
    #         "1. Flowchart",
    #         "2. Piechart",
    #         "3. Barchart",
    #         "4. State Diagram",
    #         "5. Exit"
    #     ]
    # ).ask()

    choice = "1. Flowchart"

    if choice == "5. Exit":
        console.print("Exiting MermaidJS Chart Generator. Goodbye!")
        sys.exit()
    elif choice in chart_map:
        chart_info = chart_map[choice]
        try:
            module = importlib.import_module(chart_info["module"])
            chart_class = getattr(module, chart_info["class"])
            chart_instance = chart_class()
            chart_instance.generate_chart(file_name)
        except Exception as e:
            console.print(f"Error loading chart: {e}", style="bold red")
            sys.exit(1)
    else:
        console.print("Invalid choice, please try again.", style="bold yellow")
