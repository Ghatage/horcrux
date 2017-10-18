![header](https://user-images.githubusercontent.com/3139649/31358032-a42ab7fc-ad09-11e7-973d-d0b5b0981763.png)

'The Dropbox for IPFS' //  'Hide in plain sight'

##### Why do I need **horcrux**?
horcrux is a client which can hopefully resolve some of the drawbacks IPFS has.

* Data on IPFS is permanent! So you better be careful of what you put on there
* Your data is on someone else's computer, how do you secure it?
* IPFS can get slow and if you're uploading a huge file, it might take a while
* A teeny tiny change to a huge file? You'll have to upload the entire file again!

##### What does horcrux do?
* horcrux uses `deduplication` to find similar patterns in a file and breaks down the file into those chunks.
* It then encrypts those chunks and pushes them to IPFS 
* It keeps track of which encrypted chunk belongs to which file. 
* It can then recreate the file based on this info.

In this way: 
* Only chunks with updates will be pushed to IPFS, saving time and bandwidth
* Everything that's pushed is encrypted

Visual representation
![working](https://user-images.githubusercontent.com/3139649/31358031-a428b81c-ad09-11e7-8f4c-4cd973b02391.png)


##### This project is currently under development!
TODO:
- Finish reconstructing file from downloaded and decrypted block files
- Clean up downloaded blk and enc files
- Find a more elegant way to generate and download blk and enc files without changing pyrabin
- Introduce a config file which can have the encryption password and other details
- Reintroduce UI and hook it up with the horcrux via Flask


##### Dependencies and credits
horcrux is written in such a way that all the dependencies it uses can be swapped out easily. However the prototype was made with the help of these fine repos:

- python3
- ipfsapi (https://ipfs.io/docs/getting-started/)
- simple-crypt (https://github.com/andrewcooke/simple-crypt/)
- pyrabin (https://github.com/aitjcize/pyrabin)
- DragAndDrop UI (https://github.com/pcote/DragDropProject)
