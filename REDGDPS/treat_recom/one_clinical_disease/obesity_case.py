def obese(hba1c_records,previous_state,current_BMI,med_dose_last_time):

    full_dose= ("full dose").upper()
    second_or_third_med_level=[('DPP4i').upper(), ('SGLT2i').upper(), (("oral GLP1ra").upper()).upper(), ('Pio').upper(), ('SU').upper()]

    next_date="Your next check is after 3 months"
    proposed_med={}
    #If the patient will get treatment for the first time
    if(previous_state=="First time"):
        proposed_med[("Metformin").upper()]=full_dose
    else:
        #The target variable represents the threshold to decide whether the patient achieved objective or not
        target_=6.5 ####target(previous_state,med_dose_last_time)
        proposed_med=med_dose_last_time
        current_hba1c=hba1c_records[0]
        if(current_hba1c>=target_):
            #Here we'll be working on the case of someone using only metformin
            if([("Metformin").upper()] == list(med_dose_last_time.keys())):
                proposed_med[("Metformin").upper()]=full_dose
                if(current_BMI>35):
                    proposed_med["GLP-1RA"]=full_dose
                    proposed_med["Consider also bariatric surgery"]="∅"
                else:
                    proposed_med["SGLT2i or GLP1RA or dual GIP/GLP1ra"]=full_dose
            #In the comming 2 elif conditions we'll be working on the case of someone using metformin + one treatment from this list ["SGLT2i or GLP1RA or dual GIP/GLP1ra"]    
            elif(("Metformin").upper() in med_dose_last_time and ("SGLT2i").upper() in med_dose_last_time and len(med_dose_last_time)==2):
                proposed_med[("Metformin").upper()]=full_dose
                proposed_med[("SGLT2i").upper()]=full_dose
                second_or_third_med_level.remove(("SGLT2i").upper() )
                proposed_med["You can choose any item from this list: {}".format(second_or_third_med_level)]=full_dose
            elif(("Metformin").upper() in med_dose_last_time and (("GLP1RA").upper() in med_dose_last_time or ("dual GIP/GLP1ra").upper() in med_dose_last_time) and len(med_dose_last_time)==2):
                proposed_med[("Metformin").upper()]=full_dose
                if(("dual GIP/GLP1ra").upper() in med_dose_last_time):
                    proposed_med["dual GIP/GLP1ra"]=full_dose
                else:
                    proposed_med[("GLP1RA").upper()]=full_dose
                
                second_or_third_med_level.remove(("oral GLP1ra").upper())
                second_or_third_med_level.remove(('DPP4i').upper())
                proposed_med["You can choose any item from this list: {}".format(second_or_third_med_level)]=full_dose

            # Here we move to the step of recommending basal insulin 
            elif(("Metformin").upper() in med_dose_last_time and not(("Basal insulin").upper() in med_dose_last_time) and len(med_dose_last_time)>=3 and ((("SGLT2i").upper() in med_dose_last_time and not(("GLP1RA").upper() in med_dose_last_time)) or ((("GLP1RA").upper() in med_dose_last_time or ("dual GIP/GLP1ra").upper() in med_dose_last_time) and not(("DPP4i").upper() in med_dose_last_time)))):
                drugs=list(med_dose_last_time.keys())
                drugs.remove(("Metformin").upper())
                
                if(("GLP1RA").upper() in drugs):  
                    drugs.remove(("GLP1RA").upper())
                
                if(("dual GIP/GLP1ra").upper() in drugs):  
                    drugs.remove(("dual GIP/GLP1ra").upper())

                logic_drugs=1
                for item in drugs:
                    if(item not in second_or_third_med_level):
                        logic_drugs=0
                if(logic_drugs==1): 
                    proposed_med={}
                    proposed_med[("Basal insulin").upper()]=full_dose
                else:
                    proposed_med={}
                    proposed_med["Can't recommend treatment for this case !"]=""
            elif(("Basal insulin").upper() in med_dose_last_time):
                proposed_med={}
                proposed_med[("Basal insulin").upper()]= full_dose
            else:
                #Here we deal with treatments out of algorithm logic 
                proposed_med={}
                proposed_med["Can't recommend treatment for this case !"]=""
        else:
            # Here we work on the case of patients who achieved the target
            next_date="Your next check is after 6 months"
            for med_item in med_dose_last_time.keys():
                proposed_med[med_item]=full_dose
                
    return(proposed_med,next_date)
