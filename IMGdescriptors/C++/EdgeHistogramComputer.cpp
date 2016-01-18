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

Mat compute(Mat image, int rows, int cols){

	std::vector<Mat> kernels;
	double sqrt2 = std::sqrt(2.0);
	kernels.push_back((Mat_<double>(2,2) << 1.0,1.0,-1.0,-1.0));
	kernels.push_back((Mat_<double>(2,2) << 1.0,-1.0,1.0,-1.0));
	kernels.push_back((Mat_<double>(2,2) << sqrt2,0.0,0.0,-sqrt2));
	kernels.push_back((Mat_<double>(2,2) << 0.0,sqrt2,-sqrt2,0.0));
	kernels.push_back((Mat_<double>(2,2) << 2.0,-2.0,-2.0,2.0));

	Mat descriptor;
	Mat dominant_gradients = Mat::zeros(image.rows, image.cols, image.depth());
	Mat max_gradient;
	float range[] = { 0, 5 } ;
    const float* histRange = { range };
	int depth = CV_32F;
	Point anchor(-1,-1);
	int delta = 0;
	int bins = 5;
	filter2D(image, max_gradient, depth, kernels[0], anchor, delta, BORDER_DEFAULT);
	max_gradient = abs(max_gradient);
	for(int i=1; i<bins; i++){
		Mat kernel = kernels[i];
		Mat gradient;
		filter2D(image, gradient, depth, kernel, anchor,delta, BORDER_DEFAULT);
		gradient = abs(gradient);
		max(max_gradient, gradient, max_gradient);
		dominant_gradients.setTo(i, max_gradient == gradient);
	}
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
			calcHist(&dominant_gradients, 1, 0, mask, hist, 1, &bins, &histRange, true, false);
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
		Mat descriptor = compute(image, 2, 2);
		ofstream file;
		file.open((output_folder + string("/") + filenames[i]).c_str());
		file << descriptor;
		file.close();
	}
	return 0;
}
