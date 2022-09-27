# setup
Theoretically you don't need your own backend as the frontend device will use my instance of the backend by default.

But for the case you want to have and use your own instance, here is the short description:
(to do this you need to have basic knowledge about Amazon Web Services)

- create 3 AWS Lambdas using the content of the rainradar_* directories
- configure the S3 bucket with the name "rainradar" and configure the read/write access to it for all 3 lambdas
- test all 3 lambdas
- create Event Bridge with 1 hour rate for the rainradar_mosmix_update lambda
- create Event Bridge with 2-5 min rate for the rainradar_rv_update lambda
- create API Gateway for the rainradar_get lambda
- the current frontend source code contains the hardcoded URL of my API Gateway so you need to adjust it to use you own


