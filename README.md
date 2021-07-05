# docker-selenium-python
Docker base image to run python based scripts for selenium in one container. Compiled on top of base python image build on alpine. This method uses chromium in headless.


# Usage
Build docker-image from scratch. This may take a while, because numpy and pandas must be compiled from source. This is indeed a point, where improvements can begin.

Basic requirements are pandas, numpy and selenium. Simply change your requirements to your needs. 

- Create a python script to trigger selenium based events or crawl the web
- Copy your files to the specified locations
- Run ```docker run -it --rm --shm-size=128m docker-selenium-python:latest python main.py```

Intended usage is for crawling scheduled sites on AWS ECS and Azure ACR. Simply build the container as base and add your scripts to it. Add ```--shm.size=128m``` to it to ensure running correctly. See Docker Run specifications. For some webpages Chrome needs extra memory.

# Example
To run the given example execute the following:

```docker run -it --rm --shm-size=128m docker-selenium-python:alpine python ./examples/main.py```

This example scrapes our homepage and writes the services of our company human readable to console. This can be extended using a MS Teams Channel do be sent to. Documentation can be found [here](https://docker-selenium-python.readthedocs.io/en/latest/).

# Advanced Usage
Triggering your script directly at the start of the container requires you to fiddle with the Dockerfile. Simply add your requirements to a ```requirements.txt``` and copy your source files to the image.

We provide an example script located in examples folder. Use this as a reference guide provided.

```Dockerfile
FROM infologistix/docker-selenium-python:alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY your/app/ ./

CMD "python main.py"
```

Simply build this file to suit your applicational use.

When using Machine learning tools use one of our other selenium based Containers by changing the tag:

- buster
- alpine, latest

For Machine Learning applications we recommend the *buster* tag to install every library there is. Make sure to install only necessary things.

This image was developed for [infologistix GmbH](https://infologistix.de)