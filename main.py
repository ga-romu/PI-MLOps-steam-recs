from fastapi import FastAPI, Query
import api_functions as af

#instance app
app = FastAPI()

#Endpoint functions

@app.get(path = '/developer',
          description = """ <font color="blue">
                        INSTRUCTIONS<br>
                        1. Clik on "Try it out".<br>
                        2. Type user_id the box box below.<br>
                        3. Scroll to "Responses".
                        </font>
                        """,
         tags=["General queries"])
def developer(developer: str = Query(..., 
                                description="Name of Developer", 
                                example="Valve")):
        
    return af.developer(developer)

@app.get(path = '/userdata',
          description = """ <font color="blue">
                        INSTRUCTIONS<br>
                        1. Clik on "Try it out".<br>
                        2. Type user_id the box box below.<br>
                        3. Scroll to "Responses".
                        </font>
                        """,
         tags=["General queries"])
def userdata(user_id: str = Query(..., 
                                description='Id of a specific User', 
                                example="Derp-e")):
        
    return af.userdata(user_id)