// Auto-generated. Do not edit!

// (in-package soft_robot_learning.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class sensor_processing {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.xSensor = null;
      this.ySensor = null;
    }
    else {
      if (initObj.hasOwnProperty('xSensor')) {
        this.xSensor = initObj.xSensor
      }
      else {
        this.xSensor = 0.0;
      }
      if (initObj.hasOwnProperty('ySensor')) {
        this.ySensor = initObj.ySensor
      }
      else {
        this.ySensor = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type sensor_processing
    // Serialize message field [xSensor]
    bufferOffset = _serializer.float32(obj.xSensor, buffer, bufferOffset);
    // Serialize message field [ySensor]
    bufferOffset = _serializer.float32(obj.ySensor, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type sensor_processing
    let len;
    let data = new sensor_processing(null);
    // Deserialize message field [xSensor]
    data.xSensor = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [ySensor]
    data.ySensor = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'soft_robot_learning/sensor_processing';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '85a7f1f6ce3d01e7b0a20f37a29b8607';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    #This is a custom message template for the state of the robot
    #Modify it with the amount of sensors you have to put into your RL 
    #algorithm
    
    float32 xSensor
    float32 ySensor
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new sensor_processing(null);
    if (msg.xSensor !== undefined) {
      resolved.xSensor = msg.xSensor;
    }
    else {
      resolved.xSensor = 0.0
    }

    if (msg.ySensor !== undefined) {
      resolved.ySensor = msg.ySensor;
    }
    else {
      resolved.ySensor = 0.0
    }

    return resolved;
    }
};

module.exports = sensor_processing;
