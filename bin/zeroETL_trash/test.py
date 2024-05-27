
cluster = ['something']
cluster2 = ['something']

cluster = cluster[0] if len(cluster) > 0 else None
cluster2 = cluster2[0] if len(cluster2) > 0 else None

if(not cluster or not cluster2):
    raise Exception("cluser not found")

print(cluster)