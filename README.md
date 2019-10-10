
# gift-recommender

Recommendation engine/service for the gifting app

**Queries:**
To ask for `num` recommendations for a receiver of id `receiver_id` between a price of `min` and `max` having a minimum of `prom` promoted items, make a GET request to: `/recommend/receiver_id/num?min_price=min&max_price=max&min_promoted=prom`

For example to get 5 recommendations (`num = 5`) out of which at least 3 are promoted (`prom = 3`), a receiver of id = 2 and a price between $5.000,01 and $20.000,2 , the path for the GET request is: `/recommend/2/5?min_price=5000.01&max_price=20000.2&min_promoted=3`

**Local Setup:**

Python version: 3.7+

Install dependencies: `pip install -r requirements.txt`

Run server: `flask run`

You will need to specify the following environment variables:

Flask:

* FLASK_APP=recommender_api
* FLASK_ENV
* SECRET_KEY
* APP_SETTINGS

Postgres db:

either

* POSTGRES_URL
* POSTGRES_USER
* POSTGRES_PW
* POSTGRES_DB

and/or

* DATABASE_URL

AWS Bucket:

* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
* AWS_REGION
* BUCKET_NAME
