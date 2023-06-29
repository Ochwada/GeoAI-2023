import laspy

def convert_laz_to_las(input_file, output_file):
    # Open the .laz file
    las = laspy.read(input_file)

    # Create a new .las file
    las_out = laspy.create(file_version=las.version, point_format=las.point_format)

    # Copy header information from the original .laz file to the new .las file
    las_out.header = las.header

    # Copy point data from the original .laz file to the new .las file
    las_out.points = las.points

    # Save the new .las file
    las_out.write(output_file)

    # Close the files
    las.close()
    las_out.close()
    
print("Done")