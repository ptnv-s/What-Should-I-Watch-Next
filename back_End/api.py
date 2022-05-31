from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from api_1 import get_recommendations_based_on_genres,get_recommendation_content_model
from api_0 import cold_start_check
from api_5 import recommendedMoviesAsperItemSimilarity,movieIdToTitle1
from api_3 import movieIdToTitle3,recommendedMoviesAsperItemSimilarity2
from api_4 import movieIdToTitle2,getRecommendedMoviesAsperUserSimilarity
from api_2 import get_recommendation_content_model2



app = FastAPI()

class request_body1(BaseModel):
	movie_title : str

class request_body2(BaseModel):
	userid : int

@app.get("/api3")
def api1(data : request_body2):
    test_data = [
                data.userid
        ]
    try:
        pred_list = movieIdToTitle3(recommendedMoviesAsperItemSimilarity2(test_data[0]))
        print(pred_list)
        return { 'recommendation' : pred_list}
    except:
        pred_list = cold_start_check(test_data[0])
        pred_list = pred_list['title'].values.tolist()
        pred_list = pred_list[0:10]
        return { 'recommendation' : pred_list}


@app.get("/api4")
def api1(data : request_body2):
    test_data = [
			data.userid
	]
    try:
        pred_list = movieIdToTitle2(getRecommendedMoviesAsperUserSimilarity(test_data[0]))
        return { 'recommendation' : pred_list}
    except:
        pred_list = cold_start_check(test_data[0])
        pred_list = pred_list['title'].values.tolist()
        pred_list = pred_list[0:10]
        return { 'recommendation' : pred_list}

@app.get("/api0")
def api1(data : request_body2):
    test_data = [
			data.userid
	]
    print(test_data)
    pred_list = cold_start_check(test_data[0])

    return { 'recommendation' : pred_list}

@app.get("/api5")
def api1(data : request_body2):
    test_data = [
			data.userid
	]
    try:
        pred_list = movieIdToTitle1(recommendedMoviesAsperItemSimilarity(test_data[0]))
        return { 'recommendation' : pred_list}
    except:
        pred_list = cold_start_check(test_data[0])
        pred_list = pred_list['title'].values.tolist()
        pred_list = pred_list[0:10]
        return { 'recommendation' : pred_list}
@app.get("/api1")
def api1(data : request_body1):
    test_data = [
			data.movie_title
	]
    pred_list = get_recommendations_based_on_genres(test_data[0])
    return { 'recommendation' : pred_list}

@app.get("/api2")
def api2(data : request_body2):
    test_data = [
			data.userid
	]
    try:
        pred_list = get_recommendation_content_model2(test_data[0])
        return { 'recommendation' : pred_list}
    except:
        pred_list = cold_start_check(test_data[0])
        pred_list = pred_list['title'].values.tolist()
        pred_list = pred_list[0:10]
        return { 'recommendation' : pred_list}
        
@app.get("/")
async def root():
    return {"message": "Hello World"}
