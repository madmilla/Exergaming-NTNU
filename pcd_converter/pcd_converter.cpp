#include <iostream>
#include <fstream>
#include <String>
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>

namespace fs = ::boost::filesystem;
using namespace std;


// return the filenames of all files that have the specified extension
// in the specified directory and all subdirectories
void get_all(const fs::path& root, const string& ext, vector<fs::path>& ret)
{
	if (!fs::exists(root) || !fs::is_directory(root)) return;
	fs::recursive_directory_iterator it(root);
	fs::recursive_directory_iterator endit;
	while (it != endit)
	{
		if (fs::is_regular_file(*it) && it->path().extension() == ext) {
			ret.push_back(it->path());
		}
		++it;
	}

}

void make_requested_dir(const string& create_this_dir) {
	boost::filesystem::path dir(create_this_dir);
	if (boost::filesystem::create_directories(dir)) {
		std::cout << "Folder succesfully created." << "\n";
	}
}

void open_PCD_files_and_store_as_ascii(const string& filepath, const string& filename, const string& where_to_store) {
	pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>);

	if (pcl::io::loadPCDFile<pcl::PointXYZ>(filepath+"\\"+filename, *cloud) == -1) //* load the file
	{
		PCL_ERROR("Couldn't read file \n");
		cout << filepath + "\\" + filename << " appears to not be a actual point cloud library file." << endl;
	}
	cout << "Processing " << filename << endl;
	pcl::io::savePCDFileASCII(where_to_store + "\\" + filename, *cloud);
}
void open_PCD_file_and_store_as_ascii(const string& filepath, const string& where_to_store) {
	pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>);

	if (pcl::io::loadPCDFile<pcl::PointXYZ>(filepath, *cloud) == -1) //* load the file
	{
		PCL_ERROR("Couldn't read file \n");
		cout << filepath << " appears to not be a actual point cloud library file." << endl;
	}
	std::string filename = filepath.substr(filepath.find_last_of("\\") + 1);
	cout << "Processing " << filename << endl;
	pcl::io::savePCDFileASCII(where_to_store + "\\" + filename, *cloud);
}

int main (int argc, char** argv)
{
	cout << "\nPCD Converter tool" << endl;
	cout << "V0.2 " << endl;
	if (argc != 3) {
		cout << "usage: " << argv[0] << " <filename or folder> <foldername to store file(s) in>\n";
		cout << "1. example: " << argv[0] << " C:\\PCDSamples1 C:\\exportfolder\n";
		cout << "2. example: " << argv[0] << " C:\\PCDSamples1\1.pcd C:\\exportfolder\n";
	} else {
		//argv[1] = "C:\code\PCDsample1\\";
		//cout << "argv0 = " << argv[0] << endl;
		cout << "Read file(s from)	\t= " << argv[1] << endl;
		cout << "Storing file(s) to  \t\t= " << argv[2] << "\n" << endl;
		//cout << argc << endl;
		//cout << "argv2 = " << argv[2] << endl;
		// We assume argv[1] is a filename to open
		ifstream the_file(argv[1]);
		// Always check to see if file opening succeeded
		if (!the_file.is_open()) {
			cout << "The first parameter is not a PCD file.\nContinuing with folder processing." << endl;
			vector<fs::path> temp;

			get_all(argv[1],".pcd", temp);
			if (temp.begin() == temp.end()) {
				cout << "Could not find any PCD files. Is this the correct folder? Does this folder exist?" << endl;
			}else{
				cout << "Amount of PCD files found: " << temp.size() << endl;
				make_requested_dir(argv[2]);
				for (std::vector<fs::path>::iterator it = temp.begin(); it != temp.end(); ++it) {
					open_PCD_files_and_store_as_ascii(it->branch_path().generic_string(), it->filename().generic_string(), argv[2]);
				}
				cout << "All done! Have a nice day!" << endl;
				
			}
		} else {
			make_requested_dir(argv[2]);
			open_PCD_file_and_store_as_ascii(argv[1], argv[2]);
			cout << "All done! Have a nice day!" << endl;
		}
	}

  return (0);
}

