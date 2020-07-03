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

class apriltag_data {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.x_pos_gnd = null;
      this.y_pos_gnd = null;
    }
    else {
      if (initObj.hasOwnProperty('x_pos_gnd')) {
        this.x_pos_gnd = initObj.x_pos_gnd
      }
      else {
        this.x_pos_gnd = 0.0;
      }
      if (initObj.hasOwnProperty('y_pos_gnd')) {
        this.y_pos_gnd = initObj.y_pos_gnd
      }
      else {
        this.y_pos_gnd = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type apriltag_data
    // Serialize message field [x_pos_gnd]
    bufferOffset = _serializer.float32(obj.x_pos_gnd, buffer, bufferOffset);
    // Serialize message field [y_pos_gnd]
    bufferOffset = _serializer.float32(obj.y_pos_gnd, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type apriltag_data
    let len;
    let data = new apriltag_data(null);
    // Deserialize message field [x_pos_gnd]
    data.x_pos_gnd = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [y_pos_gnd]
    data.y_pos_gnd = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'soft_robot_learning/apriltag_data';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '7eb6b532fc62c3db52dc0849aeb59aea';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 x_pos_gnd
    float32 y_pos_gnd
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new apriltag_data(null);
    if (msg.x_pos_gnd !== undefined) {
      resolved.x_pos_gnd = msg.x_pos_gnd;
    }
    else {
      resolved.x_pos_gnd = 0.0
    }

    if (msg.y_pos_gnd !== undefined) {
      resolved.y_pos_gnd = msg.y_pos_gnd;
    }
    else {
      resolved.y_pos_gnd = 0.0
    }

    return resolved;
    }
};

module.exports = apriltag_data;
