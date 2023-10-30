import matplotlib.pyplot as plt

def plot(coords):
    x = []
    y = []
    for shape in coords:
        for e in shape.coordinates:
            for c in e.primitives:
                x.append(c.x)
                y.append(c.y)
    plt.scatter(x,y)
    plt.show()