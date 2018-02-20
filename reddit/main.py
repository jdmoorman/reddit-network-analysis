from data.experiment_setup import experiment

exp = experiment(name="hello")

with exp.open("world.txt", "w") as f:
	f.write("lol")


with exp.open("world.txt", "a") as f:
	f.write("wut")
