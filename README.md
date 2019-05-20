# training-data-api

API to upload and manage training data

## uploadImageToBlob

This should allow you to upload an image to a particular container with metadata

For each Seal, there should be a number of containers for the different image types and usages. For seal `LF1` for example; we should have the following containers:

LF1-TRAINING-ORIGINAL
LF1-TRAINING-PROCESSED
LF1-TRAINING-TEST

LF1-USER-UNVERIFIED
LF1-USER-VERIFIED

## Batch uploading content for AI classifier training

For training purposes, it is expected a Zip file of images are uploaded for a seal; the originals will be stored in the `LF1-TRAINING-ORIGINAL` container. These will then be run through the processor to crop and convert them into a standard image format to be run against the AI classifier.

Once these have all been processed, 10% should be moved from the `LF1-TRAINING-PROCESSED` container into the `LF1-TRAINING-TEST` container; or a mechanism provided for a user to pick which should be `kept behind` for testing the model outcome

## User uploading to see what seal they've seen

When a user uploads an image of a seal to find out who it is, their image(s) should be put into the appropriately named unverified container, i.e. `{SEALID}-USER-UNVERIFIED` so that they can be verified by a CSG rep.

If the image is not able to be match successfully it should be put in the `USER-UNKNOWN` container for manual checking.
