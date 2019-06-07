import matplotlib.pyplot as plt
import matplotlib.animation as animation

class GraphInstance():
    def __init__(self, client_address):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        
        self.fig = fig
        self.ax = ax
        self.title = client_address[0] + ", " + str(client_address[1])

    def graph_animation(self, i, temp, ys):
        # Draw x and y lists
        xs = list(range(0, len(ys)))
            
        self.ax.clear()
        try:
            self.ax.plot(xs, ys)
        except Exception:
            None #casos de concorrência que estragam a animação

        # Format plot
        plt.xticks(rotation=45, ha='right')
        self.ax.set_ylim([0, 100])
        plt.subplots_adjust(bottom=0.30)
        plt.title(self.title)
        plt.ylabel('Market Cap do Canil do Reino')
        plt.xlabel('Tempo decorrido')