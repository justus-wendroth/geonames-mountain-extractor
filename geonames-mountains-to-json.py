import json
import argparse


def toString(x: str):
    if (x == ""):
        return None

    return str(x)


def toInt(x: str):
    if (x == ""):
        return None

    return int(x)


def toFloat(x: str):
    if (x == ""):
        return None

    return float(x)


def lineToJSON(line: str) -> dict:
    """Converts a tsv line in a geonames table to a JSON object."""
    object = {}

    values = line.split("\t")
    tableColumns = [("geonameid", toString), ("name", toString), ("asciiname", toString), ("alternatenames", toString), ("latitude", toFloat), ("longitude", toFloat), ("feature class", toString), ("feature code", toString), ("country code", toString),
                    ("cc2", toString), ("admin1 code", toString), ("admin2 code", toString), ("admin3 code", toString), ("admin4 code", toString), ("population", toInt), ("elevation", toInt), ("dem", toInt), ("timezone", toString), ("modification date", toString)]

    for i in range(len(values)):
        object[tableColumns[i][0]] = tableColumns[i][1](values[i])

    return object


def isMountain(geoObject: dict) -> bool:
    """A mountain can be of feature class peak (PK) or mountain (MT)."""
    return geoObject["feature class"] == "T" and (geoObject["feature code"] == "MT" or geoObject["feature code"] == "PK")


def convertToMountain(geoObject: dict) -> dict:
    """Converts a geonames geoObject to a mountain object."""

    mountain = {}
    mountain["id"] = geoObject["geonameid"]
    mountain["name"] = geoObject["name"]
    mountain["latitude"] = geoObject["latitude"]
    mountain["longitude"] = geoObject["longitude"]
    mountain["featureCode"] = geoObject["feature code"]

    if geoObject["elevation"] == None:
        mountain["elevation"] = geoObject["dem"]
    else:
        mountain["elevation"] = geoObject["elevation"]

    return mountain


def extractMountains(inputFile: str, outputFile: str, minimumElevation: int = 0) -> 'list[dict]':
    """Extracts the mountains out of the input file."""
    mountains = []

    with open(args.input, "r") as file:
        for line in file:
            object = lineToJSON(line.strip())
            if isMountain(object):
                mountain = convertToMountain(object)
                if mountain["elevation"] >= minimumElevation:
                    mountains.append(mountain)

    return mountains


def writeMountains(mountains: 'list[dict]', outputFile: str):
    """Writes the list of mountains to the output file."""
    with open(args.output, "w+") as file:
        json.dump(mountains, file, indent=4)


parser = argparse.ArgumentParser(
    description="Convert geonames tsv to JSON and filter out non mountains.")

parser.add_argument("input", type=str, help="Input file geonames tsv")
parser.add_argument("output", type=str, help="Output file JSON with mountains")
parser.add_argument("--elevation", type=int, help="Minimum elevation of the mountains")

args = parser.parse_args()

mountains = extractMountains(args.input, args.output, args.elevation)
writeMountains(mountains, args.output)
