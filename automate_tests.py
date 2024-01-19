import subprocess
import csv
import sys

# Check if the correct number of arguments is provided
if len(sys.argv) != 2:
    print("Usage: {} <number_of_times>".format(sys.argv[0]))
    sys.exit(1)

# Get the value of the command-line argument
times = int(sys.argv[1])

# Check if the argument is a positive integer
if not (times > 0):
    print("Please provide a positive integer as the argument.")
    sys.exit(1)

# List of tests to be run (replace placeholders with actual test names)
tests = [
    "org.apache.solr.search.TestSolrCachePerf",
    "org.apache.solr.search.TestSearchPerf",
    "org.apache.solr.request.TestWriterPerf",
    "org.apache.solr.update.TestIndexingPerformance",
    "org.apache.solr.core.TestConfLoadPerf",
    "org.apache.solr.cloud.PeerSyncReplicationTest.test",
    "org.apache.solr.cloud.ReplicationFactorTest.test",
    "org.apache.solr.cloud.SyncSliceTest.test",
    "org.apache.solr.cloud.UnloadDistributedZkTest.test",
    "org.apache.solr.cloud.TestCloudSearcherWarming.testPeersyncFailureReplicationSuccess",
    "org.apache.solr.cloud.ReindexCollectionTest.testSameTargetReindexing",
    "org.apache.solr.cloud.BasicDistributedZkTest.test",
    "org.apache.solr.handler.admin.MBeansHandlerTest.testMetricsSnapshot",
    "org.apache.solr.cloud.TestPullReplica",
    "org.apache.solr.cloud.ReindexCollectionTest",
    "org.apache.solr.cloud.MultiThreadedOCPTest",
    "org.apache.solr.cloud.PeerSyncReplicationTest",
    "org.apache.solr.search.TestRecovery",
    "org.apache.solr.search.TestCoordinatorRole",
    "org.apache.solr.cloud.TestCloudConsistency",
    "org.apache.solr.pkg.TestPackages"
]

# CSV file to log results
csv_file = "results.csv"

# Create or truncate the CSV file with headers
with open(csv_file, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["File", "Iteration", "Result"])

    # Run each test x times and log results in the CSV file
    for test_to_run in tests:
        for i in range(1, times + 1):
            print(f"Running {test_to_run} - Iteration {i}")

            # Construct the command to run the test
            command = [
                "./gradlew", "test", "--tests",
                "-Djavac.failOnWarnings=false", "-Dtests.useSecurityManager=false", test_to_run
            ]

            try:
                # Run the command and capture the result
                result = subprocess.check_output(command, text=True, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                # Handle error if the command fails
                result = f"Error: {e.output}"

            # Log the result in the CSV file
            csv_writer.writerow([test_to_run, i, result])

print("Script completed. Results are logged in {}".format(csv_file))

