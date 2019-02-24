# Automated-Traffic-Control
Project on controlling traffic signals dynamically using DIP and ML concept

## traffic-capacity-counting:

### Data
Go to https://en.savefrom.net/ and download video in 720p quality with url https://youtu.be/wqctLW0Hb_0

### How to run script
> Install [Anaconda3 Distribution](https://www.anaconda.com/distribution/) on your machine. 
> If already installed, then install the required dependencies by running the following set of commands.
```
conda install <package_name>
```

Edit **traffic_capacity.py** if needed:
```
IMAGE_DIR = "./out"
VIDEO_SOURCE = "./input.mp4"
SHAPE = (720, 1280)  # HxW
AREA_PTS = np.array([[780, 716], [686, 373], [883, 383], [1280, 636], [1280, 720]]) 

...

pipeline = PipelineRunner(pipeline=[
    CapacityCounter(area_mask=area_mask, image_dir=IMAGE_DIR),
    ContextCsvWriter('./report.csv',start_time=1505494325, fps=1, faster=10, field_names=['capacity']) # saving every 10 seconds
], log_level=logging.DEBUG)
```
Run script:
```
python traffic.py
```
