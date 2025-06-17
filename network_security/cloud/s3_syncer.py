
import os
import subprocess

class S3Sync:
    # def sync_folder_to_s3(self,folder,aws_bucket_url):
    #     command = ["aws", "s3", "sync", folder, aws_bucket_url]
    #     #command = f"aws s3 sync {folder} {aws_bucket_url} "
    #     os.system(command)


    def sync_folder_to_s3(self, folder, aws_bucket_url):
        try:
            result = subprocess.run(["aws", "s3", "sync", folder, aws_bucket_url], check=True, capture_output=True, text=True)
            print("Upload Output:", result.stdout)
        except subprocess.CalledProcessError as e:
            print("Upload Failed:", e.stderr)

    
    def sync_folder_from_s3(self,folder,aws_bucket_url):
        #command = f"aws s3 sync  {aws_bucket_url} {folder} "
        command = ["aws", "s3", "sync", aws_bucket_url, folder]
        os.system(command)



# class S3Sync:
#     def sync_folder_to_s3(self, folder, aws_bucket_url):
#         command = ["aws", "s3", "sync", folder, aws_bucket_url]
#         result = subprocess.run(command, capture_output=True, text=True)
#         if result.returncode != 0:
#             print(f"Error syncing to S3: {result.stderr}")

#     def sync_folder_from_s3(self, folder, aws_bucket_url):
#         command = ["aws", "s3", "sync", aws_bucket_url, folder]
#         result = subprocess.run(command, capture_output=True, text=True)
#         if result.returncode != 0:
#             print(f"Error syncing from S3: {result.stderr}")
