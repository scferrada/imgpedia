package computer;

import java.util.ArrayList;
import java.util.List;

import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.MatOfFloat;
import org.opencv.core.MatOfInt;
import org.opencv.imgproc.Imgproc;

public class GrayHistogramComputer extends DescriptorComputer {

	private int rows = 1;
	private int cols = 1;
	private int bins = 256;
	private MatOfInt channels = new MatOfInt(0);
	private MatOfInt histSize;
	private MatOfFloat ranges = new MatOfFloat(0.0f, 256.0f);
	

	public GrayHistogramComputer(int rows, int cols, int bins) {
		this.rows = rows;
		this.cols = cols;
		this.bins = bins;
	}
	
	@Override
	public Mat compute(Mat image) {
		List<Mat> img = new ArrayList<Mat>();
		img.add(image);
		this.histSize = new MatOfInt(this.bins);
		
		int imageH = image.rows();
		int imageW = image.cols();
		List<Mat> descriptor = new ArrayList<Mat>();
		int rpf = imageH/this.rows;
		int cpf = imageW/this.cols;
		for(int row=0; row<this.rows; row++){
			for(int col=0; col<this.cols; col++){
				Mat hist = new Mat();
				Mat mask = Mat.zeros(imageH, imageW, CvType.CV_8U);
				Mat ones = Mat.ones(rpf, cpf, CvType.CV_8U);
				Mat aux = mask.colRange(cpf*col, cpf*(col+1)).rowRange(rpf*row, rpf*(row+1));
				ones.copyTo(aux);
				Imgproc.calcHist(img, this.channels, mask, hist, this.histSize, this.ranges);
				Core.normalize(hist, hist);
				descriptor.add(hist);
			}
		}
		Mat ret = new Mat();
		Core.vconcat(descriptor, ret);
		return ret;
	}

}
