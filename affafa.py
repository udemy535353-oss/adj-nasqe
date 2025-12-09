import socket

addr = ("", 8080)  # all interfaces, port 8080
if socket.has_dualstack_ipv6():
    print("finded ipv6_pla")
    s = socket.create_server(addr, family=socket.AF_INET6, dualstack_ipv6=True)
    print(socket.getaddrinfo("youtube.com",80,proto=socket.IPPROTO_TCP))
else:
    s = socket.create_server(addr)