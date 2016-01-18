#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <stdio.h>
#include <fstream>
#include <sys/types.h>
#include <dirent.h>
#include <unistd.h>

# define PI 3.1415927  /* pi */

using namespace std;
using namespace cv;


Mat compute(Mat image, int cols, int rows, int threshold){
	Mat descriptor;
	Mat ykernel = (Mat_<double>(3,3) << -1.0,-2.0,-1.0,0.0,0.0,0.0,1.0,2.0,1.0);
	Mat xkernel = (Mat_<double>(3,3) << -1.0,0.0,1.0,-2.0,0.0,2.0,-1.0,0.0,1.0);
	int bins = 18;
	float range[] = {0, 2*PI} ;
	const float* histRange = { range };
	int depth = CV_32F;
	Point anchor(-1,-1);
	int delta = 0;
	Mat dx, dy, orientations, magnitudes;
	filter2D(image, dx, depth, xkernel, anchor, delta, BORDER_DEFAULT);
	filter2D(image, dy, depth, ykernel, anchor, delta, BORDER_DEFAULT);
	cartToPolar(dx,dy,magnitudes,orientations,false);
	Mat mask_threshold = Mat::ones(image.rows, image.cols, image.depth());
	mask_threshold.setTo(0, magnitudes<=threshold);
	
	int width = image.cols;
	int height = image.rows;
	int rpb = height/rows;
	int cpb = width/cols;
	for(int row=0; row<rows; row++){
		for(int col=0; col<cols; col++){
			Mat hist;
			Mat mask = Mat::zeros(image.rows, image.cols, image.depth());
			Mat sector(mask, Rect(Point(cpb*col, rpb*row), Point(cpb*(col+1), rpb*(row+1))));
			Mat ROI(mask_threshold, Rect(Point(cpb*col, rpb*row), Point(cpb*(col+1), rpb*(row+1))));
			sector.setTo(1, ROI == 1);
			cout << countNonZero(mask) << endl;
			calcHist(&orientations, 1, 0, mask, hist, 1, &bins, &histRange, true, false);
			normalize(hist, hist);
			descriptor.push_back(hist);
		}
	}
	return descriptor;
}

int main0(int argc, char** argv){
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
		Mat descriptor = compute(image, 2, 2, 100);
		ofstream file;
		file.open((output_folder + string("/") + filenames[i]).c_str());
		file << descriptor;
		file.close();
	}
	return 0;
}

int main(int argc, char** argv){
	Mat image = imread("../../imdata/0001.jpg");
	cvtColor(image, image, CV_BGR2GRAY);
	Mat descriptor = compute(image, 2, 2, 100);
	cout << descriptor << endl;
}
