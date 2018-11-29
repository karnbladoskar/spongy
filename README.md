# spongy
What mushrooms are really edible? 

## Data

Download the dataset files here:
  * [Training and validation images [13GB]](https://data.deic.dk/shared/2fd47962a38e2a70570f3be027cea57f)
      * Running `md5sum fungi_train_val.tgz` on the tgz file should produce `df2b2980835668ed1d9a0e286e4bdadd`
      * Images have a max dimension of 1024px and have been converted to JPEG format
      * Untaring the images creates a directory structure like `images/category/image.jpg`. This may take a while.

  * [Testing images [1.3GB]](https://data.deic.dk/shared/53f154ca9e9f1e6aee8587f5d18f81fd)
      * Running `md5sum fungi_test.tgz` on the tgz file should produce `949fc7266f7c6574e4ce359cf2571c85`
      * Images have a max dimension of 1024px and have been converted to JPEG format
      * Untaring the images creates a directory structure like `test/image.jpg`. This may take a while.

  * [Training and validation annotations [2.9MB]](https://data.deic.dk/shared/8dc110f312677d2b53003de983b3a26e)
      * Running `md5sum train_val_annotations.tgz` on the tgz file should produce `c3c0f1b8a8d0b60619c43d9c89bdbc7e'
  
  * [Testing image information [92KB]](https://data.deic.dk/shared/c899715d20e2e80063ced63d9cfec9c3)
      * Running `md5sum test_information.tgz` on the tgz file should produce `2f8a8f361e59d27d9ce4c96f4dec3817`
