import errno
import socket


def find_port(start=10000, end=20000) -> int:
    for candidate in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('0.0.0.0', candidate))
                return candidate
            except socket.error as e:
                if e.errno != errno.EADDRINUSE:
                    raise
    raise Exception(f'find_port(start={start},end={end}) no bindable tcp port found in interval')


if __name__ == '__main__':
    print(find_port())
    print(find_port())
