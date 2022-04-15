# Projet SMA - Argumentation-based Negotiation for choosing a car engine 

## Practical informations

*Deadline :* 15 avril 2022 - 23h59

*Lien vers rapport (5 pages) :* https://www.overleaf.com/4174382465zcrtkprxdbsq

## Summary

The practical sessions in this Multi-Agent System Course will be devoted to the programming of a negotiation & argumentation simulation. Agents representing human engineering will need to negotiate with each other to make a joint decision regarding choosing the best engine. The negotiation comes when the agents have different preferences on the criteria, and the argumentation will help them decide which item to select. Moreover, the arguments supporting the best choice will help build the justification supporting it, an essential element for the company to develop its marketing campaign.

The model is tests and demonstrates several Mesa concepts and features:
 - MultiGrid
 - Multiple agent types (wolves, sheep, grass)
 - Overlay arbitrary text (wolf's energy) on agent's shapes while drawing on CanvasGrid
 - Agents inheriting a behavior (random movement) from an abstract parent
 - Writing a model composed of multiple files.
 - Dynamically adding and removing agents from the schedule

## The story

Imagine that a car manufacturer wants to launch a new car on the market. For this, a crucial choice is the one of the engines that should meet some technical requirements but at the same time be attractive for the customers (economic, robust, ecological, etc.). Several types of engines exist and thus provide a large other of cars models: essence or diesel Internal Combustion Engine (ICE), Compressed Natural GAS (CNG), Electric Battery (EB), Fuel Cell (FC), etc. The company decides to take into account different criteria to evaluate them: Consumption, environmental impact (CO2, clean fuel, NOX 1 ...), cost, durability, weight, targeted maximum speed, etc. To establish the best other/choice among a large set of options, they decide to simulate a negotiation process where agents, with different opinions and preferences (even different knowledge and expertise), discuss the issue to end up with the best other. The simulation will allow the company to simulate several typologies of agent behaviours (expertise, role, preferences, . . . ) at a lower cost within a reasonable time.

## Dependencies

To install the dependencies use pip and the requirements.txt in this directory. e.g.

```
    $ pip install -r requirements.txt
```


### Files architecture

    .
    ├── .gitignore                     # avoid unecessary data exchange between git and local files
    ├── communication                  # folder containing files related to the comunication
    │   └── files
    │   └── files
    ├── venv                           # folder containing file related to the argumentation       
    │   └── pw_argumentation.py        # file containing the code related to the argumentation       
    ├── README.me                      # presents the GIT repository
    └── mesa.code-workspace            # workspace
