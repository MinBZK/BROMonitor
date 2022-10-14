import json

# Script to validate the validity and constraints of the language json files
# Mostly a skeleton for when we want to do actual aimed validation
try:
    with open("app/backend/i18n/nl-NL.json") as json_file:
        json_object = json.load(json_file)

        # Validate lengths of the values
        for (key, value) in json_object.items():
            if len(value) > 256:
                raise Exception("Te lange string in waarde van key => " + key)

        print("Succesvol gevalideerd!")
except Exception as e:
    print("Error bij het valideren van de json! \n" + str(e))
