def parameter_to_directory(parameter):

    switcher={
        "Name": "demographic data.identities.0.details.items.0.value.value",
        "Surname": "demographic data.identities.0.details.items.1.value.value",
        "Gender": "demographic data.details.items.3.value.value",
        "Birth date": "demographic data.details.items.0.items.0.value.value",
        "Country of birth": "demographic data.details.items.0.items.1.value.value",
        "Province of birth": "demographic data.details.items.0.items.2.value.value",
        "Town of birth": "demographic data.details.items.0.items.3.value.value",
        "DNI": "demographic data.details.items.0.items.5.value.value",
        "Street name": "demographic data.contacts.0.addresses.0.details.items.0.items.0.value.value",
        "Street N°": "demographic data.contacts.0.addresses.0.details.items.0.items.1.value.value",
        "Postal Code": "demographic data.contacts.0.addresses.0.details.items.1.value.value",
        "Town": "demographic data.contacts.0.addresses.0.details.items.2.value.value",
        "Province": "demographic data.contacts.0.addresses.0.details.items.3.value.value",
        "Country": "demographic data.contacts.0.addresses.0.details.items.4.value.value",

        "Height": "analytics.1.content.0.data.events.0.data.items.0.value.magnitude",
        "Weight": "analytics.1.content.1.data.events.0.data.items.0.value.magnitude",
        "BMI": "analytics.1.content.2.data.events.0.data.items.0.value.magnitude",
        
        "laboratory test name": "content.0.data.events.0.data.items.0.value.value",
        "laboratory test result":"content.0.data.events.0.data.items.6.items.2.value.magnitude",

        "cardiovascular risk factors": "content.0.data.items.1.items.0.value.value",
        "Clinical desease": "content.0.items.0.data.items.0.value.value",
        "Age": "age.content.0.data.events.0.data.items.0.value.magnitude",
        "Vital status": "vital status.content.0.data.events.0.data.items.0.value.value",
        "Symptoms":"symptoms.content.0.data.events.0.data.items.0.value.value"
    }

    return switcher.get(parameter, "nothing")