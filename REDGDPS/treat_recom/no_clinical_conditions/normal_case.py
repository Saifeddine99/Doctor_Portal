from REDGDPS.treat_recom.no_clinical_conditions.First_time import first_time
from REDGDPS.treat_recom.no_clinical_conditions.treatment_reco_main import recommended_treatment

def normal_case(previous_state_,hba1c_records,symptoms,treatment_data):

    proposed_med={}
    # Now let's deal with people having diabetes for the first time:
    if(previous_state_=="First time"):
        next_date="Your next check is after 3 months"
        #These users have currently discovered their suffer from diabetes...
        proposed_med=first_time(hba1c_records[0],symptoms)

    else:
        #These users are already suffering from diabetes...
        
        target_=6.5 #target(previous_state_,treatment_data) ###### This function must have a big update !
        #Here we will start iterating the above target conditions
        if(hba1c_records[0]>target_):
            next_date="Your next check is after 3 months"
            proposed_med=recommended_treatment(treatment_data,hba1c_records,target_,symptoms) 
            
        else:
            next_date="Your next check is after 6 months"
            proposed_med=treatment_data

    return(proposed_med,next_date)
