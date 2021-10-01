from linode_api4 import LinodeClient
token = "1130e72b887afd10b9961e035241c2c90c73080ad535e69c88950d22cfa23d77"
client = LinodeClient(token)

my_linodes = client.linode.instances()

for current_linode in my_linodes:
    print(current_linode.label)

available_regions = client.regions()

chosen_region = available_regions[0]

new_linode, password = client.linode.instance_create('g5-standard-4',
                                                     chosen_region,
                                                     image='linode/debian9')


print(new_linode)
print(password)

print("ssh root@{} - {}".format(new_linode.ipv4[0], password))