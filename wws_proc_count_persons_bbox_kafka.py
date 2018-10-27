from wws_wrap import StreamOperator, wws_start
import json
from kafka import KafkaProducer

class PeopleCountingOperator(StreamOperator):

    block_type = 'pywrap_count_people'
    input_ports = [('in', str)]
    output_ports = [('out', str)]

    def __init__(self, inputs, outputs, 
                 camera: str='unknown', # identifier of video stream source
                 brokers: str='localhost:9092', # Kafka bootstrap_servers
                 topic: str='wws', # Kafka topic 
                 confidence: float=0.7, **kwargs):
        StreamOperator.__init__(self, inputs, outputs)
        self._camera = camera  # A name assigned to the processor
        self._confidence = max(0.0, min(confidence, 1.0))
        self._topic = topic # Kafka topic
        try:
            self._producer = KafkaProducer(bootstrap_servers = brokers, 
                                           value_serializer = lambda v: json.dumps(v).encode('utf-8'))
        except:
            pass

    def process(self, data, key=None):
        output_dict = { "camera" : self._camera, "count_person" : 0, "bbox": [] }
        # will set input type hints to JSON directly
        data_double_quotes = data.replace("\'", "\"") #JSON strings must use double quotes
        data_dict = json.loads(data_double_quotes)
        if "payload" in data_dict:
            if "objects" in data_dict["payload"]:
                if "detections" in data_dict["payload"]["objects"]:
                   detect_obj_list = data_dict["payload"]["objects"]["detections"]
                   for detect_obj in detect_obj_list:
                       if "class" in detect_obj:
                           if detect_obj["class"]["name"] == "person":
                             if detect_obj["confidence"] >= self._confidence:
                                 output_dict["count_person"] += 1
                                 output_dict["bbox"].append(detect_obj["bbox"])
        if hasattr(self, '_producer'):
            self._producer.send(self._topic, output_dict)
        yield 'out', output_dict

if __name__ == '__main__':
    wws_start()
