import pymongo as py
myclient=py.MongoClient("mongodb://localhost:27017")

from decrypt import decrypt_data

#Relating data to "clinical_data"
medical_data_coll=myclient["Clinical_database"]["Medical data"]
medical_hist_coll=myclient["Clinical_database"]["Medical history"]
#relating data to "demographic_database"
demographic_data_coll=myclient["Demographic_database"]["Demographic data"]
#---------------------------------------------------------------------------
#this function allows the generation of a dictionary containing all data to be later converted to a pandas dataframe
#For each variable: if it's not found in database then we give it the "UNKNOWN" value
def dict_generation(consent_uuids):
    #preparing the demographic data to be displayed:
    gender=[]
    dem_uuidz_list=[]
    cursor_demog = demographic_data_coll.find({"uuid": {"$in": consent_uuids}})
    for demographic_doc in cursor_demog:

        occurence=medical_data_coll.count_documents({"uuid":demographic_doc["uuid"]})

        for occ in range(occurence):
            dem_uuidz_list.append(demographic_doc["uuid"])
            gender.append(decrypt_data(demographic_doc["demographic data"]["details"]["items"][3]["value"]["value"]))

    #preparing the medical data to be displayed:
    age=[]
    vital_status=[]
    symptoms=[]

    anaemia=[]
    diabetes=[]
    frailty=[]
    heart_failure=[]
    established_CVD=[]
    hepatic_steatosis=[]
    strokes=[]

    hypertension=[]
    hypercholesterolemia=[]
    albuminuria=[]
    smoking=[]
    early_CVD=[]

    med_uuidz_list=[]
    #Here we'll be querying medical_data.
    cursor_med_data=medical_data_coll.find({"uuid": {"$in": consent_uuids}})
    for med_data_doc in cursor_med_data:
        med_uuidz_list.append(med_data_doc["uuid"])
        try:
            age.append(int(decrypt_data(med_data_doc["age"]["content"][0]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"])))
        except:
            age.append("UNKNOWN")
        try:
            vital_status.append(decrypt_data(med_data_doc["vital status"]["content"][0]["data"]["events"][0]["data"]["items"][0]["value"]["value"]))
        except:
            vital_status.append("UNKNOWN")
        try:
            symptoms.append(decrypt_data(med_data_doc["symptoms"]["content"][0]["data"]["events"][0]["data"]["items"][0]["value"]["value"]))
        except:
            symptoms.append("UNKNOWN")

        anaemia.append("NO")
        diabetes.append("NO")
        frailty.append("NO")
        heart_failure.append("NO")
        established_CVD.append("NO")
        hepatic_steatosis.append("NO")
        strokes.append("NO")

        try:
            problem_list=list(med_data_doc["problem list"])
            for problem in problem_list:
                problem_name = decrypt_data(problem["content"][0]["items"][0]["data"]["items"][0]["value"]["value"])
                
                if problem_name==("anaemia").upper():
                    anaemia[-1]="YES"
                if problem_name==("diabetes").upper():
                    diabetes[-1]="YES"
                if problem_name==("frailty").upper():
                    frailty[-1]="YES"
                if problem_name==("heart_failure").upper():
                    heart_failure[-1]="YES"
                if problem_name==("established_CVD").upper():
                    established_CVD[-1]="YES"
                if problem_name==("hepatic_steatosis").upper():
                    hepatic_steatosis[-1]="YES"
                if problem_name==("strokes").upper():
                    strokes[-1]="YES"
        except:
            pass

        hypertension.append("NO")
        hypercholesterolemia.append("NO")
        albuminuria.append("NO")
        smoking.append("NO")
        early_CVD.append("NO")

        try:
            risk_factors=list(med_data_doc["risk factors"])
            for cvrf in risk_factors:
                cvrf_name=decrypt_data(cvrf["content"][0]["data"]["items"][1]["items"][0]["value"]["value"])
                
                if cvrf_name==("High_blood_pressure").upper():
                    hypertension[-1]="YES"
                if cvrf_name==("hypercholesterolemia").upper():
                    hypercholesterolemia[-1]="YES"
                if cvrf_name==("albuminuria").upper():
                    albuminuria[-1]="YES"
                if cvrf_name==("smoking").upper():
                    smoking[-1]="YES"
                if cvrf_name==("family history of early CVD").upper():
                    early_CVD[-1]="YES"

        except:
            pass


    #preparing the medical history to be displayed:
    bmi=[]
    hba1c=[]
    egfr=[]
    uacr=[]
    creatinine_phosphokinase=[]
    ejection_fraction=[]
    platelets=[]
    serum_creatinine=[]
    serum_sodium=[]
    
    cursor_med_hist=medical_hist_coll.find({"uuid": {"$in": consent_uuids}})
    for med_hist_doc in cursor_med_hist:
        try:
            bmi.append(float(decrypt_data(med_hist_doc["analytics"][1]["content"][2]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"])))
        except:
            bmi.append("UNKNOWN")
        
        hba1c.append("UNKNOWN")
        egfr.append("UNKNOWN")
        uacr.append("UNKNOWN")
        creatinine_phosphokinase.append("UNKNOWN")
        ejection_fraction.append("UNKNOWN")
        platelets.append("UNKNOWN")
        serum_creatinine.append("UNKNOWN")
        serum_sodium.append("UNKNOWN")

        try:
            analytics=list(med_hist_doc["analytics"][0])
            for test in analytics:
                test_name = decrypt_data(test["content"][0]["data"]["events"][0]["data"]["items"][0]["value"]["value"])
                test_result = float(decrypt_data(test["content"][0]["data"]["events"][0]["data"]["items"][6]["items"][2]["value"]["magnitude"]))
                if test_name==("egfr").upper():
                    egfr[-1]=test_result
                if test_name==("uacr").upper():
                    uacr[-1]=test_result
                if test_name==("hba1c").upper():
                    hba1c[-1]=test_result
                if test_name==("creatinine_phosphokinase").upper():
                    creatinine_phosphokinase[-1]=test_result
                if test_name==("ejection_fraction").upper():
                    ejection_fraction[-1]=test_result
                if test_name==("platelets").upper():
                    platelets[-1]=test_result
                if test_name==("serum_creatinine").upper():
                    serum_creatinine[-1]=test_result
                if test_name==("serum_sodium").upper():
                    serum_sodium[-1]=test_result

        except:
            pass

    # Create a dictionary to map values in med_uuidz_list to their indices
    index_mapping = {value: index for index, value in enumerate(med_uuidz_list)}
    # Sort list2 and list3 based on the order in med_uuidz_list
    sorted_demog_uuidz_list, gender = zip(*sorted(zip(dem_uuidz_list, gender), key=lambda x: index_mapping[x[0]]))

    #Putting data to be displayed in a dictionary:
    csv_dict={  "Gender":gender,
                "Age":age,
                "Vital Status":vital_status,
                "Symptoms":symptoms,

                "Anaemia":anaemia,
                "Diabetes":diabetes,
                "Frailty":frailty,
                "Heart Failure":heart_failure,
                "Established CVD":established_CVD,
                "Hepatic Steatosis":hepatic_steatosis,
                "Strokes":strokes,

                "Smoking":smoking,
                "High Blood Pressure":hypertension,
                "Albuminuria":albuminuria,
                "Hypercholesterolemia":hypercholesterolemia,
                "Family History Of Early CVD":early_CVD,

                "BMI": bmi,

                "HbA1c": hba1c,
                "eGFR": egfr,
                "UACR": uacr,
                "Creatinine_Phosphokinase": creatinine_phosphokinase,
                "ejection_Fraction": ejection_fraction,
                "Platelets": platelets,
                "Serum_Creatinine":serum_creatinine,
                "Serum_sodium":serum_sodium
                }

    return csv_dict