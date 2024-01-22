medium_dose=("medium dose").upper()
full_dose= ("full dose").upper()
second_or_third_med_level=[('DPP4i').upper(), ('SGLT2i').upper(), ('oral GLP1ra').upper(), ('Pio').upper(), ('SU').upper()]

def first_time(current_hba1c,symptoms):
    proposed_med={}
    if(current_hba1c<7.0):
        proposed_med[("nonpharmacological therapy").upper()]=("No specific dose").upper()
    elif (current_hba1c>=7 and current_hba1c<=9):
        proposed_med[("Metformin").upper()]=medium_dose
    else:
        proposed_med[("Metformin").upper()]=full_dose
        if(symptoms=='YES'):
            proposed_med[("Basal insulin").upper()]=full_dose
        else:
            proposed_med[("You can choose any item from this list: {}".format(second_or_third_med_level)).upper()]=full_dose

    return(proposed_med)