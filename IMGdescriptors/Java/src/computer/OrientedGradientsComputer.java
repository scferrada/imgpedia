package computer;

import java.util.ArrayList;
import java.util.List;

import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.MatOfFloat;
import org.opencv.core.MatOfInt;
import org.opencv.imgproc.Imgproc;

public class OrientedGradientsComputer extends DescriptorComputer {

	private int rows = 1;
	private int cols = 1;
	private double threshold = 0.0;
	private int bins = 18;
	private MatOfInt channels = new MatOfInt(0);
	private MatOfInt histSize;
	private MatOfFloat ranges = new MatOfFloat(0.0f, (float) (2*Math.PI));
	private double[][] x = new double[][]{{-1.0, 0.0, 1.0}, {-2.0, 0.0, 2.0}, {-1.0, 0.0, 1.0}};
	private double[][] y = new double[][]{{-1.0, -2.0, -1.0}, {0.0, 0.0, 0.0}, {1.0, 2.0, 1.0}};
	private Mat xkernel = new Mat(3,3,CvType.CV_32F);
	private Mat ykernel = new Mat(3,3,CvType.CV_32F);
	
	public OrientedGradientsComputer() {
		initializeKernels();
	}

	public OrientedGradientsComputer(int rows, int cols, double threshold) {
		this.rows = rows;
		this.cols = cols;
		this.threshold = threshold;
		initializeKernels();
	}
	
	private void initializeKernels() {
		for(int i=0; i<3; i++){
			for(int j=0; j<3; j++){
				this.xkernel.put(i, j, this.x[i][j]);
				this.ykernel.put(i, j, this.y[i][j]);
			}
		}
	}
	@Override
	public Mat compute(Mat image){
		Mat dx = new Mat();
		Mat dy = new Mat();
		Imgproc.filter2D(image, dx, CvType.CV_32F, this.xkernel);
		Imgproc.filter2D(image, dy, CvType.CV_32F, this.ykernel);
		Mat orientations = new Mat();
		Mat magnitudes = new Mat();
		Mat mask = new Mat();
		Core.cartToPolar(dx, dy, magnitudes, orientations);
		Imgproc.threshold(magnitudes, mask, threshold, 1, Imgproc.THRESH_BINARY);
		mask.convertTo(mask, CvType.CV_8UC1);
		System.out.println(Core.countNonZero(mask));
		int imageH = image.rows();
		int imageW = image.cols();
		List<Mat> descriptor = new ArrayList<Mat>();
		int rpf = imageH/this.rows;
		int cpf = imageW/this.cols;
		List<Mat> container = new ArrayList<Mat>();
		container.add(orientations);
		this.histSize = new MatOfInt(this.bins);
		for(int row=0; row<this.rows; row++){
			for(int col=0; col<this.cols; col++){
				Mat hist = new Mat();
				Mat sector = Mat.zeros(imageH, imageW, CvType.CV_8UC1);
				Mat ones = Mat.ones(rpf, cpf, CvType.CV_8UC1);
				Mat aux = sector.colRange(cpf*col, cpf*(col+1)).rowRange(rpf*row, rpf*(row+1));
				ones.copyTo(aux);
				Imgproc.calcHist(container, this.channels, sector.mul(mask), hist, this.histSize, this.ranges);
				Core.normalize(hist, hist);
				descriptor.add(hist);
			}
		}
		Mat ret = new Mat();
		Core.vconcat(descriptor, ret);
		
		return ret;
	}

	/*private int obtainFilteredOrientations(Mat dx, Mat dy, Mat orientations, Mat magnitudes, Mat mask) {
		int normfactor = 0;
		Mat magx = new Mat(), magy = new Mat();
		Core.absdiff(dx, Mat.zeros(dx.size(), dx.depth()), magx);
		Core.absdiff(dy, Mat.zeros(dy.size(), dy.depth()), magy);
		Core.add(magx, magy, magnitudes);
		for(int row=0; row<orientations.rows(); row++){
			for(int col=0; col<orientations.cols(); col++){
				double magnitude = magnitudes.get(row, col)[0];
				if(magnitude>this.threshold){
					double orientation = Math.atan2(dy.get(row, col)[0], dx.get(row, col)[0]);//*180.0/Math.PI;
					orientations.put(row, col, orientation);
					normfactor++;
					mask.put(row, col, 1);
				}else{
					orientations.put(row, col, 0.0f);
				}
			}
		}
		return normfactor;
	}*/
}
