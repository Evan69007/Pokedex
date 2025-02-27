import json
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

f = open('myenv/pokedex.json')
data = json.load(f)

def calculate_nb_pokemon():
    nb_pokemon = 0
    for pokemon in data['pokemon']:
        nb_pokemon += 1
    return nb_pokemon

def nb_pokemon_weight_more_10kg():
    nb_pokemon_weight_more_10kg = 0
    for i in data['pokemon']:
        weight_value = float(i['weight'].split()[0])
        if weight_value > 10:
            nb_pokemon_weight_more_10kg += 1
    return nb_pokemon_weight_more_10kg

def dict_to_tuple():
    pokemon_list = []
    for i in data['pokemon']:
        pokemon_list.append((i['name'], i['weight']))
    return pokemon_list

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
    return filtered_list

def get_all_evolutions(pokemon):
    evolutions = []
    if "next_evolution" in pokemon:
        for i in pokemon['next_evolution']:
            evolutions.append(i['name'])
    if len(evolutions) == 0:
        return ("No Evolutions")
    return evolutions

f.close()

def update_types():
    type1label.config(text="type(s): " + data['pokemon'][index]['type'][0])
    if data['pokemon'][index]['type'][1:]:
        type2label.config(text=data['pokemon'][index]['type'][1])
    else:
        type2label.config(text="")

def update_pokedex_entry():
    pokedex_entry.config(text="Pokedex Entry: " + data['pokemon'][index]['num'])

def update_name():
    label_name.config(text=data['pokemon'][index]['name'])

def update_height():
    height_entry.config(text="Height: " + data['pokemon'][index]['height'])

def update_weight():
    weight_entry.config(text="wheight: " + data['pokemon'][index]['weight'])

def update_egg():
    egg_entry.config(text="Distance to hatch: " + data['pokemon'][index]['egg'])

def update_evolutions():
    evolutions = get_all_evolutions(data['pokemon'][index])
    if len(evolutions) > 2:
        evolutions_entry.config(text="evolutions: " + evolutions)
    else:
        evolutions_entry.config(text="evolutions: " + ", ".join(evolutions))

def update_labels():
    update_name()
    update_types()
    update_pokedex_entry()
    update_height()
    update_weight()
    update_egg()
    update_evolutions()
    show_image_from_url(data['pokemon'][index]['img'])
    clicked.set("Search for a pokemon")

def get_all_pokemons():
    pokemon_list = []
    for pokemon in data['pokemon']:
        pokemon_list.append(pokemon['name'])
    return pokemon_list

# The window!
window = tk.Tk()

index = 0

# Global label for the image
label = None  # Initialize as None to avoid issues with global usage

def show_image_from_url(url):
    global label  # Reference the global label variable

    # Fetch the image from the URL using requests
    response = requests.get(url)
    img_data = response.content
    
    # Open the image using PIL
    img = Image.open(BytesIO(img_data))
    
    # Convert the image to a format Tkinter can handle (PhotoImage)
    img_tk = ImageTk.PhotoImage(img)

    # If the label already exists, destroy it
    if label:
        label.destroy()

    # Create a Label widget to display the image
    label = tk.Label(picture_frame, image=img_tk)
    label.image = img_tk  # Keep a reference to avoid garbage collection
    label.pack()

def previousPokemon():
    global index
    if index <= 0:
        index = len(data['pokemon']) - 1
    else:
        index -= 1
    update_labels()

def nextPokemon():
    global index
    if index >= len(data['pokemon']) - 1:
        index = 0
    else:
        index += 1
    update_labels()
    
def showSelected(pokemon):
    global index
    pokemon_index = 0
    for poke in data['pokemon']:
        if poke['name'] == pokemon:
            break
        pokemon_index += 1
    index = pokemon_index
    update_labels()

window.title("Pokedex")
window.geometry("800x500")
window.configure(background="crimson")

# Configure 4 rows and 3 columns.
window.rowconfigure([i for i in range(4)], minsize=50, weight=1)
window.columnconfigure([i for i in range(3)], minsize=50, weight=1)

### Name Frame
name_frame = tk.Frame(window, relief=tk.RAISED, borderwidth=4)
label_name = tk.Label(name_frame, text=data['pokemon'][index]['name'], font=("Futura", 16))
label_name.pack()
name_frame.grid(row=0, column=0)

### Picture Frame
picture_frame = tk.Frame(window, relief=tk.SUNKEN, borderwidth=2)
show_image_from_url(data['pokemon'][index]['img'])
picture_frame.grid(row=1, column=0)

### Type Frame
type_frame = tk.Frame(window, relief=tk.RAISED, borderwidth=2)
type1label = tk.Label(type_frame, text="type(s): " + data['pokemon'][index]['type'][0], font=("Futura", 12))
type1label.grid(row=0, column=0)
if data['pokemon'][index]['type'][1:]:
    type2label = tk.Label(type_frame, text=data['pokemon'][index]['type'][1], font=("Futura", 12))
else:
    type2label = tk.Label(type_frame, text="", font=("Futura", 12))
type2label.grid(row=0, column=1)
type_frame.grid(row=3, column=0)

### Search Frame
search_frame = tk.Frame(window, relief=tk.RAISED, borderwidth=2)
search_frame.columnconfigure([0, 1, 2, 3], weight=1)

label_previous = tk.Label(search_frame, font=("Futura", 16))
tk.Button(label_previous, text="Previous Pokemon", command=previousPokemon).pack()
label_previous.grid(row=0, column=0)

label_search = tk.Label(search_frame, font=("Futura", 16))
pokemon_names = get_all_pokemons()
clicked = tk.StringVar()
clicked.set("Search for a pokemon")
menu = tk.OptionMenu(label_search, clicked, *pokemon_names, command=showSelected)
menu.grid(row=0, column=1, padx=10)
label_search.grid(row=0, column=1)

label_next = tk.Label(search_frame, font=("Futura", 16))
tk.Button(label_next, text="Next Pokemon", command=nextPokemon).pack()
label_next.grid(row=0, column=3)

search_frame.grid(row=0, column=1, columnspan=2, sticky="ew")

### Info Frame
info_frame = tk.Frame(window, relief=tk.SUNKEN, borderwidth=4)
info_frame.rowconfigure([0, 1, 2], weight=1)
info_frame.columnconfigure([0, 1], weight=1)

pokedex_entry = tk.Label(info_frame, text="Pokedex Entry: " + data['pokemon'][index]['num'], font=("Futura", 16))
pokedex_entry.grid(row=0, column=0, columnspan=2)

height_entry = tk.Label(info_frame, text="Height: " + data['pokemon'][index]['height'], font=("Futura", 16))
height_entry.grid(row=1, column=0)

weight_entry = tk.Label(info_frame, text="wheight: " + data['pokemon'][index]['weight'], font=("Futura", 16))
weight_entry.grid(row=2, column=0)

egg_entry = tk.Label(info_frame, text="Distance to hatch: " + data['pokemon'][index]['egg'], font=("Futura", 16))
egg_entry.grid(row=1, column=1)

evolutions = get_all_evolutions(data['pokemon'][index])
if len(evolutions) > 2:
    evolutions_entry = tk.Label(info_frame, text="evolutions: " + evolutions, font=("Futura", 16))
else:
    evolutions_entry = tk.Label(info_frame, text="evolutions: " + ", ".join(evolutions), font=("Futura", 16))
evolutions_entry.grid(row=2, column=1)

info_frame.grid(row=1, rowspan=3, column=1, columnspan=2, sticky="nsew")

window.mainloop()
