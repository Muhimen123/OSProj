import os
import sys

import questionary
from rich import print as rprint
from charts.chart import Chart

class Node:
    shape_start = {
        'Rectangle': '[',
        'Rounded Rectangle': '(',
        'Oval': '(['
    }

    shape_end = {
        'Rectangle': ']',
        'Rounded Rectangle': ')',
        'Oval': '])'
    }

    def __init__(self, name, shape):
        self.name = name
        self.shape = shape

    def node_string(self):
        output = f"{self.shape_start[self.shape]}{self.name}{self.shape_end[self.shape]}"
        return output

class Edge:
    edge_symbol = {
        "Arrow head": "-->",
        "Open link": "--",
        "Dotted link": "-.->",
        "Circle head": "--o",
    }

    def __init__(self, start, end, connection, edge_text):
        self.start = start
        self.end = end
        self.connection = connection
        self.edge_text = edge_text

    def edge_string(self):
        edge_symbol_string = ""
        edge_symbol_string += self.edge_symbol[self.connection]

        if self.edge_text != "":
            edge_symbol_string += f"|{self.edge_text}|"

        return edge_symbol_string

class Flowchart(Chart):

    nodes = list()
    edges = list()

    node_count = 0

    def __init__(self):
        super().__init__()
        self.file_path = None
        print("Flowchart class initialized.")

    def choose_option(self):
        option = questionary.select(
            "Select operation: ",
            choices=[
                "Add node",
                "Add edge",
                "Show all nodes",
                "Show all edges",
                "Confirm Write",
                "Abort",
            ]
        ).ask()

        self.option_handler(option)

    def option_handler(self, option):
        if option == "Add node":
            self.add_node()
        elif option == "Add edge":
            self.add_edge()
        elif option == "Show all nodes":
            self.show_all_nodes()
        elif option == "Show all edges":
            self.show_all_edges()
        elif option == "Confirm Write":
            self.confirm_write()
        elif option == "Abort":
            sys.exit()

    def add_node(self):
        node_name = questionary.text("Enter node name: ").ask()

        shape = questionary.select(
            "Select shape: ",
            choices=[
                "Rectangle",
                "Rounded Rectangle",
                "Oval"
            ]
        ).ask()

        node = Node(node_name, shape)
        self.nodes.append(node)

    def show_all_nodes(self):
        tmp_count = 0
        for node in self.nodes:
            tmp_count += 1
            print(f"{tmp_count}. {node.name}")


    def show_all_edges(self):
        for edge in self.edges:
            print(f"{edge.start} - {edge.end}")

    def add_edge(self):
        source_index = questionary.text("Source start index: ").ask()
        destination_index = questionary.text("Destination end index: ").ask()

        connection_type = questionary.select(
            "Choose an edge type: ",
            choices=[
                "Arrow head",
                "Open link",
                "Dotted link",
                "Circle head"
            ]
        ).ask()

        edge_text = questionary.text("Enter edge text(leave blank if none): ").ask()

        edge = Edge(source_index, destination_index, connection_type, edge_text)
        self.edges.append(edge)

    def confirm_write(self):
        with open(self.file_path, "a") as f:
            f.write("```mermaid\n")
            f.write("flowchart TD;\n")
            for edge in self.edges:
                start_id = int(edge.start)
                start = self.nodes[start_id-1].node_string()

                finish_id = int(edge.end)
                finish = self.nodes[finish_id-1].node_string()

                edge_string = edge.edge_string()
                final_string = f"{start_id}{start}{edge_string}{finish_id}{finish}"

                f.write(final_string + '\n')

            f.write("```\n\n")

        rprint("[bold green] Successfully written chart [/bold green]")
        sys.exit()

    def generate_chart(self, filename):
        pwd = os.getcwd()
        pwd += '/'
        pwd += filename

        self.file_path = filename
        rprint(f"Generating Flowchart in:[italic blue] {pwd} [/italic blue]")

        while True:
            self.choose_option()
