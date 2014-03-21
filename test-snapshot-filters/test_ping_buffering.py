import pdb
import sys
from mq.requester import Requester
from snapshot.snapshot_service import SnapshotService
from snapshot.snapshot_filter import SnapshotFilter
from threading import Thread, Timer
import thread
import time

# The point of this is to set up a TestFilter that listens for changes to a file
# managed by a SnapshotService. We want to have it collapse requests that happen
# in a brief period and only do one update sometime afterwards.

class TestFilter(SnapshotFilter):
    def __init__(self, snapshot_req_port, snapshot_sub_port, inputs):
        listen = False
        host = "127.0.0.1"
        retry_period = 1000
        output = ''
        SnapshotFilter.__init__(self, listen, host, snapshot_req_port,
                                snapshot_sub_port, retry_period, inputs, output)
        return

    def get_processed_data(self):
        [result] = self.get_inputs()
        return result

    #@Override
    # NOTE:     We wouldn't normally override this
    def process_data_once(self):
        contents = self.get_processed_data()
        print("Simulate processing of data")
        print(contents)
        return

def start_snapshot_service(reply_port, publish_port):
    header_file_map = {}
    header_file_map['test_file'] = "./test_file.txt"

    working_directory = "./tmp"
    service = SnapshotService(header_file_map, working_directory, reply_port, publish_port)
    service.run()
    return

def start_test_filter(req_port, sub_port):
    test_filter = TestFilter(req_port, sub_port, ["=====test_file"])
    test_filter.run()
    return


if __name__ == "__main__":
    reply_port = 10000
    publish_port = 10001

    # Start the snapshot service
    snapshot_service_thread = Thread(target=start_snapshot_service, args=(reply_port, publish_port))
    snapshot_service_thread.daemon = True
    snapshot_service_thread.start()

    # Start the filter we want to exercise
    test_filter_thread = Thread(target=start_test_filter, args=(reply_port, publish_port))
    test_filter_thread.daemon = True
    test_filter_thread.start()

    # Update file
    #   NOTE: We should only see one "Simulate processing of data" message if
    #   this works properly.
    requester = Requester("127.0.0.1", reply_port)
    for i in range(10):
        requester.make_request("=====PUT test_file\n\t%d" % i)


    # Wait until test is done
    exit_timer = Timer(5, sys.exit, args=(0,))
    exit_timer.start()

