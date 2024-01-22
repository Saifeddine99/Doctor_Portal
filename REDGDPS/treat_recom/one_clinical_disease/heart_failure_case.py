def heart_failure_(hba1c_records,previous_state,med_dose_last_time):
    full_dose= ("full dose").upper()
    second_or_third_med_level=[('DPP4i').upper(), ('oral GLP1ra').upper(), ('Pio').upper(), ('SU').upper()]

    next_date="Your next check is after 3 months"
    proposed_med={}
    #If the patient will get treatment for the first time
    if(previous_state=="First time"):
        proposed_med[("Metformin").upper()]=full_dose
        proposed_med[("SGLT2i").upper()]=full_dose

    else:
        #The target variable represents the threshold to decide whether the patient achieved objective or not
        target_=6.5 ####target(previous_state,med_dose_last_time)
        proposed_med=med_dose_last_time
        current_hba1c=hba1c_records[0]
        if(current_hba1c>=target_):
            #Here we'll be working on the case of someone using only metformin+ SGLT2i
            if(("Metformin").upper() in med_dose_last_time and ("SGLT2i").upper() in med_dose_last_time and len(med_dose_last_time)==2):
                proposed_med[("Metformin").upper()]=full_dose
                proposed_med[("SGLT2i").upper()]=full_dose
                proposed_med["You can choose any item from this list: {}".format(second_or_third_med_level)]=full_dose
            # Here we move to the step of recommending basal insulin
            elif(("Metformin").upper() in med_dose_last_time and not(("Basal insulin").upper() in med_dose_last_time) and ("SGLT2i").upper() in med_dose_last_time and len(med_dose_last_time)>=3 ):
                drugs=list(med_dose_last_time.keys())
                drugs.remove(("Metformin").upper())
                drugs.remove(("SGLT2i").upper())
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
        else:# Here we work on the case of patients who achieved the target
            next_date="Your next check is after 6 months"
            for med_item in med_dose_last_time.keys():
                proposed_med[med_item]=full_dose
    return(proposed_med,next_date)
