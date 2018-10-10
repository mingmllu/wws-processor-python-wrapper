import { ExternalOperator, Stream, InputPort, declare_external_op } from "@xstream/core"
interface ConversationTranscript extends ExternalOperator<string> {
  person1: InputPort<string>;
  $person1: InputPort<string>;
  person2: InputPort<string>;
  $person2: InputPort<string>;
  transcript: Stream<string>;
  $transcript: Stream<string>;
  count1: Stream<number>;
  $count1: Stream<number>;
  count2: Stream<number>;
  $count2: Stream<number>;
}

function transcribe(params: {
  name1: string,
  name2: string
}): ConversationTranscript {
let spec = {
    "blockType": "Transcript",
    "functionName": "transcribe",
    "version": "1.0.0",
    "paramsSpec": {
        "name1": {
            "default": null
        },
        "name2": {
            "default": null
        }
    },
    "inputSpec": {
        "person1": {
            "default": true
        },
        "person2": {
            "default": false
        }
    },
    "outputSpec": {
        "transcript": {
            "default": true
        },
        "count1": {
            "default": false
        },
        "count2": {
            "default": false
        }
    },
    "meta": {
        "processor": "wws/pywrap"
    }
  }
  return declare_external_op<string, ConversationTranscript>(spec)(params)
}

import { source } from "@xstream/core"
let source1 = source<string>({amqp: {topic: 'person.one'}});
let source2 = source<string>({amqp: {topic: 'person.two'}});

let tran = transcribe({name1: 'Nero', name2: 'Bart'});

source1.pipe(tran.person1);
source2.pipe(tran.person2);

tran.transcript.sink('transcript');

tran.count1.sink('count1');
tran.count2.sink('count2');