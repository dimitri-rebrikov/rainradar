# setup
Theoretically you don't need your own backend as the frontend device will use my instance of the backend by default.

But for the case you want to have and use your own instance, here is the short description:
(to do this you need to have basic knowledge about Amazon Web Services)

- create 3 AWS Lambdas using the zipped content of the rainradar_* directories. For the rainradar_rv_update lambda you will also need to create a python layer, see the chapter below.
- configure the S3 bucket with the name "rainradar" and configure the read/write access to it for all 3 lambdas
- test all 3 lambdas
- create Event Bridge with 1 hour rate for the rainradar_mosmix_update lambda
- create Event Bridge with 2-5 min rate for the rainradar_rv_update lambda
- create API Gateway for the rainradar_get lambda. For the API Gateway you may also want to create throttling to prevent unexpected costs if someone runs a request attack to your endpoint
- the current frontend source code contains the hardcoded URL of my API Gateway so you need to adjust it to use you own

## rainradaf_rv_update python layer
The rainradar_rv_update lambda uses functions depending on the h5py python library. 
This library not only not included into the standard python distribution available on the AWS but also has hardware dependent part. So you need to create a layer for this

Commands to create the layer zip on your local machine:
- install the same python version you will use for the lambdas in AWS
- `mkdir python`
- `pip install h5py --platform manylinux2014_x86_64 --only-binary=:all: -t python`
- `zip -r layer.zip python/` (if you don't have zip command, just use the zipper of your choice, but pay attention that the 'python' directory is preserved inside of the the zip)

Then you just need to create a new layer in your AWS environment and upload the 'layer.zip' as its content.

Later during the creation of the rainradar_rv_update lambda you shall configure it to use this layer.


