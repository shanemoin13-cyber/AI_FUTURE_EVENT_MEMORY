import json
import os
import networkx as nx
import matplotlib.pyplot as plt


MEMORY_FILE = "future_memory.json"


# ==========================================
# LOAD FUTURE MEMORY
# ==========================================

if not os.path.exists(MEMORY_FILE):

    print("future_memory.json not found.")
    print("Run future_event.py first.")

    exit()


with open(MEMORY_FILE, "r") as file:
    memory = json.load(file)


if not memory:

    print("Future memory is empty.")

    exit()


# ==========================================
# CREATE GRAPH
# ==========================================

graph = nx.DiGraph()


# ==========================================
# ADD EVENTS FROM MEMORY
# ==========================================

for event in memory:

    event_name = event["event_name"]
    probability = event["probability"]

    graph.add_node(event_name)

    # Create a possible next event
    next_event = "Possible Failure"

    graph.add_node(next_event)

    graph.add_edge(
        event_name,
        next_event,
        probability=probability / 100
    )


# ==========================================
# POSITION GRAPH
# ==========================================

position = nx.spring_layout(
    graph,
    seed=42
)


# ==========================================
# DRAW GRAPH
# ==========================================

nx.draw(
    graph,
    position,
    with_labels=True,
    node_size=3000,
    arrows=True
)


# ==========================================
# SHOW PROBABILITIES
# ==========================================

edge_labels = nx.get_edge_attributes(
    graph,
    "probability"
)


# Convert probability to percentage

percentage_labels = {}

for edge, value in edge_labels.items():

    percentage_labels[edge] = (
        f"{value * 100:.1f}%"
    )


nx.draw_networkx_edge_labels(
    graph,
    position,
    edge_labels=percentage_labels
)


# ==========================================
# TITLE
# ==========================================

plt.title(
    "AI Future Event Memory Graph"
)


# ==========================================
# DISPLAY
# ==========================================

plt.show()