import matplotlib.pyplot as plt
import matplotlib.animation as animation

class GraphInstance():
    def __init__(self):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        
        self.fig = fig
        self.ax = ax

    def graph_animation(self, i, temp, ys):
        # Draw x and y lists
        xs = list(range(0, len(ys)))
        self.ax.clear()
        self.ax.plot(xs, ys)

        # Format plot
        plt.xticks(rotation=45, ha='right')
        self.ax.set_ylim([0, 100])
        plt.subplots_adjust(bottom=0.30)
        plt.title('Canil do Reino Stock Prices')
        plt.ylabel('Market Cap')