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

class gcode_packager {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.x_percentage = null;
      this.y_percentage = null;
    }
    else {
      if (initObj.hasOwnProperty('x_percentage')) {
        this.x_percentage = initObj.x_percentage
      }
      else {
        this.x_percentage = 0.0;
      }
      if (initObj.hasOwnProperty('y_percentage')) {
        this.y_percentage = initObj.y_percentage
      }
      else {
        this.y_percentage = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type gcode_packager
    // Serialize message field [x_percentage]
    bufferOffset = _serializer.float32(obj.x_percentage, buffer, bufferOffset);
    // Serialize message field [y_percentage]
    bufferOffset = _serializer.float32(obj.y_percentage, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type gcode_packager
    let len;
    let data = new gcode_packager(null);
    // Deserialize message field [x_percentage]
    data.x_percentage = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [y_percentage]
    data.y_percentage = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'soft_robot_learning/gcode_packager';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '04ac0e9112339add0ccbc4911b02d6de';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 x_percentage
    float32 y_percentage
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new gcode_packager(null);
    if (msg.x_percentage !== undefined) {
      resolved.x_percentage = msg.x_percentage;
    }
    else {
      resolved.x_percentage = 0.0
    }

    if (msg.y_percentage !== undefined) {
      resolved.y_percentage = msg.y_percentage;
    }
    else {
      resolved.y_percentage = 0.0
    }

    return resolved;
    }
};

module.exports = gcode_packager;
