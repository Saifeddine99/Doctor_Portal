medium_dose=("medium dose").upper()
full_dose= ("full dose").upper()

#This function finds the name of the "ONE" chosen medication from the list.
def find_item_1(med_dose_last_time):
    item=''
    for key in med_dose_last_time:
        if (key != ("nonpharmacological therapy").upper() and key != ("Metformin").upper()):
            item=key
    return(item)

def niad_check(med_dose_last_time):
    niad_list=[('DPP4i').upper(), ('SGLT2i').upper(), ('oral GLP1ra').upper(), ('Pio').upper(), ('SU').upper()]
    score=0
    for key in med_dose_last_time:
        if key in niad_list :
            score+=1
    if (('DPP4i').upper() in med_dose_last_time and ('oral GLP1ra').upper() in med_dose_last_time):
        score=0
    return(score)

def recommended_treatment(med_dose_last_time,hba1c_records,target,symptoms):

    #this is the list of the second/third level medications
    niad_list=[('DPP4i').upper(), ('SGLT2i').upper(), ('oral GLP1ra').upper(), ('Pio').upper(), ('SU').upper()]

    current_hba1c=hba1c_records[0]
    previous_hba1c=hba1c_records[1]
    if (len(hba1c_records)==3):
        before_previous_hba1c=hba1c_records[2]

    proposed_med=med_dose_last_time
    
#Here we are working on the case of a user using only nonpharmacological therapy
    if ((("nonpharmacological therapy").upper() in med_dose_last_time) and len(med_dose_last_time)==1):
        if(current_hba1c>=7):
            proposed_med[("Metformin").upper()]=medium_dose

        elif (len(hba1c_records)==2):
            if(previous_hba1c<7):
                proposed_med=med_dose_last_time
            else:
                proposed_med={("this_cond").upper():("Doesn't exist").upper()}
                
        elif(len(hba1c_records)==3):
            if(6.5<=previous_hba1c<7 and 6.5<=before_previous_hba1c<7):
                proposed_med[("Metformin").upper()]=medium_dose
            elif (previous_hba1c>=7 or before_previous_hba1c>=7):
                proposed_med={("this_cond").upper():("Doesn't exist").upper()}
            elif (previous_hba1c<6.5 or before_previous_hba1c<6.5):
                proposed_med=med_dose_last_time
            else:
                proposed_med={("this_cond").upper():("Doesn't exist").upper()}

        else:
            proposed_med={("this_cond").upper():("Doesn't exist").upper()}

    #Here we'll be working on the case of someone using only metformin
    elif (((("nonpharmacological therapy").upper() in med_dose_last_time) and (("Metformin").upper() in med_dose_last_time) and len(med_dose_last_time)==2) or ((("Metformin").upper() in med_dose_last_time) and len(med_dose_last_time)==1)):
        #proposed_med=med_dose_last_time
        if(med_dose_last_time[("Metformin").upper()] == medium_dose):
            if(target<current_hba1c<=8):
                proposed_med[("Metformin").upper()]=full_dose
            elif (8<current_hba1c<=9):
                proposed_med[("Metformin").upper()]=full_dose
                proposed_med[("You can choose any item from this list: {}".format(niad_list)).upper()]=medium_dose
            else:
                proposed_med={}
                proposed_med[("Visit a doctor").upper()]=("Critical situation").upper()
        else:
            proposed_med[("You can choose any item from this list: {}".format(niad_list)).upper()]=medium_dose
    # Here we're working on Metformin + only one drug from the niad_list
    elif ((len(med_dose_last_time)==2 and not(("nonpharmacological therapy").upper() in med_dose_last_time)) or ((("nonpharmacological therapy").upper() in med_dose_last_time) and len(med_dose_last_time)==3)) and niad_check(med_dose_last_time)==1 and not(("Basal insulin").upper() in med_dose_last_time) and (("Metformin").upper() in med_dose_last_time):
        if(symptoms=="YES" and current_hba1c>9 and not(("nonpharmacological therapy").upper() in med_dose_last_time)):
            proposed_med={}
            proposed_med[("Metformin").upper()]=full_dose
            proposed_med[("Basal insulin").upper()]=full_dose
        else:
            first_med_from_list= find_item_1(med_dose_last_time)

            if(first_med_from_list==("DPP4i").upper()):
                niad_list.remove(("oral GLP1ra").upper())
            elif(first_med_from_list==("oral GLP1ra").upper()):
                niad_list.remove(("DPP4i").upper())

            if(target<current_hba1c<=8):
                if(med_dose_last_time[("Metformin").upper()]==med_dose_last_time[first_med_from_list]==full_dose):
                    niad_list.remove(first_med_from_list)
                    proposed_med[("You can choose any item from this list: {}".format(niad_list)).upper()]=full_dose
                else:
                    proposed_med[("Metformin").upper()]=full_dose
                    proposed_med[first_med_from_list]=full_dose    
            elif (8<current_hba1c<=9):
                proposed_med[("Metformin").upper()]=full_dose
                proposed_med[first_med_from_list]=full_dose 
                niad_list.remove(first_med_from_list)
                proposed_med[("You can choose any item from this list: {}".format(niad_list)).upper()]=full_dose
            else:
                proposed_med={}
                proposed_med[("Visit a doctor").upper()]=("Critical situation").upper()
    # Here we're working on Metformin + strictly more than 1 drug from the niad_list
    elif ((len(med_dose_last_time)>=3 and not(("nonpharmacological therapy").upper() in med_dose_last_time)) or ((("nonpharmacological therapy").upper() in med_dose_last_time) and len(med_dose_last_time)>=4)) and not(("Basal insulin").upper() in med_dose_last_time) and (("Metformin").upper() in med_dose_last_time) and niad_check(med_dose_last_time)>=2:
        
        if(("DPP4i").upper() in med_dose_last_time):
            niad_list.remove(("oral GLP1ra").upper())
        elif(("oral GLP1ra").upper() in med_dose_last_time):
            niad_list.remove(("DPP4i").upper())

        if(target<current_hba1c<=8):
                #Here we will add another drug
                for key in med_dose_last_time:
                    if(key!= ("nonpharmacological therapy").upper()):
                        proposed_med[key]=full_dose
                    if(key != ("nonpharmacological therapy").upper() and key != ("Metformin").upper()):
                        niad_list.remove(key)
                if( len(niad_list)>0):
                    proposed_med[("You can choose any item from this list: {}".format(niad_list)).upper()]=full_dose  
                else:
                    proposed_med={}
                    proposed_med[("Basal insulin").upper()]=full_dose
        elif (8<current_hba1c<=9):
            proposed_med={}
            proposed_med[("Basal insulin").upper()]=full_dose
        else:
            proposed_med={}
            proposed_med[("Visit a doctor").upper()]=("Critical situation").upper()
    #Here we will work on the case of patient using met+ insulin
    elif ((("Basal insulin").upper() in med_dose_last_time) and (("Metformin").upper() in med_dose_last_time) and (len(med_dose_last_time)==2)):
        proposed_med={}
        proposed_med[("Metformin").upper()]=full_dose
        if(symptoms=="NO" and current_hba1c<=9):
            proposed_med[("You can choose any item from this list: {}".format(niad_list)).upper()]=full_dose        
        else:
            proposed_med[("Basal insulin").upper()]=full_dose
    elif(("Basal insulin").upper() in med_dose_last_time):
        proposed_med={}
        proposed_med[("Basal insulin").upper()]= full_dose
    else:
        proposed_med={("this_cond").upper():("Doesn't exist").upper()}
    return(proposed_med)