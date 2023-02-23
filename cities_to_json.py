import json

# Data to be written
dictionary = {
	"Дніпро": "Dnipro",
	"Київ": "Kyiv"
}

# Serializing json
json_object = json.dumps(dictionary, indent=4)

# Writing to sample.json
with open("cities_for_weather.json", "w") as outfile:
	outfile.write(json_object)
