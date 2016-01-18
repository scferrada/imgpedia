package computer;

import java.util.ArrayList;
import java.util.List;

import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.MatOfFloat;
import org.opencv.core.MatOfInt;
import org.opencv.imgproc.Imgproc;

public class EdgeHistogramComputer extends DescriptorComputer {

	private final float sqrt2 = (float) Math.sqrt(2);
	private List<Mat> kernels = new ArrayList<Mat>();
	private int rows = 1;
	private int cols = 1;
	private int bins = 5;
	private MatOfInt channels = new MatOfInt(0);
	private MatOfInt histSize;
	private MatOfFloat ranges = new MatOfFloat(0.0f, 5.0f);
	private float[][] a = new float[][]{{1.0f, 1.0f}, {-1.0f, -1.0f}};
	private float[][] b = new float[][]{{1.0f, -1.0f}, {1.0f, -1.0f}};
	private float[][] c = new float[][]{{sqrt2, 0.0f}, {0.0f, -sqrt2}};
	private float[][] d = new float[][]{{0.0f, sqrt2}, {-sqrt2, 0.0f}};
	private float[][] e = new float[][]{{2.0f, -2.0f}, {-2.0f, 2.0f}};
	
	public EdgeHistogramComputer(int rows, int cols) {
		this();
		this.rows = rows;
		this.cols = cols;
	}
	
	public EdgeHistogramComputer() {
		this.initializeKernels();
	}
	
	private void initializeKernels() {
		Mat y = new Mat(2,2,CvType.CV_32F);
		Mat x = new Mat(2,2,CvType.CV_32F);
		Mat diag = new Mat(2,2,CvType.CV_32F);
		Mat invdiag = new Mat(2,2,CvType.CV_32F);
		Mat none = new Mat(2,2,CvType.CV_32F);
		for(int row=0; row<2; row++){
			for(int col=0; col<2; col++){
				y.put(row, col, a[row][col]);
				x.put(row, col, b[row][col]);
				diag.put(row, col, c[row][col]);
				invdiag.put(row, col, d[row][col]);
				none.put(row, col, e[row][col]);
			}
		}
		this.kernels.add(y);
		this.kernels.add(x);
		this.kernels.add(diag);
		this.kernels.add(invdiag);
		this.kernels.add(none);
	}

	@Override
	public Mat compute(Mat image) {
		List<Mat> descriptor = new ArrayList<Mat>();
		Mat dominantGradients = Mat.zeros(image.size(), CvType.CV_32F);
		Mat maxGradient = new Mat();
		Imgproc.filter2D(image, maxGradient, CvType.CV_32F, this.kernels.get(0));
		Core.absdiff(maxGradient, Mat.zeros(maxGradient.size(), CvType.CV_32F), maxGradient);
		for(int i=1; i<this.kernels.size(); i++){
			Mat kernel = this.kernels.get(i);
			Mat gradient = new Mat();
			Imgproc.filter2D(image, gradient, CvType.CV_32F, kernel);
			Core.absdiff(gradient, Mat.zeros(gradient.size(), CvType.CV_32F), gradient);
			Core.max(maxGradient, gradient, maxGradient);
			updateDominant(maxGradient, gradient, i, dominantGradients);
		}
		int imageH = image.rows();
		int imageW = image.cols();
		int rpf = imageH/this.rows;
		int cpf = imageW/this.cols;
		this.histSize = new MatOfInt(this.bins);
		List<Mat> container = new ArrayList<Mat>();
		container.add(dominantGradients);
		for(int row=0; row<this.rows; row++){
			for(int col=0; col<this.cols; col++){
				Mat hist = new Mat();
				Mat mask = Mat.zeros(imageH, imageW, CvType.CV_8U);
				Mat ones = Mat.ones(rpf, cpf, CvType.CV_8U);
				Mat aux = mask.colRange(cpf*col, cpf*(col+1)).rowRange(rpf*row, rpf*(row+1));
				ones.copyTo(aux);
				Imgproc.calcHist(container, this.channels, mask, hist, this.histSize, this.ranges);
				Core.normalize(hist, hist);
				descriptor.add(hist);
			}
		}
		Mat ret = new Mat();
		Core.vconcat(descriptor, ret);
		return ret;
	}

	private void updateDominant(Mat maxGradient, Mat gradient, int i, Mat dominantGradients) {
		for(int row=0; row<maxGradient.rows(); row++){
			for(int col=0; col<maxGradient.cols(); col++){
				if(maxGradient.get(row, col)[0] == gradient.get(row, col)[0]){
					dominantGradients.put(row, col, i);
				}
			}
		}
	}

}
