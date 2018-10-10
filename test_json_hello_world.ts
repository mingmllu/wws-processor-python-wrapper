import { ExternalOperator, Stream, InputPort, declare_external_op } from "@xstream/core"

interface JsonHelloWorldOperator extends ExternalOperator<string> {
  in: InputPort<number>;
  $in: InputPort<number>;
  out: Stream<string>;
  $out: Stream<string>;
}

function pywrap_json_hello_world(params: {

}): JsonHelloWorldOperator {
  let spec = {
    "blockType": "pywrap_json_hello_world",
    "functionName": "pywrap_json_hello_world",
    "version": "0.0.1",
    "paramsSpec": {},
    "inputSpec": {
        "in": {
            "default": true
        }
    },
    "outputSpec": {
        "out": {
            "default": true
        }
    },
    "meta": {
        "processor": "wws/pywrap"
    }
  }
  return declare_external_op<string, JsonHelloWorldOperator>(spec)(params)
}


import { source } from "@xstream/core"
source("test/pywrap/input")
.pipe(pywrap_json_hello_world({}))
.sink("test/pywrap/output")

