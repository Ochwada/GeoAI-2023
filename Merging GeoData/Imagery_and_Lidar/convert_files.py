import lasio
import laspy

# Converts a LAS file to a LAZ file.
  #Args:
    # --> input_file: The path to the input LAS file.
    # -->output_file: The path to the output LAZ file.
  #Returns:
     # -->None.

    

def las_to_laz(input_file, output_file):
    #Read the LAS file
    las_file = lasio.read(input_file)

    #Write the LAZ file
    las_file.write(output_file)




def laz_to_las(input_file, output_file):
    las = laspy.read(input_file)
    las_out = laspy.create(file_version=las.header.version, point_format=las.header.point_format)
    las_out.header = las.header
    las_out.points = las.points
    las_out.write(output_file)


print('successful conversion')