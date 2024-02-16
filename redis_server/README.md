## Build Your Own Redis Server

Redis is an open-source, in-memory data structure store used as a database, cache, and message broker. It supports various data structures such as strings, hashes, lists, sets, sorted sets with range queries, bitmaps, hyperloglogs, geospatial indexes with radius queries, and streams. This challenge involves building your own Redis server, which will offer similar functionalities as the original Redis.

### Key Features of Redis:

- **In-Memory Data Store:** Redis primarily stores data in memory, making it extremely fast for data retrieval and storage operations.

- **Data Structures:** Redis supports a wide range of data structures, allowing for versatile data storage and manipulation.

- **Persistence:** Redis offers options for data persistence, enabling data to be stored on disk for durability.

### Background:

- **Origin:** Redis was created by Salvatore Sanfilippo, commonly known as antirez, in 2009.

- **Language:** Redis is implemented in ANSI C, providing high performance and portability across different systems.

This challenge provides an opportunity to explore the architecture and functionalities of Redis, allowing you to gain practical experience in building a distributed, in-memory data store.

### Components of the Redis Server:

1. **Network Layer:** Handles incoming client connections and communication protocols.
   
2. **Command Processing:** Parses client commands and executes corresponding operations on the data store.
   
3. **Data Structures:** Implements various data structures such as strings, lists, sets, hashes, sorted sets, bitmaps, and hyperloglogs.
   
4. **Persistence:** Offers mechanisms for data persistence, including snapshotting and append-only file (AOF) persistence.

### Redis Commands:

- **GET key:** Get the value stored at the specified key.
  
- **SET key value [EX seconds] [PX milliseconds] [NX|XX]:** Set the value of a key with an optional expiration time and condition.
  
- **DEL key [key ...]:** Delete one or more keys.
  
- **INCR key:** Increment the integer value of a key by one.
  
- **DECR key:** Decrement the integer value of a key by one.
  
- **LPUSH key value [value ...]:** Prepend one or multiple values to a list.
  
- **RPUSH key value [value ...]:** Append one or multiple values to a list.



