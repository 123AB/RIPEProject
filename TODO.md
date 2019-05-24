# TODO



- Read and write to pickle
- General characteristics of the network topology
- Vulnerability, different metrics for the network
- Information spreading



### Function to see if points (like AS) are within radius

```python
def in_circle(center_x, center_y, radius, x, y):
    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
    return square_dist <= radius ** 2
```

This function is going to be very expensive to run for all links. We could subdivide the map in a grid.