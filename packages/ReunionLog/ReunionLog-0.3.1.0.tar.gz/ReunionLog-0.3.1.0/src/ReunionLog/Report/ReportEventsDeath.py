import requests
from enum import Enum;
import json
import ReunionLog as RL
from graphql_query import Argument, Directive, Field, Operation, Query, Variable




"""class Difficulty(Enum):
    LFR = 1,
    NORMAL = 3,
    HC = 4,
    MYTHIC = 5"""
#Difficulty.Diff.value gives the value of the diff


# https://denisart.github.io/graphql-query/usage.html#arguments
episode = Variable(name="code", type="String")
event = Variable(name="Deaths", type="Deaths")
eTime = Variable(name="eTime", type="Float")
diff = Variable(name="Diff", type = "Int")
enID = Variable(name="eID", type = "Int")

arg_episode = [Argument(name="code", value=episode)]
arg_event = [Argument(name="dataType", value="Deaths"), Argument(name = "difficulty", value=Variable(name="Diff", type = "Int")), Argument(name = "encounterID", value = Variable(name="eID", type="Int")), Argument(name="endTime", value=Variable(name="eTime", type="String")), Argument(name = "wipeCutoff", value=3), Argument(name="useAbilityIDs", value="false")]

queryDeath = Query(
    name="reportData",
    fields=[
        Field(
            name="report",
            arguments=arg_episode,
            fields=[
                Field(
                    name="events",
                    arguments=arg_event,
                    fields=["data"]
                )
            ]
        )
    ]
)
operation = Operation(
    type="query",
    variables=[episode, eTime, diff, enID],
    queries=[queryDeath]
)


"""Gets the data 'events' from GraphQL api. Require response, auth-url and event string"""
def Get_Data_EventDeath(response, publicURL, diff, **kwargs):
    #difficultyVal = diff.value
    """match diff:
        case Difficulty.LFR.value:
            break;
        case Difficulty.NORMAL.value:
            break;
        case Difficulty.HC.value:
            break;
        case Difficulty.MYTHIC.value:
            break;
        case _:
            break;"""

    if kwargs == {}:
        print("---Assuming default kwargs---");
        kwargs = {'code' : "fj6Pp7TVkaW2KXzB", 'eTime':999999999999}
    print(kwargs)

    data = {"query": operation.render(), "variables": kwargs}
    with requests.Session() as session:
        session.headers = response
        response = session.get(publicURL, json= data)
    return response.json()

