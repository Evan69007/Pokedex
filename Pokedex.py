import json

f = open('pokedex.json')

data = json.load(f)


def calculate_nb_pokemon():
	nb_pokemon = 0
	for pokemon in data['pokemon']:
		nb_pokemon += 1
	return nb_pokemon

# print(calculate_nb_pokemon())

def nb_pokemon_weight_more_10kg():
	nb_pokemon_weight_more_10kg = 0
	for i in data['pokemon']:
		weight_value = float(i['weight'].split()[0])
		if weight_value > 10:
			nb_pokemon_weight_more_10kg += 1
	return (nb_pokemon_weight_more_10kg)

# print(nb_pokemon_weight_more_10kg())


def dict_to_tuple():
	pokemon_list = []
	for i in data['pokemon']:
		pokemon_list.append((i['name'], i['weight']))
	return (pokemon_list)

data_in_tuple = dict_to_tuple()

def filter_by_weight():
	filtered_list = data_in_tuple
	i = 0
	for i in range(len(filtered_list)):
		j = i + 1
		for j in range(len(filtered_list) - 1):
			weight_value_i = float(filtered_list[i][1].split()[0])
			weight_value_j = float(filtered_list[j][1].split()[0])
			if (weight_value_i < weight_value_j):
				temp = filtered_list[i]
				filtered_list[i] = filtered_list[j]
				filtered_list[j] = temp
			j += 1
		i += 1
	return (filtered_list)


# print(filter_by_weight())


def get_all_evolutions(pokemon):
	evolutions = []
	for i in pokemon['next_evolution']:
		evolutions.append(i['name'])
	if (len(evolutions) == 0):
		return ("Pas d'évolutions")
	return (evolutions)

# print(get_all_evolutions(data['pokemon'][0]))

f.close()