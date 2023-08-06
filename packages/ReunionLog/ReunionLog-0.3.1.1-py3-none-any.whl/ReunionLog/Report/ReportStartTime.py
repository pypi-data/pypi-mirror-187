import requests
import json

queryStart = """query($code:String){
                    reportData{
                        report(code:$code){
                            startTime
                        }
                    }
                }"""

def Get_Data_StartTime(response, publicURL, **kwargs):
    #print(new_queryDeath)
    #print(f"event_field: \n{event_field}\n")
    #print(f"event_field: \n{reportData_field}\n")
    #print(f"event_field: \n{new_queryDeath}\n")
    data = {"query": queryStart, "variables": kwargs}
    with requests.Session() as session:
        session.headers = response
        response = session.get(publicURL, json= data)
    return response.json()