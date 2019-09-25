# gift-recommender
Recommendation engine/service for the gifting app

**Queries:**
To ask for `num` recommendations for a receiver of id `receiver_id` make a GET request to: `/recommend/receiver_id/num`

For example with `num = 5`, and a receiver of id = 2, the path for the GET request is: `/recommend/2/5`

To ask for `num` default recommendations (not associated to the preferences of a receiver) make a GET request to: `/recommend/num`

For example, with `num = 2` the path for the GET request is: `/recommend/2`

**Local Setup:**

Python version: 3.7+

Install dependencies: `pip install -r requirements.txt`

Run server: `flask run`

You will need to specify the following environment variables:

Flask:
```
FLASK_APP=recommender_api
FLASK_ENV
SECRET_KEY
APP_SETTINGS
```
Postgres db:

either
```
POSTGRES_URL
POSTGRES_USER
POSTGRES_PW
POSTGRES_DB
```
and/or
```
export DATABASE_URL
```
AWS Bucket:
```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
BUCKET_NAME
```
