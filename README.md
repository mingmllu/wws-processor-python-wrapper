# wws-processor-python-wrapper

WWS processor implemented in Python for passing object detection JSON results to a separate platform.

## Install wws_wrap package
### Requirements
1. Bring up all WWS docker containers by running the shell script "launch.sh":
```
/video-analytics-0.5.1$./launch.sh start
```
2. Must use Python 3.5 or later

First create a virtual environment. Then run the following command:
```
$pip install ext/pywrap_processor
```
## Use the python-wrapper processor "obj_detect_person_count_kafka.ts"

First step: launch the Python script "wws_proc_count_persons_kafka.py" by running it from the command line:
```
$ python wws_proc_count_persons_kafka.py
```
You will see the following information displayed on the screen:
```
INFO:wws_wrap:main args: {}
DEBUG:asyncio:Using selector: EpollSelector
INFO:aioamqp.protocol:Recv open ok
DEBUG:aioamqp.channel:Channel is open
DEBUG:aioamqp.channel:Queue declared
DEBUG:aioamqp.channel:Queue bound
DEBUG:aioamqp.channel:Queue bound
INFO:wws_wrap.rpc_server:Awaiting RPC requests
```
Second step: use webpack to compile the TypeScript file "obj_detect_person_count_kafka.ts" and generate a JavaScript file, say "bundle.js". 

Third step: use WWS-CLI to launch the processor:
```
$ wws run bundle.js
```
*Alternatively* if WWS-CLI is not available in the second step and third step, you can take advantage of WWS sandbox to run the processor. To do this, you can open the file "obj_detect_person_count_kafka.ts", copy the entire code and paste it to the sandbox. Hit the button Dashboard button "RUN" to start.