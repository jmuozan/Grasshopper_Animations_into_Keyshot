#1- GHPython
Vert_data = open(Vert_storage, "w")
Face_data = open(Face_storage, "w")


for v in Mesh.Vertices:
	Vert_data.write(str(v) + "\n")
Vert_data.close()

for f in Mesh.Faces:
	Face_data.write(str(f)[2:-1] + "\n")
Face_data.close()