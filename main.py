import boto3

#####
ACCESS_ID = 'id'
SECRET_KEY = 'key'
BUCKET = 'bucket'
REGION_NAME = "ams3"
ENDPOINT = "https://ams3.digitaloceanspaces.com"
###


server_list = []
final_dict = {}


def sizeof(num, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

session = boto3.session.Session()
client = session.client('s3',
                            region_name=REGION_NAME,
                            endpoint_url=ENDPOINT,
                            aws_access_key_id=ACCESS_ID,
                            aws_secret_access_key=SECRET_KEY)


for key in client.list_objects(Bucket=BUCKET, MaxKeys=25000)['Contents']:
    server_name = key['Key'].split('/')[0]
    size = key['Size']
    if server_name not in final_dict.keys():
        final_dict[server_name] = size
    else:
        old_size = final_dict.get(server_name)
        final_dict[server_name] = size + old_size
        
for key, value in final_dict.items():
    final_dict[key] = sizeof(value)

print(final_dict)