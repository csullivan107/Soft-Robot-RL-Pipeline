// Generated by gencpp from file soft_robot_learning/gcode_packager.msg
// DO NOT EDIT!


#ifndef SOFT_ROBOT_LEARNING_MESSAGE_GCODE_PACKAGER_H
#define SOFT_ROBOT_LEARNING_MESSAGE_GCODE_PACKAGER_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace soft_robot_learning
{
template <class ContainerAllocator>
struct gcode_packager_
{
  typedef gcode_packager_<ContainerAllocator> Type;

  gcode_packager_()
    : x_percentage(0.0)
    , y_percentage(0.0)  {
    }
  gcode_packager_(const ContainerAllocator& _alloc)
    : x_percentage(0.0)
    , y_percentage(0.0)  {
  (void)_alloc;
    }



   typedef float _x_percentage_type;
  _x_percentage_type x_percentage;

   typedef float _y_percentage_type;
  _y_percentage_type y_percentage;





  typedef boost::shared_ptr< ::soft_robot_learning::gcode_packager_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::soft_robot_learning::gcode_packager_<ContainerAllocator> const> ConstPtr;

}; // struct gcode_packager_

typedef ::soft_robot_learning::gcode_packager_<std::allocator<void> > gcode_packager;

typedef boost::shared_ptr< ::soft_robot_learning::gcode_packager > gcode_packagerPtr;
typedef boost::shared_ptr< ::soft_robot_learning::gcode_packager const> gcode_packagerConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::soft_robot_learning::gcode_packager_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::soft_robot_learning::gcode_packager_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::soft_robot_learning::gcode_packager_<ContainerAllocator1> & lhs, const ::soft_robot_learning::gcode_packager_<ContainerAllocator2> & rhs)
{
  return lhs.x_percentage == rhs.x_percentage &&
    lhs.y_percentage == rhs.y_percentage;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::soft_robot_learning::gcode_packager_<ContainerAllocator1> & lhs, const ::soft_robot_learning::gcode_packager_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace soft_robot_learning

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::soft_robot_learning::gcode_packager_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::soft_robot_learning::gcode_packager_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::soft_robot_learning::gcode_packager_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::soft_robot_learning::gcode_packager_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::soft_robot_learning::gcode_packager_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::soft_robot_learning::gcode_packager_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::soft_robot_learning::gcode_packager_<ContainerAllocator> >
{
  static const char* value()
  {
    return "04ac0e9112339add0ccbc4911b02d6de";
  }

  static const char* value(const ::soft_robot_learning::gcode_packager_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x04ac0e9112339addULL;
  static const uint64_t static_value2 = 0x0ccbc4911b02d6deULL;
};

template<class ContainerAllocator>
struct DataType< ::soft_robot_learning::gcode_packager_<ContainerAllocator> >
{
  static const char* value()
  {
    return "soft_robot_learning/gcode_packager";
  }

  static const char* value(const ::soft_robot_learning::gcode_packager_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::soft_robot_learning::gcode_packager_<ContainerAllocator> >
{
  static const char* value()
  {
    return "float32 x_percentage\n"
"float32 y_percentage\n"
;
  }

  static const char* value(const ::soft_robot_learning::gcode_packager_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::soft_robot_learning::gcode_packager_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.x_percentage);
      stream.next(m.y_percentage);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct gcode_packager_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::soft_robot_learning::gcode_packager_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::soft_robot_learning::gcode_packager_<ContainerAllocator>& v)
  {
    s << indent << "x_percentage: ";
    Printer<float>::stream(s, indent + "  ", v.x_percentage);
    s << indent << "y_percentage: ";
    Printer<float>::stream(s, indent + "  ", v.y_percentage);
  }
};

} // namespace message_operations
} // namespace ros

#endif // SOFT_ROBOT_LEARNING_MESSAGE_GCODE_PACKAGER_H