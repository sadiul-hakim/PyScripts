import asyncio

# Set to keep track of all currently connected client writers
connected_clients: set[asyncio.StreamWriter] = set()


async def broadcast(
    message: str, sender_writer: asyncio.StreamWriter | None = None
) -> None:
    """Send a message to all connected clients, optionally skipping the sender."""
    encoded = message.encode("utf-8")

    # Iterate over a copy of the set in case a client disconnects during broadcast
    for client_writer in list(connected_clients):
        if client_writer is not sender_writer:
            try:
                client_writer.write(encoded)
                # await writer.drain() suspends until the OS socket buffer is flushed
                await client_writer.drain()
            except ConnectionError:
                connected_clients.discard(client_writer)


async def handle_client(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    """
    Runs independently as a separate task for EACH connected client.
    Handles greeting, message receiving, broadcasting, and cleanup.
    """
    addr = writer.get_extra_info("peername")
    client_name = f"{addr[0]}:{addr[1]}"
    print(f"[+] Connected: {client_name}")

    connected_clients.add(writer)

    # 1. Welcome the new client
    writer.write(f"Welcome to the Async Chat, {client_name}!\n".encode("utf-8"))
    writer.write(b"Type your message and hit Enter. Type 'quit' to exit.\n\n")
    await writer.drain()

    # 2. Notify everyone else
    await broadcast(f"*** {client_name} joined the room ***\n", sender_writer=writer)

    try:
        while True:
            # Suspends until a newline arrives from THIS client
            # Other clients continue chatting while this client is waiting
            data = await reader.readline()

            # Empty bytes (b'') means the client closed the connection (EOF)
            if not data:
                break

            message = data.decode("utf-8", errors="replace").strip()

            if message.lower() == "quit":
                break

            if message:
                print(f"[{client_name}] {message}")
                await broadcast(f"[{client_name}]: {message}\n", sender_writer=writer)

    except ConnectionResetError:
        print(f"[-] Abrupt disconnection from: {client_name}")
    finally:
        # 3. Clean up when client disconnects
        connected_clients.discard(writer)
        print(f"[-] Disconnected: {client_name}")
        await broadcast(f"*** {client_name} left the room ***\n")

        writer.close()
        await writer.wait_closed()


async def main(host: str = "127.0.0.1", port: int = 8888) -> None:
    # start_server automatically calls handle_client(reader, writer) as a new task
    # whenever a new connection is accepted
    server = await asyncio.start_server(handle_client, host, port)

    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"🚀 TCP Chat Server running on {addrs}")
    print("Waiting for connections... (Press Ctrl+C to stop)\n")

    async with server:
        # Keep server running forever until cancelled
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped.")
