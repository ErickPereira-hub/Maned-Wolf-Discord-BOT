import matplotlib.pyplot as plt

plt.style.use("dark_background") #<--- setting the style of the graph
plt.plot([1, 2, 3, 4], [-10, -121, 12, 9], color = "#2F2FE4", linewidth = 2) #<--- Plotting the graph
plt.xlabel("Time (days)")
plt.ylabel("Quantity of members")
plt.savefig("XXX.png", dpi = 75)