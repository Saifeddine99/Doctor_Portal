import json
import copy
from encrypt import encrypt_data
#---------------------------------------------------------------------------
def save_symptoms(symptoms):
    #This is a json file containing standard clinical data in the OpenEHR standards form
    full_path_encounter_symptoms = 'encounter_symptoms_20231002120050_000001_1.json'
    #Demographic data file:
    with open(full_path_encounter_symptoms, 'r') as openfile:
        # Reading from json file
        json_object_encounter_symptoms = json.load(openfile)

    json_object_encounter_symptoms["content"][0]["data"]["events"][0]["data"]["items"][0]["value"]["value"]=encrypt_data(symptoms.upper())

    return json_object_encounter_symptoms
#---------------------------------------------------------------------------
def save_laboratory_test_results(current_hba1c,egfr,uacr):
    #This is a json file containing standard clinical data in the OpenEHR standards form
    full_path_laboratory_test_results = 'laboratory_result_report_20231003110928_000001_1.json'
    #Demographic data file:
    with open(full_path_laboratory_test_results, 'r') as openfile:
        # Reading from json file
        json_object_laboratory_test_results = json.load(openfile)
    
    laboratory_tests=[("hba1c").upper(), ("egfr").upper(), ("uacr").upper()]
    laboratory_test_results=[current_hba1c, egfr, uacr]
    
    laboratory_test_results_list=[]
    for x in range(3):
        laboratory_test_results_list.append(copy.deepcopy(json_object_laboratory_test_results))
        laboratory_test_results_list[-1]["content"][0]["data"]["events"][0]["data"]["items"][6]["items"][2]["value"]["magnitude"]=encrypt_data(str(laboratory_test_results[x]))
        laboratory_test_results_list[-1]["content"][0]["data"]["events"][0]["data"]["items"][0]["value"]["value"]=encrypt_data(laboratory_tests[x].upper())
    return(laboratory_test_results_list)
#---------------------------------------------------------------------------
def save_bmi(current_bmi,height,weight):
    #This is a json file containing standard clinical data in the OpenEHR standards form
    full_path_bmi_json = 'bmi_20231002121554_000001_1.json'
    #Demographic data file:
    with open(full_path_bmi_json, 'r') as openfile:
        # Reading from json file
        json_object_bmi = json.load(openfile)

    json_object_bmi["content"][0]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"]=encrypt_data(str(height))
    json_object_bmi["content"][1]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"]=encrypt_data(str(weight))
    json_object_bmi["content"][2]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"]=encrypt_data(str(current_bmi))

    return(json_object_bmi)
#---------------------------------------------------------------------------
def save_problem_list(frailty,heart_failure,established_CVD,hepatic_steatosis,strokes):
    #This is a json file containing standard clinical data in the OpenEHR standards form
    full_path_problem_list_json = 'problem_list.v1_20230913120942_000001_1.json'
    #Demographic data file:
    with open(full_path_problem_list_json, 'r') as openfile:
        # Reading from json file
        json_object_problem_list = json.load(openfile)

    problem_dict={
        "frailty":frailty,
        "heart_failure":heart_failure,
        "established_CVD":established_CVD,
        "hepatic_steatosis":hepatic_steatosis,
        "strokes":strokes
    }

    problem_list=[]
    for problem,value in problem_dict.items():
        if value=="YES":
            problem_list.append(copy.deepcopy(json_object_problem_list))
            problem_list[-1]["content"][0]["items"][0]["data"]["items"][0]["value"]["value"] = encrypt_data(problem.upper())

    return problem_list
#---------------------------------------------------------------------------
def save_risk_factors(CVRFs):
    #This is a json file containing standard clinical data in the OpenEHR standards form
    full_path_risk_factors_json = 'risk_factors_20231002120317_000001_1.json'
    #Demographic data file:
    with open(full_path_risk_factors_json, 'r') as openfile:
        # Reading from json file
        json_object_risk_factors = json.load(openfile)

    risk_factors=[]
    for cvrf in CVRFs:
        risk_factors.append(copy.deepcopy(json_object_risk_factors))
        risk_factors[-1]["content"][0]["data"]["items"][1]["items"][0]["value"]["value"] = encrypt_data(cvrf.upper())
    
    return(risk_factors)
#---------------------------------------------------------------------------
def save_medication_list(proposed_med):
    #This is a json file containing standard clinical data in the OpenEHR standards form
    full_path_medication_list = 'medication_list.v1_20230913120547_000001_1.json'
    #Demographic data file:
    with open(full_path_medication_list, 'r') as openfile:
        # Reading from json file
        json_object_medication_list = json.load(openfile)
    medication_list=[]
    for drug,dose in proposed_med.items():
        medication_list.append(copy.deepcopy(json_object_medication_list))
        medication_list[-1]["content"][0]["items"][0]["description"]["items"][0]["value"]["value"] = encrypt_data(drug.upper())
        medication_list[-1]["content"][0]["items"][0]["description"]["items"][2]["items"][3]["value"]["value"] = encrypt_data(dose.upper())
    return(medication_list)
#---------------------------------------------------------------------------
def save_age_to_compo(age):
    #This is a json file containing standard clinical data in the OpenEHR standards form
    full_path_age_compo = 'age.v1_20231106112026_000001_1.json'
    #Demographic data file:
    with open(full_path_age_compo, 'r') as openfile:
        # Reading from json file
        json_object_age_compo = json.load(openfile)

    json_object_age_compo["content"][0]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"]=encrypt_data(str(age))

    return(json_object_age_compo)