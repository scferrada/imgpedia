#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <stdio.h>
#include <fstream>
#include <sys/types.h>
#include <dirent.h>
#include <unistd.h>

using namespace std;
using namespace cv;

Mat compute(Mat image, int cols, int rows, int bins){
	Mat descriptor;
	float range[] = { 0, 256 } ;
	const float* histRange = { range };
	int width = image.cols;
	int height = image.rows;
	int rpb = height/rows;
	int cpb = width/cols;
	for(int row=0; row<rows; row++){
		for(int col=0; col<cols; col++){
			Mat hist;
			Mat mask = Mat::zeros(height, width, image.depth());
			Mat ones(mask, Rect(Point(cpb*col, rpb*row), Point(cpb*(col+1), rpb*(row+1))));
			ones = 1;
 			calcHist(&image, 1, 0, mask, hist, 1, &bins, &histRange, true, false);
 			normalize(hist, hist);
 			descriptor.push_back(hist);
		} 
	}
	return descriptor;
}

int main(int argc, char** argv){
	if(argc <3){
		cout << "usage: ./ input_path output_path" <<endl;
		return -1;
	}

	//get all filenames
	DIR *dp;
	dirent *d;
	vector<string> filenames;
	if((dp = opendir(argv[1])) != NULL)
		perror("opendir");

	while((d = readdir(dp)) != NULL){
		if(!strcmp(d->d_name,".") || !strcmp(d->d_name,"..") || !strcmp(d->d_name,"Thumbs.db"))
			continue;
		filenames.push_back(string(d->d_name));
	}
	string input_folder = string(argv[1]);
	string output_folder = string(argv[2]);
	//calculate descriptor for each image
	for(int i=0; i<filenames.size(); i++){
		cout << input_folder + string("/") + filenames[i] << endl;
		Mat image = imread(input_folder + string("/") + filenames[i]);
		cvtColor(image, image, CV_BGR2GRAY);
		Mat descriptor = compute(image, 2, 2, 32);
		ofstream file;
		file.open((output_folder + string("/") + filenames[i]).c_str());
		file << descriptor;
		file.close();
	}
	return 0;
}
