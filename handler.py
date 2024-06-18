import time
from collections import defaultdict
from threading import Event
import importlib

# Load the module for decoding messages if provided
decode_module = None
try:
    decode_module = importlib.import_module("mbot_lcm_msgs")
except ImportError:
    print(f"Error: Could not import module mbot_lcm_msgs")
    decode_module = None

# Data structures to hold message counts, timestamps, and LCM types
message_counts = defaultdict(int)
message_times = defaultdict(list)
channel_types = {}
stop_event = Event()
decoded_message_dict = defaultdict(list)

def message_handler(channel, data):
    global message_counts, message_times, channel_types, decoded_message_dict
    
    lcm_type = "Unknown"
    decoded_message = None
    if decode_module:
        try:
            # Attempt to decode the message to find its type
            for attr in dir(decode_module):
                lcm_type_class = getattr(decode_module, attr)
                if isinstance(lcm_type_class, type) and hasattr(lcm_type_class, 'decode'):
                    try:
                        lcm_type = lcm_type_class.__name__
                        decoded_message = lcm_type_class.decode(data)
                        break
                    except Exception:
                        continue
        except Exception as e:
            lcm_type = f"Error: {e}"

    # Store the decoded message fields if the channel matches any of the specified channels
    if decoded_message:
        decoded_message_dict[channel] = decode_fields(decoded_message)

    # Update message counts and times
    message_counts[channel] += 1
    message_times[channel].append(time.time())
    channel_types[channel] = lcm_type

# Helper function to recursively decode nested messages
def decode_fields(decoded_msg):
    fields = []
    for field in decoded_msg.__slots__:
        value = getattr(decoded_msg, field)
        # Check if the value is a list or tuple of nested objects
        if isinstance(value, (list, tuple)):
            nested_values = []
            for item in value:
                if hasattr(item, '__slots__'):
                    nested_values.append(decode_fields(item))
                else:
                    nested_values.append(truncate_array(item))
            fields.append((field, nested_values))
        elif hasattr(value, '__slots__'):
            # Recursively decode nested objects
            fields.append((field, decode_fields(value)))
        else:
            fields.append((field, truncate_array(value)))
    return fields

# Helper function to truncate long lists
def truncate_array(value):
    try:
        # checks if the value is array-like and if its length > 10
        if hasattr(value, '__len__') and len(value) > 10:
            return tuple(value[:10]) + ("...",)
    except TypeError:
        pass
    # otherwise return the original value
    return value

def get_status():
    status = []
    for channel, times in message_times.items():
        current_time = time.time()
        times = [t for t in times if current_time - t < 1]
        message_times[channel] = times
        rate = len(times) / 1.0
        total_messages = message_counts[channel]
        lcm_type = channel_types.get(channel, "Unknown")
        channel_status = {
            "channel": channel,
            "type": lcm_type,
            "rate": rate,
            "total_messages": total_messages
        }
        status.append(channel_status)

    decoded_status = []
    for channel, decoded_message in decoded_message_dict.items():
        decoded_status.append({
            "channel": channel,
            "decoded_message": format_decoded_message(decoded_message)
        })

    return {"status": status, "decoded_status": decoded_status}

def format_decoded_message(msg, indent=0):
    formatted_message = []
    # (key, value)
    if isinstance(msg, tuple) and len(msg) == 2 and not hasattr(msg[1], '__len__'):
        key, value = msg
        formatted_message.append(f"{' ' * indent}{key}: {str(value)}")
    # (key, [value1, value2, value3])
    elif isinstance(msg, tuple) and len(msg) == 2 and not hasattr(msg[1][0], '__len__'):
        key, value = msg
        formatted_message.append(f"{' ' * indent}{key}: {str(value)}")
    # all other cases
    else:
        for item in msg:
            if isinstance(item, tuple) and len(item) == 2:
                key, value = item
                if not hasattr(value, '__len__') or not hasattr(value[0], '__len__'):
                    formatted_message.append(f"{' ' * indent}{key}: {str(value)}")
                else:
                    formatted_message.append(f"{' ' * indent}{key}:")
                    for v in value:
                        formatted_message.extend(format_decoded_message(v, indent + 2))
    return formatted_message
