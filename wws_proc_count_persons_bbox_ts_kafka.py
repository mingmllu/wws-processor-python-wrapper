from wws_wrap import StreamOperator, wws_start
import json
from typing import Any
from kafka import KafkaProducer

class PeopleCountingOperator(StreamOperator):

    block_type = 'pywrap_count_people'
    input_ports = [('in', Any)]
    output_ports = [('out', Any)]

    def __init__(self, inputs, outputs, 
                 camera: str='unknown', # identifier of video stream source
                 brokers: str='localhost:9092', # Kafka bootstrap_servers
                 topic: str='wws', # Kafka topic 
                 confidence: float=0.7, **kwargs):
        StreamOperator.__init__(self, inputs, outputs)
        self._camera = camera  # A name assigned to the processor
        self._confidence = max(0.0, min(confidence, 1.0))
        self._topic = topic # Kafka topic
        self._last_sent_time = 0 # the time when the last message is sent
        try:
            self._producer = KafkaProducer(bootstrap_servers = brokers, 
                                           value_serializer = lambda v: json.dumps(v).encode('utf-8'))
        except:
            pass

    def process(self, data, key=None):
        output_dict = { "camera" : self._camera, "count_person" : 0, "bbox": [], "ts2kafka" : 0, "detect_ts" : 0 }
        data_dict = data # data already a JSON object
        if "payload" in data_dict:
            if "detections" in data_dict["payload"]:
                if "detections" in data_dict["payload"]["detections"]:
                   detect_obj_list = data_dict["payload"]["detections"]["detections"]
                   for detect_obj in detect_obj_list:
                       if "class" in detect_obj:
                           if detect_obj["class"]["name"] == "person":
                             if detect_obj["confidence"] >= self._confidence:
                                 output_dict["count_person"] += 1
                                 output_dict["bbox"].append(detect_obj["bbox"])
                                 output_dict["ts2kafka"] = time.time()
                                 output_dict["detect_ts"] = data_dict["ts"]
        if hasattr(self, '_producer'):
            self._producer.send(self._topic, output_dict)
            if time.time() - self._last_sent_time >= 0.25:
                output_dict.pop("bbox")
                self._producer.send(self._topic + "_sti", output_dict)
                self._producer.send("aggregate_sti", output_dict)  # send the message under a general topic
                self._last_sent_time = time.time()
        yield 'out', output_dict

if __name__ == '__main__':
    wws_start()
