import bloock
from bloock.client.integrity import IntegrityClient
from bloock.client.record import RecordClient
from bloock.entity.integrity.network import Network
from datetime import datetime
import json

from encrypt import encrypt_data

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def previous_decision(name,uuid):
        # we set the API key and create a client
        bloock.api_key = os.getenv("API_KEY") 
        record_client = RecordClient()
        integrity_client = IntegrityClient()


        dict_yes={"name": encrypt_data(name),
                "uuid": uuid,
                "decision": encrypt_data("YES")
                }
        json_string_yes = json.dumps(dict_yes)
        record_yes = record_client.from_json(json_string_yes).build()
        records = [record_yes]
        timestamp_yes=0
        try:
                timestamp_yes = integrity_client.verify_records(records)
        except:
                date_yes=0
        
        if timestamp_yes:
                date_yes=datetime.utcfromtimestamp(timestamp_yes)


        dict_no={"name": encrypt_data(name),
                "uuid": uuid,
                "decision": encrypt_data("NO")
                }
        json_string_no = json.dumps(dict_no)
        record_no = record_client.from_json(json_string_no).build()
        records = [record_no]
        timestamp_no=0
        try:
                timestamp_no = integrity_client.verify_records(records)
        except:
                date_no=0
        
        if timestamp_no:
                date_no=datetime.utcfromtimestamp(timestamp_no)

        if date_yes==0 and date_no==0:
                return "no previous decision"
        elif date_yes and date_no==0:
                return "YES"
        elif date_no and date_yes==0:
                return "NO"
        else:
                if date_yes > date_no:
                        return "YES"
                else:
                        return "NO"