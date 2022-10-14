import matplotlib.pyplot as plt
 
 
x =[5, 7, 8, 7, 2, 17, 2, 9,
    4, 11, 12, 9, 6]
 
y =[99, 86, 87, 88, 100, 86,
    103, 87, 94, 78, 77, 85, 86]


plt.xlabel("Cost (# of steps)")
plt.ylabel("Success probability (%)")
plt.scatter(x, y, c ="blue")
plt.tight_layout()
 
# To show the plot
plt.show()

# from matplotlib import pyplot as plt
# import optuna


# def objective(trial):
#     x = trial.suggest_float("x", 0, 5)
#     y = trial.suggest_float("y", 0, 3)

#     v0 = 4 * x ** 2 + 4 * y ** 2
#     v1 = (x - 5) ** 2 + (y - 5) ** 2
#     return v0, v1


# study = optuna.create_study(directions=["minimize", "maximize"])
# study.optimize(objective, n_trials=10)

# optuna.visualization.matplotlib.plot_pareto_front(study, target_names = ["cost", "success probability"])
# plt.show()

