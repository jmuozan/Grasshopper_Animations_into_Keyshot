if Clear:
	open(Animation_path, "w")
if not Clear:
	A_data = open(Animation_path, "a")
	for v in Mesh.Vertices:
		A_data.write(str(v) + ",")
	A_data.write("\n")
A_data.close()
