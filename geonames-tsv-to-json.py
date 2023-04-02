import json


def lineToJSON(line: str) -> dict:
    object = {}

    # TODO: convert to correct types
    # TODO: add None if empty String

    values = line.split("\t")
    tableColumns = ["geonameid", "name", "asciiname", "alternatenames", "latitude", "longitude", "feature class", "feature code", "country code",
                    "cc2", "admin1 code", "admin2 code", "admin3 code", "admin4 code", "population", "elevation", "dem", "timezone", "modification date"]

    for i in range(len(values)):
        object[tableColumns[i]] = values[i]

    return object


def isMountain(geoObject: dict) -> bool:
    return geoObject["feature class"] == "T" and geoObject["feature code"] == "MT"


with open("allCountries.txt", "r") as file:
    mountains = []
    for line in file:
        object = lineToJSON(line.strip())
        if isMountain(object):
            mountains.append(object)
    # print(mountains)
    # print(len(mountains))

with open("mountains-worldwide.json", "w+") as file:
    json.dump(mountains, file, indent=4)