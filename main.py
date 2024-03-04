from fastapi import FastAPI, Query
import api_functions as af

#instance app
app = FastAPI()

#Endpoint functions

@app.get(path = '/recommendation_user',
          description = """ <font color="blue">
                        INSTRUCTIONS<br>
                        1. Clik on "Try it out".<br>
                        2. Type user_id the box box below.<br>
                        3. Scroll to "Responses".
                        </font>
                        """,
         tags=["General queries"])
def recommendation_user(user_id: str = Query(..., 
                                description="Id of specific User", 
                                example="zombieman182")):
        
    return af.recommendation_user(user_id)