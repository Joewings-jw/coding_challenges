# Memcached Server

A simple Memcached server implementation using asyncio in Python.

## Overview

The server listens for incoming connections from clients and handles various Memcached commands, including SET, GET, ADD, REPLACE, APPEND, PREPEND, CAS (compare-and-swap), INCREMENT, and DECREMENT.

## Supported Commands

- **SET**: Store data in the cache.
- **GET**: Retrieve data from the cache.
- **ADD**: Store data only if the key does not already exist.
- **REPLACE**: Store data only if the key already exists.
- **APPEND**: Append data to an existing key's value.
- **PREPEND**: Prepend data to an existing key's value.
- **CAS**: Compare and swap data based on a unique identifier.
- **INC**: Increment the value of a numeric key.
- **DEC**: Decrement the value of a numeric key.

## Usage

The server can be started with the specified port number and maximum cache size (optional).

### Example

```bash
python memcached_server.py -p 11211 -s 10000
```

### Arguments

- **-p, --port**: Port number to run the server on (default: 11211).
- **-s, --max-cache-size**: Maximum cache size in bytes (default: unlimited).

## Telnet Commands and Responses

### SET

```plaintext
# Command Format
SET <key> <flags> <exptime> <byte count> [noreply]
<data block>

# Example Command
SET new_key 0 3600 4
data

# Response
STORED [unique_id]
```

### ADD

```plaintext
# Command Format
ADD <key> <flags> <exptime> <byte count> [noreply]
<data block>

# Example Command
ADD new_key 0 3600 4
data


# Response
NOT_STORED
```

### REPLACE

```plaintext
# Command Format
REPLACE <key> <flags> <exptime> <byte count> [noreply]
<data block>

# Example Command
REPLACE existing_key 0 3600 4
data


# Response
STORED [unique_id]
```

### CAS

```plaintext
# Command Format
cas <key> <flags> <exptime> <byte count> [noreply]
<data block>

# Example Command
cas new_key 0 3600 4 [unique_id]

# Response
STORED
```

### APPEND

```plaintext
# Command Format
APPEND <key> <flags> <exptime> <byte count> [noreply]
<data block>

# Example Command
APPEND existing_key 0 3600 4
data


# Response
STORED
```

### PREPEND

```plaintext
# Command Format
PREPEND <key> <flags> <exptime> <byte count> [noreply]
<data block>

# Example Command
PREPEND existing_key 0 3600 4
data


# Response
STORED
```