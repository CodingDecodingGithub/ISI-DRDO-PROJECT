from math import gcd
from functools import reduce

def calculate_key_length(positions):
    if len(positions) < 2:
        raise ValueError("At least 2 positions are required to calculate distance.")
    # ... (Keep the rest of the file the same)
        
    # Sort positions
    sorted_positions = sorted(positions)
    
    # Calculate consecutive distances
    distances = [
        sorted_positions[i + 1] - sorted_positions[i]
        for i in range(len(sorted_positions) - 1)
    ]
    
    # Check if all elements are identical (which would make distance 0)
    if all(d == 0 for d in distances):
        raise ValueError("All positions cannot be the same value.")
        
    # Calculate GCD of the distances
    # Filter out 0s if any identical numbers were inputted
    valid_distances = [d for d in distances if d > 0]
    
    if not valid_distances:
        gcd_distance = 0
    else:
        gcd_distance = reduce(gcd, valid_distances)
    
    return {
        "original_positions": positions,
        "sorted_positions": sorted_positions,
        "distances": distances,
        "gcd": gcd_distance
    }