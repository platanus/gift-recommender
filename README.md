# gift-recommender
Recommendation engine/service for the gifting app

**Basic query:**
To ask for `num` recommendations for user described by:
```{
    'likes': [a],
    'dislikes': [b],
  }```
make a GET request to: `/recommend/num?likes=a&dislikes=b`

For example with `num = 4`, and a user described by:
```{
  'likes': [1, 2],
  'dislikes': [3, 4],
}```
the path for the GET request is: `/recommend/4?likes=1&likes=2&dislikes=3&dislike=4`