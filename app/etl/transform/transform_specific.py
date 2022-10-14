import json

# Transforms the nested objects in CPT's to be flat.
# - Because of the way the data is modelled, a one-to-many relation is expected
# - We know its one-to-one, hence we can flatten


def transform_cpt_nesteds(json_input):
    penetrometer_survey = {}
    penetration_test = {}

    for key, value in (
        json_input["cptConePenetrometerSurveyCollection"][0][
            "cptConePenetrationTestCollection"
        ][0]
    ).items():
        penetration_test[key] = value

    for key, value in (json_input["cptConePenetrometerSurveyCollection"][0]).items():
        penetrometer_survey[key] = value

    penetrometer_survey.pop("cptConePenetrationTestCollection")
    penetrometer_survey["conePenetrationTest"] = penetration_test

    json_input.pop("cptConePenetrometerSurveyCollection")
    json_input["conePenetrometerSurvey"] = penetrometer_survey

    return json_input


transformer_mapping = {
    "cpt": transform_cpt_nesteds,
}
