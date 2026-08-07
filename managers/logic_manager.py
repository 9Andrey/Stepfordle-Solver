import pandas as pd
import networkx as nx
from collections import defaultdict
from itertools import chain
from pathlib import Path


def declarePaths() -> None:
    """Makes variables for the different paths where data can
    and is stored."""
    
    # Project directory
    global BASE_DIR
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Data folder (CSVs)
    global DATA_DIR
    DATA_DIR = BASE_DIR / "data"


def setupTree() -> None:
    """Creates the track diagram according to the CSV files
    stations.csv, connections.csv, and zonesConnections.csv"""

    # Read CSVs
    nodes_df = pd.read_csv(DATA_DIR / "stations.csv", skipinitialspace=True)
    edges_df = pd.read_csv(DATA_DIR / "connections.csv", skipinitialspace=True)
    zones_df = pd.read_csv(DATA_DIR / "zonesConnections.csv", skipinitialspace=True)

    # Create track graph (with all stations)
    Stops = nx.Graph()

    # Add stations with their names
    for _, row in nodes_df.iterrows():
        Stops.add_node(row["id"], name=row["station_name"])

    # Add station edges (connections)
    for _, row in edges_df.iterrows():
        Stops.add_edge(row["node_1"], row["node_2"])

    # Gather all distances to lookup
    global stop_dist
    stop_dist = dict(nx.all_pairs_shortest_path_length(Stops))

    # Create zone graph
    Zones = nx.Graph()

    # Add zones 1-10
    for z in range(1, 11):
        Zones.add_node(z)

    # Add zone edges
    for _, row in zones_df.iterrows():
        Zones.add_edge(row["zone_1"], row["zone_2"])

    # Create lookup for zone distances
    global zone_dist
    zone_dist = dict(nx.all_pairs_shortest_path_length(Zones))


def createLookupDictionaries() -> None:
    """Creates useful dictionaries for efficient lookups,
    instead of looking in the CSVs"""

    # Get a dictionary with station data
    global stations
    stations = (
        pd.read_csv(DATA_DIR / "stations.csv", skipinitialspace=True)
        .set_index("id")
        .to_dict(orient="index")
    )

    # Creates a dictionary with the ids of stations in each zone
    global stations_in_zone
    stations_in_zone = defaultdict(list)

    for station_id, station in stations.items():
        stations_in_zone[station["zone"]].append(station_id)

    stations_in_zone = {
        zone: tuple(ids)
        for zone, ids in stations_in_zone.items()
    }


def initialise() -> None:
    declarePaths()
    setupTree()
    createLookupDictionaries()


def getPossibleZones(*zones_info: tuple) -> list:
    """Given one or more tuples (zone_num, dist) returns
    the eligible zones that are tuple[1] distance from tuple[0]."""

    counts = defaultdict(int)
    eligible_zones = []

    for zone, dist in zones_info:
        for target in range(1, 11):
            if zone_dist[zone][target] == dist:
                eligible_zones.append(target)
                counts[target] += 1

    if len(zones_info) == 1:
        return eligible_zones

    possible_zones = []

    for zone in range(1, 11):
        if counts[zone] == len(zones_info):
            possible_zones.append(zone)

    return possible_zones


def getAllStationsInZones(zones: tuple) -> tuple:
    """Given a list of zones, it outputs every station
    inside those zones."""

    station_ids = tuple(
        chain.from_iterable(stations_in_zone[z] for z in zones)
    )

    return station_ids


def getPossibleStationsFrom(possibilities: tuple, *stop_info: tuple) -> list:
    """From the possibilities, get the possible station
    given the station id tuple[0] is tuple[1] distance
    from target."""

    counts = defaultdict(int)
    eligible_stops = []

    for station_id, dist in stop_info:
        lookup = stop_dist[station_id]

        for possible_id in possibilities:
            if lookup[possible_id] == dist:
                eligible_stops.append(possible_id)
                counts[possible_id] += 1

    if len(stop_info) == 1:
        return eligible_stops

    target_stops = []

    # Preserves the original ordering of possibilities
    for possible_id in possibilities:
        if counts[possible_id] == len(stop_info):
            target_stops.append(possible_id)

    return target_stops


def givenGuessesGivePossibleTargets(*guesses: tuple) -> list:
    """Given one or more tuples (id, zone_dist, stop_dist)
    get the possible targets."""

    # Get zones where the target could be
    zones_info = []
    for guess in guesses:
        zones_info.append((stations[guess[0]]["zone"], guess[1]))

    # Slowly narrow down the target
    possible_zones = getPossibleZones(*zones_info)
    eligible_stations = getAllStationsInZones(possible_zones)

    # Extract station data from input
    stop_info = []
    for guess in guesses:
        stop_info.append((guess[0], guess[2]))

    return getPossibleStationsFrom(eligible_stations, *stop_info)


def getAllBestGuesses(*already_guessed: tuple) -> list:
    """When you input every guess you did, it looks for what
    stations narrow it down the furthest."""
    
    available_targets = givenGuessesGivePossibleTargets(*already_guessed)
    unavailable_guesses = [(lambda x: x[0])(guess) for guess in already_guessed]

    available_guesses = list(range(len(stations)))
    for unavailable in unavailable_guesses:
        if available_guesses.count(unavailable) == 1: available_guesses.remove(unavailable)

    # Calculates the average number of guesses remaining if we did that guess
    # Compares it to the best and adds it to a list if its like the best, if its the best reset the list
    best = float("inf")
    best_guesses = []
    for guess in available_guesses:
        current_sum = 0
        for target in available_targets:
            dist_station = stop_dist[target][guess]
            dist_zone = zone_dist[stations[target]["zone"]][stations[guess]["zone"]]
            current_sum += len(givenGuessesGivePossibleTargets((guess, dist_zone, dist_station), 
                                                               *already_guessed))
        average = current_sum / len(available_targets)
        if average == best: 
            best_guesses.append(guess)
        elif average < best: 
            best = average
            best_guesses = [guess, ]
                        
    return best_guesses


def reduceGuessesWithTargets(targets: tuple, candidate_guesses: tuple) -> list:
    """Priotitises tragets for the best guesses, if a possible
    target is one of the best guesses, it gets that one."""
    
    best_guesses = []
    for guess in candidate_guesses:
        if targets.count(guess) == 1: best_guesses.append(guess)
    
    if len(best_guesses) == 0: return candidate_guesses
    return best_guesses


def bestGuessGivenTargets(*already_guessed: tuple) -> list:
    """When inputing the guesses made, it narrows it down the
    furthest to get the best stations for the next guess"""

    all_best_guesses = getAllBestGuesses(*already_guessed)
    available_targets = givenGuessesGivePossibleTargets(*already_guessed)
    
    return reduceGuessesWithTargets(available_targets, all_best_guesses)


# When module is called, setup essential stuff
initialise()
