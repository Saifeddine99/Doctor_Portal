def ckd_ob_cvr(current_eGFR,current_UACR,current_BMI,CVRFs):
    #chronic kidney disease
    chronic_kidney_disease='NO' if current_eGFR>=60 and current_UACR<=30 else 'YES'
    #obesity
    obesity='YES' if current_BMI>=30 else 'NO'
    #High CVR:
    High_CVR='YES' if len(CVRFs)>=3 else 'NO'
    return(chronic_kidney_disease,obesity,High_CVR)

def clinical_priorities(obesity, frailty, chronic_kidney_disease, heart_failure, established_CVD,High_CVR,current_eGFR,current_UACR):

    if(obesity==frailty==chronic_kidney_disease==heart_failure==established_CVD=='NO'):
        return(['No other clinical conditions',])
    
    #Before deployment, this part needs to be checked by an expert:
    elif(chronic_kidney_disease=='YES' and current_eGFR<30):
        return(['critical_chronic_kidney_disease',])
    elif(established_CVD=='YES' or High_CVR=='YES'):
        reason_='established_CVD' if established_CVD=='YES' else 'High_CVR'
        return(['established_cvd_or_high_cvr',reason_])
    elif(frailty=='YES'):
        return(['frailty',])
    elif(heart_failure=='YES'):
        return(['heart_failure',])
    elif(chronic_kidney_disease=='YES'and ((30<=current_eGFR<=59) or (current_UACR>30))):
        return(['non_critical_chronic_kidney_disease',])
    elif(obesity=='YES'):
        return(['obesity',])
