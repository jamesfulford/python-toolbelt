# plots.py
# by James Fulford
# use to visualize data.


import matplotlib.pyplot as plt


def bar(frequencies, x="Class", y="Frequency", title="Frequencies", save=None):
    """
    Shows a bar chart of given frequencies.
        x is the x axis label (default: Class)
        y is the y axis label (default: Frequency)
        title is the title of the chart (default: Frequencies)
        save is the path + name of where to save a .png of this file.
            ex: save="/Users/averagejoe/survey results"
            will save the chart to "/Users/averagejoe" directory
            with name "survey results.png"
    """
    fig, ax = plt.subplots()
    ax.set_xlabel(x, fontsize=15)
    ax.set_ylabel(y, fontsize=15)
    ax.set_title(title, fontsize=24, fontweight='bold')
    plt.bar(range(len(frequencies)), frequencies.values(), align="center")
    plt.xticks(range(len(frequencies)), sorted(list(frequencies.keys())))
    if save:
        plt.savefig(save + ".png")
    plt.show()


def pie(frequencies, title="Share", save=None):
    """
    Shows a pie chart of given frequencies.
        title is the title of the chart (default: Share)
        save is the path + name of where to save a .png of this file.
            ex: save="/Users/averagejoe/survey results"
            will save the chart to "/Users/averagejoe" directory
            with name "survey results.png"
    """
    fig, ax = plt.subplots()
    plt.pie(frequencies.values(), labels=frequencies.keys())
    if save:
        plt.savefig(save + ".png")
    plt.show()

# pie(james, save="james")
