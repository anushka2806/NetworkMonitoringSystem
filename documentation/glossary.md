# Glossary of Computer Networks Terms

## A
| Term | Definition |
| :-- | :-- |
| **ACK (Acknowledgment)** | A signal sent by receiver to sender indicating successful receipt of data. Used in TCP. |
| **API (Application Programming Interface)** | A set of rules allowing different software applications to communicate. REST API used here. |
| **ASGI (Asynchronous Server Gateway Interface)** | Interface between async Python web apps and servers. Uvicorn uses ASGI for FastAPI. |

## B
| Term | Definition |
| :-- | :-- |
| **Binding** | Associating a socket with a specific IP address and port number. |
| **Backend** | Server-side part of application (FastAPI server handling sockets, DB, logic). |

## C
| Term | Definition |
| :-- | :-- |
| **Client** | A program that initiates requests to a server. In our system, tcp_client.py and udp_heartbeat.py are clients. |
| **Client-Server Model** | Architecture where clients request services and servers provide them. |
| **CORS (Cross-Origin Resource Sharing)** | Mechanism allowing web browsers to permit requests from different origins (frontend to backend). |
| **Connection-Oriented** | Communication requiring established connection before data transfer (e.g., TCP). |
| **Connectionless** | Communication without prior connection establishment (e.g., UDP). |

## D
| Term | Definition |
| :-- | :-- |
| **Dashboard** | Web-based graphical interface to display monitoring information. |
| **Datagram** | A self-contained, independent packet of data sent over connectionless protocol (UDP). |
| **DBMS** | Database Management System. SQLite is our DBMS. |

## E
| Term | Definition |
| :-- | :-- |
| **Endpoint** | Specific URL path in API that clients can access (e.g., /clients, /alerts). |

## F
| Term | Definition |
| :-- | :-- |
| **Fault Detection** | Process of identifying network/component failures (client going offline). |
| **FastAPI** | Modern, fast web framework for building APIs with Python. |
| **Frontend** | Client-side part of application (React dashboard visible to user). |

## H
| Term | Definition |
| :-- | :-- |
| **Heartbeat** | Periodic signal sent by client to server to indicate it is alive and functioning. |
| **HTTP (HyperText Transfer Protocol)** | Application layer protocol used for web communication. REST uses HTTP. |

## I
| Term | Definition |
| :-- | :-- |
| **IP Address (Internet Protocol Address)** | Unique numeric address assigned to each device on network (IPv4 used here). |

## J
| Term | Definition |
| :-- | :-- |
| **JSON (Java# JavaScript Object Notation)** | Lightweight data-interchange format used for API responses and socket messages. |

## L
| Term | Definition |
| :-- | :-- |
| **Listening Socket** | TCP socket in listening state ready to accept incoming connections. |

## M
| Term | Definition |
| :-- | :-- |
| **Monitor Service** | Background component that checks heartbeats and detects faults. |
| **MVC/Component Architecture**# Much less common - just keep simple description |

## N
| Term | Definition |
| :-- | :-- |
| **Network Monitoring** | Process of observing network components to ensure availability and performance. |

## O
| Term | Definition |
| :-- | :-- |
| **Offline** | State where client is not responding/no heartbeat received. |
| **Online** | State where client is active and sending heartbeats. |

## P
| Term | Definition |
| :-- | :-- |
| **Port** | Numerical identifier for specific process/service on a device (e.w. TCP port 5000). |
| **Protocol** | Set of rules governing communication between devices. |
| **Python Socket Programming** | Using Python's `socket` module to implement network communication. |

## R
| Term | Definition |
| :-- | :-- |
| **REST (Representational State Transfer)** | Architectural style for designing networked applications using HTTP methods. |
| **RTT (Round Trip Time)**# Round Trip Time: Time taken for packet to travel from source to destination and back to source. Measured in milliseconds. |

## S
| Term | Definition |
| :-- | :-- |
| **Server** | Computer/program that provides services to clients. In our system, monitoring server. |
| **Socket** | Endpoint for sending or receiving data across a computer network. Combination of IP address and port. |
| **SQLite** | Lightweight, file-based relational database. No server needed. |
| **SYN, SYN-ACK, ACK** | Three steps in TCP 3-way handshake to establish connection. |

## T
| Term | Definition |
| :-- | :-- |
| **TCP (Transmission Control Protocol)** | Connection-oriented, reliable transport protocol. Guarantees delivery, ordering. Used for registration. |
| **Timeout** | Maximum time allowed after which operation is considered failed (heartbeat timeout). |
| **Transport Layer** | Layer 4 of OSI model - TCP and UDP operate here. |
| **3-Way Handshake** | TCP process to establish reliable connection between client and server. |

## U
| Term | Definition |
| :-- | :-- |
| **UDP (User Datagram Protocol)** | Connectionless, unreliable transport protocol. Faster, less overhead. Used for heartbeats. |
| **Uvicorn** | ASGI server used to run FastAPI applications. |

## W
| Term | Definition |
| :-- | :-- |
| **WebSocket (concept)** | Not used here, but mentioned for context - full-duplex communication. We use REST. |

## Important Distinctions for Viva
- **TCP vs UDP:** TCP reliable & connection-oriented; UDP fast & connectionless
- **Heartbeat vs Ping:** Heartbeat initiated by client; ping usually initiated by monitor
- **Alert vs Event:** Alert = fault notification (requires attention); Event = log entry (audit trail)
- **Online vs Connected:** Client might be TCP-connected but not sending heartbeats - our logic uses heartbeats for liveness
