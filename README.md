
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

* `FLASK_APP=recommender_api`
* `FLASK_ENV`
* `SECRET_KEY`
* `APP_SETTINGS`

Postgres db:

either

* `POSTGRES_URL`
* `POSTGRES_USER`
* `POSTGRES_PW`
* `POSTGRES_DB`

and/or

* `DATABASE_URL`

AWS Bucket:

* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`
* `AWS_REGION`
* `BUCKET_NAME`

AWS Bucket (Rails app)

* `AWS_RAILS_ACCESS_KEY_ID`
* `AWS_RAILS_SECRET_ACCESS_KEY`
* `AWS_RAILS_REGION`
* `RAILS_BUCKET_NAME`

**Parts and pieces & How to upgrade:**

The main components in the system are:

**image feature extractor**:
Creates a vector of features from the given image. It has two models internally, the *feature extractor neural net* (FENN), which produces a higher dimensional representation and the *autoencoder* which takes that representation and compresses it to a lower dimensionality. The feature extractor currently is an EfficientNetB0 trained with ImageNet. The Autoencoder is a simple implementation of a variational autoencoder trained with Depto51 products.

How to further train the autoencode:

To generate a new version of the autoencoder weights you can run the `img_vae_train.py` script for which you will need a csv (`img_vectors.csv`) containing the features. 

A standard procedure could be:
1. Compute the features from the images of all products using the FENN
2. Save them in a file named `img_vectors.csv` where each row corresponds to the features of a single image
3. Run the `img_vae_train.py` script
4. Upload the new weights to the corresponding S3 bucket

**text feature extractor**:
Creates a vector of features from the given text. It is used in `preprocessor.py` to compute a feature vector from the product name. The models uses word2vec embeddings trained with text in spanish. To update the weights simply upload the new weights to S3 and update the `embeddings` variable in `preprocessor.py` (or simply upload them with the name `embeddings-xs-model.vec`).