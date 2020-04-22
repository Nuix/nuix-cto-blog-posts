#Require the SuperUtilities.jar

require 'aws-sdk-s3'

# Root directory that JSON files will be written to
$json_export_directory = 'F:/Exports/WSS_Temp'

# WSS doesn't get NUIX_VERSION set, so we need to use a hard coded value.
# We need this for SuperUtilities so that JSON Exporter can make a couple version
# checks regarding some features availabilitiy on WorkerItem and SourceItem after
# 7.4 and 7.6.  Note much of the rest of SuperUtilities may not work since we are
# providing nil for Utilities, but the JsonExporter should work just fine.
$nuix_version = "8.3"

# We can perform initialization here
def nuixWorkerItemCallbackInit
	awsAccess='AKIAJSMCBS6O52JAM4EA'
	awsSecret='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'
	awsRegion='us-east-1'
	$client = Aws::S3::Client.new(access_key_id: awsAccess, secret_access_key: awsSecret, region: awsRegion)

	java_import com.nuix.superutilities.SuperUtilities
	$su = SuperUtilities.init(nil,$nuix_version)
	java_import com.nuix.superutilities.export.JsonExporter
	$json_exporter = JsonExporter.new
end

# Define our worker item callback
def nuixWorkerItemCallback(worker_item)
	puts "#{worker_item.getItemGuid}"
	output_json_path = File.join($json_export_directory,"#{worker_item.getItemGuid}.json")
	output_json_file = java.io.File.new(output_json_path)
	output_json_file.getParentFile.mkdirs
	$json_exporter.exportWorkerItemAsJson(worker_item,output_json_file)

	awsBucket='com.xcorplabs.test'
	source_item = worker_item.source_item
	pathNames = source_item.getPathNames().join("/")
	puts pathNames

	$client.put_object(bucket: awsBucket, key:pathNames + "/" + worker_item.getItemGuid() + '.json', body: File.read(output_json_path))
	File.delete(output_json_path) if File.exist?(output_json_path)
end

# We can perform cleanup here if we need to
def nuixWorkerItemCallbackClose
end
