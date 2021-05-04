# From the STEM examples page
# https://stem.torproject.org/tutorials/examples/exit_used.html

import functools

from stem import StreamStatus
from stem.control import EventType, Controller

def main():
  print("Tracking requests for Tor circuits. Press 'enter' to end.")
  print("")

  with Controller.from_port() as controller:
    controller.authenticate()

    stream_listener = functools.partial(stream_event, controller)
    controller.add_event_listener(stream_listener, EventType.STREAM)

    input()  # wait for user to press enter


def stream_event(controller, event):
  if event.status == StreamStatus.SUCCEEDED and event.circ_id:
    circ = controller.get_circuit(event.circ_id)

    exit_fingerprint = circ.path[-1][0]
    exit_relay = controller.get_network_status(exit_fingerprint)

    print("Circuit for our connection to %s" % (event.target))
    print("  exit relay address: %s" % (exit_relay.address))
    print("  path: ")
    for hop in circ.path:
        print("        ", hop)
    print("")


if __name__ == '__main__':
  main()
