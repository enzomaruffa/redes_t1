import matplotlib.pyplot as plt
import matplotlib.animation as animation

class GraphInstance():
    # Inicialização do gráfico
    def __init__(self, client_address):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        
        self.drawing = True

        self.fig = fig
        self.ax = ax
        self.title = client_address[0] + ", " + str(client_address[1])

    def graph_animation(self, i, temp, ys):
        # Cria as listas de x e y
        y = ys.copy() # Importante manter uma cópia para não ter problemas de concorrência
        x = list(range(0, len(y)))
        
        self.ax.clear()
        try:
            self.ax.plot(x, y)
        except Exception:
            None # Mitiga a poluição do log com casos de concorrência estranhos e não destrutivos

        # Format plot
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.title(self.title)
        plt.ylabel('Market Cap do Canil dos Outros Reinos')
        plt.xlabel('Tempo decorrido')